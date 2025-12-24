"""
Knowledge base for QA RAG.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import re
import json
import hashlib
import pickle

import httpx
from PyPDF2 import PdfReader

from app.core.config.settings import settings
from app.modules.qa.rag.vector_store import BM25VectorStore, Chunk, tokenize
from app.modules.qa.rag.retriever import Retriever
from app.modules.qa.prompts.qa_prompts import RAG_SYSTEM_PROMPT, GENERAL_SYSTEM_PROMPT


_CJK_PATTERN = re.compile(r"[\u4e00-\u9fff]")


@dataclass
class RetrievalResult:
    chunks: List[Chunk]


class KnowledgeBase:
    def __init__(
        self,
        dataset_dir: Optional[Path] = None,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        max_pages: int = 30,
        max_docs: int = 5
    ):
        self.dataset_dir = dataset_dir or Path(__file__).resolve().parents[4] / "dataset"
        self.cache_dir = Path(__file__).resolve().parents[4] / ".cache" / "qa_rag"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        (self.cache_dir / "texts").mkdir(parents=True, exist_ok=True)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_pages = max_pages
        self.max_docs = max_docs
        self._chunks: List[Chunk] = []
        self._store: Optional[BM25VectorStore] = None
        self._retriever: Optional[Retriever] = None
        self._current_index_key: Optional[str] = None

    def _list_pdfs(self) -> List[Path]:
        if not self.dataset_dir.exists():
            return []
        return sorted(self.dataset_dir.glob("*.pdf"))

    def _match_documents(self, query: str) -> List[Path]:
        pdfs = self._list_pdfs()
        if not pdfs:
            return []

        query_tokens = set(tokenize(query))
        ranked = []
        for pdf in pdfs:
            name = pdf.stem
            tokens = set(tokenize(name))
            overlap = len(tokens & query_tokens)
            if overlap:
                ranked.append((pdf, overlap))
        ranked.sort(key=lambda item: item[1], reverse=True)

        if ranked:
            return [item[0] for item in ranked[: self.max_docs]]

        # fallback: match by CJK characters in filename
        cjk_chars = set(_CJK_PATTERN.findall(query))
        if cjk_chars:
            scored = []
            for pdf in pdfs:
                score = sum(1 for char in cjk_chars if char in pdf.stem)
                if score:
                    scored.append((pdf, score))
            scored.sort(key=lambda item: item[1], reverse=True)
            if scored:
                return [item[0] for item in scored[: self.max_docs]]

        return pdfs[: min(self.max_docs, len(pdfs))]

    def _cache_key_for_pdf(self, pdf_path: Path) -> str:
        return hashlib.sha256(str(pdf_path).encode("utf-8")).hexdigest()

    def _get_text_cache_paths(self, pdf_path: Path) -> Tuple[Path, Path]:
        cache_key = self._cache_key_for_pdf(pdf_path)
        text_path = self.cache_dir / "texts" / f"{cache_key}.txt"
        meta_path = self.cache_dir / "texts" / f"{cache_key}.json"
        return text_path, meta_path

    def _read_pdf_text(self, pdf_path: Path) -> str:
        text_path, meta_path = self._get_text_cache_paths(pdf_path)
        stats = pdf_path.stat()
        meta = {"mtime": stats.st_mtime, "size": stats.st_size}
        if text_path.exists() and meta_path.exists():
            try:
                cached_meta = json.loads(meta_path.read_text(encoding="utf-8"))
                if cached_meta == meta:
                    return text_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass

        reader = PdfReader(str(pdf_path))
        pages = reader.pages[: self.max_pages]
        texts = []
        for page in pages:
            text = page.extract_text() or ""
            texts.append(text)
        full_text = "\n".join(texts)
        try:
            text_path.write_text(full_text, encoding="utf-8")
            meta_path.write_text(json.dumps(meta, ensure_ascii=True), encoding="utf-8")
        except Exception:
            pass
        return full_text

    def _chunk_text(self, text: str, source: str) -> List[Chunk]:
        chunks: List[Chunk] = []
        if not text:
            return chunks
        length = len(text)
        start = 0
        index = 0
        while start < length:
            end = min(start + self.chunk_size, length)
            content = text[start:end].strip()
            if content:
                chunk_id = f"{source}-{index}"
                chunks.append(Chunk(chunk_id=chunk_id, content=content, source=source, page=index))
                index += 1
            start = end - self.chunk_overlap
            if start < 0:
                start = 0
        return chunks

    def _build_index(self, pdfs: List[Path]) -> None:
        chunks: List[Chunk] = []
        for pdf in pdfs:
            text = self._read_pdf_text(pdf)
            chunks.extend(self._chunk_text(text, pdf.stem))
        self._chunks = chunks
        self._store = BM25VectorStore(chunks)
        self._retriever = Retriever(self._store)

    def _index_signature(self, pdfs: List[Path]) -> Tuple[str, Dict[str, object]]:
        files = []
        for pdf in pdfs:
            stat = pdf.stat()
            files.append(
                {
                    "name": pdf.name,
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                }
            )
        payload = {
            "files": sorted(files, key=lambda item: item["name"]),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "max_pages": self.max_pages,
        }
        signature = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        return signature, payload

    def _index_paths(self, signature: str) -> Tuple[Path, Path]:
        index_path = self.cache_dir / f"{signature}.pkl"
        meta_path = self.cache_dir / f"{signature}.json"
        return index_path, meta_path

    def _load_index(self, signature: str) -> bool:
        index_path, meta_path = self._index_paths(signature)
        if not index_path.exists() or not meta_path.exists():
            return False
        try:
            state = pickle.loads(index_path.read_bytes())
            store = BM25VectorStore.from_state(state)
            self._store = store
            self._retriever = Retriever(store)
            return True
        except Exception:
            return False

    def _save_index(self, signature: str, meta: Dict[str, object]) -> None:
        if not self._store:
            return
        index_path, meta_path = self._index_paths(signature)
        try:
            index_path.write_bytes(pickle.dumps(self._store.to_state()))
            meta_path.write_text(json.dumps(meta, ensure_ascii=True), encoding="utf-8")
        except Exception:
            pass

    def retrieve(self, query: str, top_k: int = 4) -> RetrievalResult:
        pdfs = self._match_documents(query)
        signature, meta = self._index_signature(pdfs)
        if self._current_index_key != signature:
            loaded = self._load_index(signature)
            if not loaded:
                self._build_index(pdfs)
                self._save_index(signature, meta)
            self._current_index_key = signature
        if not self._retriever:
            return RetrievalResult(chunks=[])
        chunks = self._retriever.retrieve(query, top_k=top_k)
        return RetrievalResult(chunks=chunks)

    async def generate_answer(self, query: str, top_k: int = 4) -> str:
        retrieval = self.retrieve(query, top_k=top_k)
        context = "\n\n".join(chunk.content for chunk in retrieval.chunks)
        if not context:
            prompt = f"{GENERAL_SYSTEM_PROMPT}\n\n用户问题：{query}\n\n请给出简洁、实用的回答："
            return await self._call_anthropic(prompt)

        prompt = f"{RAG_SYSTEM_PROMPT}\n\n参考资料：\n{context}\n\n用户问题：{query}\n\n请给出简洁、实用的回答："
        response = await self._call_anthropic(prompt)
        return response or f"参考资料：\n{context}\n\n问题：{query}"

    async def generate_general_answer(self, query: str) -> str:
        prompt = f"{GENERAL_SYSTEM_PROMPT}\n\n用户问题：{query}\n\n请给出简洁、实用的回答："
        return await self._call_anthropic(prompt)

    async def _call_anthropic(self, prompt: str) -> str:
        if not settings.ANTHROPIC_AUTH_TOKEN or not settings.ANTHROPIC_BASE_URL:
            return ""

        base_url = settings.ANTHROPIC_BASE_URL.rstrip("/")
        if base_url.endswith("/v1/messages"):
            url = base_url
        else:
            url = base_url + "/v1/messages"
        headers = {
            "Authorization": f"Bearer {settings.ANTHROPIC_AUTH_TOKEN}",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": settings.ANTHROPIC_MODEL or "glm-4.6",
            "max_tokens": 800,
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}],
        }

        timeout = settings.API_TIMEOUT_MS / 1000 if settings.API_TIMEOUT_MS else 60
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("choices"):
                        return data["choices"][0].get("message", {}).get("content", "")
                    if "content" in data and data["content"]:
                        return data["content"][0].get("text", "")
                # Fallback: try OpenAI-compatible endpoint for GLM
                if "open.bigmodel.cn" in base_url:
                    fallback_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
                    fallback_headers = {
                        "Authorization": f"Bearer {settings.ANTHROPIC_AUTH_TOKEN}",
                        "content-type": "application/json",
                    }
                    fallback_payload = {
                        "model": settings.ANTHROPIC_MODEL or "glm-4.6",
                        "max_tokens": 800,
                        "temperature": 0.2,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                    fallback_resp = await client.post(
                        fallback_url,
                        headers=fallback_headers,
                        json=fallback_payload
                    )
                    if fallback_resp.status_code == 200:
                        data = fallback_resp.json()
                        if data.get("choices"):
                            return data["choices"][0].get("message", {}).get("content", "")
            except Exception:
                return ""
        return ""


_knowledge_base: Optional[KnowledgeBase] = None


def get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base
