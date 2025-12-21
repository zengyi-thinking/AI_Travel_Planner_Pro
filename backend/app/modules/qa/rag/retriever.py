"""
Retriever for QA knowledge base.
"""

from __future__ import annotations

from typing import List
from app.modules.qa.rag.vector_store import BM25VectorStore, Chunk


class Retriever:
    def __init__(self, store: BM25VectorStore):
        self.store = store

    def retrieve(self, query: str, top_k: int = 4) -> List[Chunk]:
        results = self.store.search(query, top_k=top_k)
        return [chunk for chunk, _score in results]
