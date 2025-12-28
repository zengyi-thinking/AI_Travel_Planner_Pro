"""
QA Agent for chat functionality.

This module provides intelligent agent for QA system,
integrating with LLM factory, RAG retriever, and prompt templates.
"""

from typing import List, Dict, Any, Optional
from app.core.ai.factory import LLMFactory
from app.modules.qa.rag.retriever import Retriever
from app.modules.qa.rag.knowledge_base import get_knowledge_base
from app.modules.qa.prompts.qa_prompts import (
    create_rag_prompt,
    create_general_prompt
)
from langchain_core.messages import HumanMessage, SystemMessage
import logging

logger = logging.getLogger(__name__)


class QAAgent:
    """
    QA Agent for handling chat interactions.
    
    This agent is responsible for:
    1. Retrieving relevant context using RAG
    2. Building prompts with retrieved context
    3. Generating responses using LLM factory
    """

    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        enable_rag: bool = True,
        top_k: int = 4
    ):
        """
        Initialize QA Agent.
        
        Args:
            provider: AI provider (default uses OpenAI-compatible API)
            model_name: Model name
            temperature: Sampling temperature
            enable_rag: Whether to use RAG retrieval
            top_k: Number of top chunks to retrieve
        """
        try:
            self.llm_client = LLMFactory.create_client(
                provider=provider,
                model_name=model_name,
                temperature=temperature
            )
        except ValueError as e:
            logger.warning(f"LLM factory failed: {e}")
            self.llm_client = None

        self.enable_rag = enable_rag
        self.top_k = top_k
        self._knowledge_base = None
        self._retriever = None

    def _get_knowledge_base(self):
        """Get or initialize knowledge base"""
        if self._knowledge_base is None:
            self._knowledge_base = get_knowledge_base()
        return self._knowledge_base

    def _get_retriever(self) -> Optional[Retriever]:
        """Get or initialize retriever"""
        if not self.enable_rag:
            return None
        if self._retriever is None:
            kb = self._get_knowledge_base()
            self._retriever = Retriever(kb._store) if kb and kb._store else None
        return self._retriever

    def _retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for the query.

        Args:
            query: User's question

        Returns:
            List of retrieved chunks with metadata
        """
        if not self.enable_rag:
            return []

        kb = self._get_knowledge_base()
        if not kb:
            return []

        try:
            retrieval = kb.retrieve(query, top_k=self.top_k)
            chunks = retrieval.chunks
            if chunks:
                sources = [f"{chunk.source}#p{chunk.page}" for chunk in chunks]
                logger.info("RAG retrieved %s chunks for query '%s': %s", len(chunks), query, sources)
            else:
                logger.info("RAG retrieved 0 chunks for query '%s'", query)
            return [
                {
                    "content": chunk.content,
                    "source": chunk.source,
                    "page": chunk.page,
                    "chunk_id": chunk.chunk_id
                }
                for chunk in chunks
            ]
        except Exception as e:
            logger.error(f"Retrieval error: {e}")

            # 返回空列表，让主流程处理
            return []

    async def chat(
        self,
        query: str,
        use_rag: bool = True
    ) -> str:
        """
        Generate response for user query.

        Args:
            query: User's question
            use_rag: Whether to use RAG retrieval

        Returns:
            Generated response

        Raises:
            Exception: When LLM is not available or generation fails
        """
        if self.llm_client is None:
            raise Exception("LLM client is not initialized. Please check API configuration.")

        messages = self._build_messages(query, use_rag)
        response = await LLMFactory.agenerate(self.llm_client, messages)

        if not response or not response.strip():
            raise Exception("LLM returned empty response. Please try again.")

        return response

    def _build_messages(self, query: str, use_rag: bool = True) -> List[Any]:
        """
        Build message list for LLM.

        Args:
            query: User's question
            use_rag: Whether to include retrieved context

        Returns:
            List of LangChain messages
        """
        if use_rag:
            context_chunks = self._retrieve_context(query)
            if context_chunks:
                context = "\n\n".join([
                    f"[来源: {c['source']} 第{c['page']}页]\n{c['content']}"
                    for c in context_chunks
                ])
                return create_rag_prompt(query, context)

        return create_general_prompt(query)

    async def chat_with_history(
        self,
        query: str,
        history: List[Dict[str, str]],
        use_rag: bool = True
    ) -> str:
        """
        Chat with conversation history support.

        Args:
            query: Current user query
            history: Conversation history (list of messages with role and content)
            use_rag: Whether to use RAG retrieval

        Returns:
            Generated response

        Raises:
            Exception: When LLM is not available or generation fails
        """
        if self.llm_client is None:
            raise Exception("LLM client is not initialized. Please check API configuration.")

        messages = []

        if use_rag:
            context_chunks = self._retrieve_context(query)
            if context_chunks:
                context = "\n\n".join([
                    f"[来源: {c['source']} 第{c['page']}页\n{c['content']}"
                        for c in context_chunks
                    ])
                messages.append(HumanMessage(content=f"参考资料：\n{context}"))

        for msg in history[-10:]:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(SystemMessage(content=msg['content']))

        messages.append(HumanMessage(content=query))

        response = await LLMFactory.agenerate(self.llm_client, messages)

        if not response or not response.strip():
            raise Exception("LLM returned empty response. Please try again.")

        return response

    async def chat_stream(
        self,
        query: str,
        history: List[Dict[str, str]],
        use_rag: bool = True
    ):
        """
        Chat with conversation history support using streaming.

        Args:
            query: Current user query
            history: Conversation history (list of messages with role and content)
            use_rag: Whether to use RAG retrieval

        Yields:
            Chunks of generated response

        Raises:
            Exception: When LLM is not available or generation fails
        """
        if self.llm_client is None:
            raise Exception("LLM client is not initialized. Please check API configuration.")

        messages = []

        if use_rag:
            context_chunks = self._retrieve_context(query)
            if context_chunks:
                context = "\n\n".join([
                    f"[来源: {c['source']} 第{c['page']}页\n{c['content']}"
                        for c in context_chunks
                    ])
                messages.append(HumanMessage(content=f"参考资料：\n{context}"))

        for msg in history[-10:]:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(SystemMessage(content=msg['content']))

        messages.append(HumanMessage(content=query))

        # 使用流式生成
        async for chunk in LLMFactory.astream_generate(self.llm_client, messages):
            yield chunk
