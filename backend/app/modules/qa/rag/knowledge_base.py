"""
Knowledge base for QA RAG.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import re

import httpx
from PyPDF2 import PdfReader

from app.core.config.settings import settings
from app.modules.qa.rag.vector_store import BM25VectorStore, Chunk, tokenize
from app.modules.qa.rag.retriever import Retriever
from app.modules.qa.prompts.qa_prompts import RAG_SYSTEM_PROMPT


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
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_pages = max_pages
        self.max_docs = max_docs
        self._chunks: List[Chunk] = []
        self._store: Optional[BM25VectorStore] = None
        self._retriever: Optional[Retriever] = None

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

    def _read_pdf_text(self, pdf_path: Path) -> str:
        reader = PdfReader(str(pdf_path))
        pages = reader.pages[: self.max_pages]
        texts = []
        for page in pages:
            text = page.extract_text() or ""
            texts.append(text)
        return "\n".join(texts)

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

    def retrieve(self, query: str, top_k: int = 4) -> RetrievalResult:
        pdfs = self._match_documents(query)
        self._build_index(pdfs)
        if not self._retriever:
            return RetrievalResult(chunks=[])
        chunks = self._retriever.retrieve(query, top_k=top_k)
        return RetrievalResult(chunks=chunks)

    async def generate_answer(self, query: str, top_k: int = 4) -> str:
        retrieval = self.retrieve(query, top_k=top_k)
        context = "\n\n".join(chunk.content for chunk in retrieval.chunks)
        if not context:
            return "未在知识库中找到相关内容，请尝试更具体的目的地或问题。"

        prompt = f"{RAG_SYSTEM_PROMPT}\n\n参考资料：\n{context}\n\n用户问题：{query}\n\n请给出简洁、实用的回答："
        response = await self._call_anthropic(prompt)
        return response or f"参考资料：\n{context}\n\n问题：{query}"

    async def _call_anthropic(self, prompt: str) -> str:
        if not settings.ANTHROPIC_AUTH_TOKEN or not settings.ANTHROPIC_BASE_URL:
            return ""

        url = settings.ANTHROPIC_BASE_URL.rstrip("/") + "/v1/messages"
        headers = {
            "x-api-key": settings.ANTHROPIC_AUTH_TOKEN,
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
                resp.raise_for_status()
                data = resp.json()
                if "content" in data and data["content"]:
                    return data["content"][0].get("text", "")
            except Exception:
                return ""
        return ""


_knowledge_base: Optional[KnowledgeBase] = None


def get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base
