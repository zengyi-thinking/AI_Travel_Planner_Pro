"""
LLM Factory

This module provides a factory pattern for creating different LLM clients.
It supports multiple AI providers (OpenAI, Spark, GLM, etc.) through a unified interface.
"""

from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class LLMFactory:
    """
    Factory class for creating LLM clients.
    Supports multiple AI providers with a unified interface.
    """

    @staticmethod
    def create_client(
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatOpenAI:
        """
        Create an LLM client based on the provider.

        Args:
            provider: AI provider name (openai, spark, glm, etc.)
            model_name: Model name (uses default if not provided)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model parameters

        Returns:
            Configured LLM client

        Raises:
            ValueError: If provider is not supported
        """
        if provider.lower() == "openai":
            return LLMFactory._create_openai_client(
                model_name or settings.OPENAI_MODEL_NAME,
                temperature,
                max_tokens,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    @staticmethod
    def _create_openai_client(
        model_name: str,
        temperature: float,
        max_tokens: Optional[int],
        **kwargs
    ) -> ChatOpenAI:
        """Create OpenAI client"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")

        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens or settings.AI_MAX_TOKENS,
            base_url=settings.OPENAI_BASE_URL,
            **kwargs
        )

    @staticmethod
    async def agenerate(
        client: ChatOpenAI,
        messages: list[BaseMessage],
        **kwargs
    ) -> str:
        """
        Asynchronously generate response from LLM.

        Args:
            client: Configured LLM client
            messages: List of chat messages
            **kwargs: Additional generation parameters

        Returns:
            Generated text response
        """
        try:
            response = await client.ainvoke(messages, **kwargs)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            raise
