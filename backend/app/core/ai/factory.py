"""
LLM Factory

This module provides a factory pattern for creating different LLM clients.
It supports multiple AI providers (OpenAI, Spark, GLM, etc.) through a unified interface.
"""

from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from app.core.config.settings import settings
import logging
import httpx

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
        Create an LLM client based on provider.

        Args:
            provider: AI provider name (openai, glm, anthropic, etc.)
            model_name: Model name (uses default if not provided)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model parameters

        Returns:
            Configured LLM client

        Raises:
            ValueError: If provider is not supported
        """
        provider = provider.lower()

        if provider in ["openai", "glm", "anthropic", "minimax"]:
            # 选择正确的模型名称
            if provider in ["glm", "anthropic"]:
                # GLM 默认使用 glm-4.7
                selected_model = model_name or "glm-4.7"
            elif provider == "minimax":
                # MiniMax 默认使用 settings.ANTHROPIC_MODEL
                selected_model = model_name or settings.ANTHROPIC_MODEL or "MiniMax-M2.1"
            else:
                selected_model = model_name or settings.OPENAI_MODEL_NAME

            return LLMFactory._create_openai_client(
                provider=provider,
                model_name=selected_model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    @staticmethod
    def _create_openai_client(
        provider: str = "openai",
        model_name: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatOpenAI:
        """Create OpenAI-compatible client (supports OpenAI, GLM, etc.)"""

        # 根据 provider 选择正确的配置
        if provider in ["glm", "anthropic"]:
            # 使用 ANTHROPIC 配置 (GLM-4.7)
            api_key = settings.ANTHROPIC_AUTH_TOKEN

            if not api_key:
                raise ValueError("ANTHROPIC_AUTH_TOKEN is not configured for GLM")

            # 智谱 GLM-4.7 使用新的端点 (Anthropic 兼容格式)
            return ChatOpenAI(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens or settings.AI_MAX_TOKENS,
                base_url="https://open.bigmodel.cn/api/anthropic/v1/messages",
                **kwargs
            )

        elif provider == "minimax":
            # 使用 MiniMax 配置
            api_key = settings.ANTHROPIC_AUTH_TOKEN

            if not api_key:
                raise ValueError("ANTHROPIC_AUTH_TOKEN is not configured for MiniMax")

            # MiniMax 使用 OpenAI 兼容格式
            base_url = getattr(settings, 'MINIMAX_BASE_URL', None) or settings.ANTHROPIC_BASE_URL
            if not base_url:
                base_url = "https://api.minimax.chat/v1/chat/completions"

            return ChatOpenAI(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens or settings.AI_MAX_TOKENS,
                base_url=base_url,
                **kwargs
            )

        else:
            # 使用 OpenAI 配置
            api_key = settings.OPENAI_API_KEY
            base_url = settings.OPENAI_BASE_URL

            if not api_key:
                raise ValueError("OPENAI_API_KEY is not configured")

            return ChatOpenAI(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens or settings.AI_MAX_TOKENS,
                base_url=base_url,
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
            # 检查是否是智谱 API（通过检查 openai_api_base）
            openai_api_base = getattr(client, 'openai_api_base', None)

            if openai_api_base and 'open.bigmodel.cn/api/anthropic' in openai_api_base:
                # 使用智谱 API 的 Anthropic 兼容格式
                return await LLMFactory._generate_with_glm_anthropic(messages, client)

            if openai_api_base and 'minimaxi.com/anthropic' in openai_api_base:
                # 使用 MiniMax API 的 Anthropic 兼容格式
                return await LLMFactory._generate_with_minimax_anthropic(messages, client)

            # 默认使用 LangChain 的调用
            response = await client.ainvoke(messages, **kwargs)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            raise

    @staticmethod
    async def _generate_with_glm_anthropic(messages: list[BaseMessage], client: ChatOpenAI) -> str:
        """使用智谱 Anthropic 兼容格式生成响应"""
        # 获取 API key（处理 SecretStr 类型）
        api_key = client.openai_api_key
        if hasattr(api_key, 'get_secret_value'):
            api_key = api_key.get_secret_value()

        # 转换消息格式
        api_messages = []
        system_message = None

        for msg in messages:
            # 获取消息类型
            msg_type = msg.type if hasattr(msg, 'type') else msg.__class__.__name__.lower().replace('message', '')
            content = msg.content

            # 智谱 API 不支持 system 消息，需要提取系统提示
            if msg_type == 'system':
                system_message = content
                continue

            # 转换消息类型：human -> user
            if msg_type == 'human':
                role = 'user'
            elif msg_type == 'ai':
                role = 'assistant'
            else:
                role = msg_type

            # 处理不同类型的消息内容
            if isinstance(content, str):
                api_messages.append({'role': role, 'content': content})
            elif isinstance(content, list):
                # 处理多模态内容
                for item in content:
                    if isinstance(item, dict):
                        api_messages.append({'role': role, 'content': item})
                    else:
                        api_messages.append({'role': role, 'content': str(item)})

        # 如果有系统消息，添加到第一条用户消息中
        if system_message and api_messages:
            api_messages[0]['content'] = f"{system_message}\n\n{api_messages[0]['content']}"

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }

        payload = {
            'model': client.model_name,
            'max_tokens': getattr(client, 'max_tokens', 1000),
            'messages': api_messages
        }

        timeout = settings.API_TIMEOUT_MS / 1000 if settings.API_TIMEOUT_MS else 60
        async with httpx.AsyncClient(timeout=timeout) as http_client:
            response = await http_client.post(
                "https://open.bigmodel.cn/api/anthropic/v1/messages",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                # 处理 Anthropic 格式的响应
                content_list = data.get('content', [])
                text_content = []
                for item in content_list:
                    if item.get('type') == 'text':
                        text_content.append(item.get('text', ''))
                return ''.join(text_content)
            else:
                error_msg = response.text
                raise Exception(f"GLM API error ({response.status_code}): {error_msg}")

    @staticmethod
    async def _generate_with_minimax_anthropic(messages: list[BaseMessage], client: ChatOpenAI) -> str:
        """使用MiniMax Anthropic兼容格式生成响应"""
        # 获取 API key（处理 SecretStr 类型）
        api_key = client.openai_api_key
        if hasattr(api_key, 'get_secret_value'):
            api_key = api_key.get_secret_value()

        # 转换消息格式
        api_messages = []

        for msg in messages:
            # 获取消息类型
            msg_type = msg.type if hasattr(msg, 'type') else msg.__class__.__name__.lower().replace('message', '')
            content = msg.content

            # MiniMax Anthropic 不支持 system 消息，需要提取系统提示
            if msg_type == 'system':
                # 可以添加到第一条用户消息中
                continue

            # 转换消息类型：human -> user
            if msg_type == 'human':
                role = 'user'
            elif msg_type == 'ai':
                role = 'assistant'
            else:
                role = msg_type

            # 处理不同类型的消息内容
            if isinstance(content, str):
                api_messages.append({'role': role, 'content': content})
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        api_messages.append({'role': role, 'content': item})
                    else:
                        api_messages.append({'role': role, 'content': str(item)})

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }

        payload = {
            'model': client.model_name,
            'max_tokens': getattr(client, 'max_tokens', 1000),
            'messages': api_messages
        }

        # 获取base_url
        base_url = getattr(client, 'openai_api_base', None)
        if base_url and '/anthropic/v1/messages' not in base_url:
            if base_url.endswith('/anthropic'):
                base_url = base_url + '/v1/messages'
            else:
                base_url = base_url + '/anthropic/v1/messages'

        timeout = settings.API_TIMEOUT_MS / 1000 if settings.API_TIMEOUT_MS else 60
        async with httpx.AsyncClient(timeout=timeout) as http_client:
            response = await http_client.post(
                base_url,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                # 处理 MiniMax Anthropic 格式的响应
                # MiniMax 返回的 content 数组可能包含 thinking 和 text 类型
                # 我们需要提取所有 text 类型的内容
                content_list = data.get('content', [])
                text_content = []
                for item in content_list:
                    if item.get('type') == 'text':
                        text_content.append(item.get('text', ''))
                    # 忽略 thinking 类型的内容
                if text_content:
                    return ''.join(text_content)
                else:
                    # 如果没有text类型，检查是否有其他类型
                    logger.warning(f"MiniMax API response has no text content: {data.keys()}")
                    return ""
            else:
                error_msg = response.text
                raise Exception(f"MiniMax API error ({response.status_code}): {error_msg}")
