"""
QA prompt templates.
"""

def create_rag_prompt(query: str, context: str):
    """
    Create RAG prompt with context.

    Args:
        query: User's question
        context: Retrieved context from knowledge base

    Returns:
        List of messages (SystemMessage and HumanMessage)
    """
    from langchain_core.messages import SystemMessage, HumanMessage

    user_content = f"""
参考资料：
{context}

用户问题：{query}
    """.strip()

    return [
        HumanMessage(content=user_content)
    ]

def create_general_prompt(query: str):
    """
    Create general prompt without RAG context.

    Args:
        query: User's question

    Returns:
        List of messages (HumanMessage only)
    """
    from langchain_core.messages import HumanMessage

    return [
        HumanMessage(content=query)
    ]

def create_weather_prompt(city: str):
    """
    Create weather query prompt.

    Args:
        city: City name

    Returns:
        Formatted prompt string
    """
    return f"请查询{city}的天气预报，包括未来3天的天气状况、温度、湿度等信息。"
