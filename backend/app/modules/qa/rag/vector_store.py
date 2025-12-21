"""
Simple in-memory vector store using BM25 scoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import List, Dict, Iterable, Tuple
import re


_TOKEN_PATTERN = re.compile(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+")


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in _TOKEN_PATTERN.findall(text)]


@dataclass
class Chunk:
    chunk_id: str
    content: str
    source: str
    page: int


class BM25VectorStore:
    """
    Minimal BM25 implementation for chunk retrieval.
    """

    def __init__(self, chunks: Iterable[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = list(chunks)
        self.k1 = k1
        self.b = b
        self._doc_tokens: List[List[str]] = []
        self._doc_freq: Dict[str, int] = {}
        self._avg_doc_len = 0.0
        self._build_index()

    def _build_index(self) -> None:
        total_len = 0
        for chunk in self.chunks:
            tokens = tokenize(chunk.content)
            self._doc_tokens.append(tokens)
            total_len += len(tokens)
            seen = set(tokens)
            for token in seen:
                self._doc_freq[token] = self._doc_freq.get(token, 0) + 1
        self._avg_doc_len = total_len / max(len(self.chunks), 1)

    def _idf(self, term: str) -> float:
        n_docs = max(len(self.chunks), 1)
        df = self._doc_freq.get(term, 0)
        return log((n_docs - df + 0.5) / (df + 0.5) + 1)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[Chunk, float]]:
        q_tokens = tokenize(query)
        scores: List[Tuple[int, float]] = []
        for idx, tokens in enumerate(self._doc_tokens):
            if not tokens:
                continue
            freq: Dict[str, int] = {}
            for token in tokens:
                freq[token] = freq.get(token, 0) + 1
            doc_len = len(tokens)
            score = 0.0
            for term in q_tokens:
                if term not in freq:
                    continue
                idf = self._idf(term)
                tf = freq[term]
                denom = tf + self.k1 * (1 - self.b + self.b * doc_len / (self._avg_doc_len or 1))
                score += idf * (tf * (self.k1 + 1)) / (denom or 1)
            if score > 0:
                scores.append((idx, score))

        scores.sort(key=lambda item: item[1], reverse=True)
        results = [(self.chunks[idx], score) for idx, score in scores[:top_k]]
        return results
