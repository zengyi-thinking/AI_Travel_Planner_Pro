"""
Copywriting Prompt Templates
AI 文案生成的提示词模板
"""

from typing import List, Optional


class CopywritingPrompts:
    """文案生成提示词模板"""

    # 平台风格定义
    PLATFORM_STYLES = {
        "xiaohongshu": {
            "name": "小红书",
            "style": "活泼、真实、种草风、多用emoji、吸引眼球的标题、分点描述",
            "length": "150-250字",
            "format": "【吸引眼球的标题】\n\n正文内容，分点描述最佳\n\n#话题1 #话题2 #话题3",
            "tone": "亲切、分享感、推荐感"
        },
        "wechat": {
            "name": "朋友圈",
            "style": "温馨、个人化、简短精致、情感共鸣",
            "length": "80-150字",
            "format": "简短精致的一段话，可以emoji点缀",
            "tone": "真实、生活化、情感化"
        },
        "weibo": {
            "name": "微博",
            "style": "有趣、话题标签、互动性强、简洁有力",
            "length": "100-200字",
            "format": "引人入胜的开头 + 内容 + #话题标签",
            "tone": "轻松、幽默、互动性"
        }
    }

    # 情感风格定义
    EMOTION_STYLES = {
        "low": {
            "range": (0, 33),
            "name": "文艺忧郁",
            "keywords": "深沉、内敛、诗意、感性、静谧、治愈",
            "tone": "温柔、细腻、含蓄"
        },
        "medium": {
            "range": (34, 66),
            "name": "轻松幽默",
            "keywords": "轻松、自然、真实、幽默、日常、随性",
            "tone": "轻松、自然、不做作"
        },
        "high": {
            "range": (67, 100),
            "name": "热情澎湃",
            "keywords": "激情、活力、热情、兴奋、正能量、向上",
            "tone": "热情、洋溢、感染力"
        }
    }

    @classmethod
    def get_emotion_style(cls, level: int) -> dict:
        """根据情感级别获取风格"""
        if level < 34:
            return cls.EMOTION_STYLES["low"]
        elif level < 67:
            return cls.EMOTION_STYLES["medium"]
        else:
            return cls.EMOTION_STYLES["high"]

    @classmethod
    def generate_copywriting_prompt(
        cls,
        platform: str = "xiaohongshu",
        keywords: Optional[List[str]] = None,
        emotion_level: int = 50,
        image_description: Optional[str] = None
    ) -> str:
        """
        生成文案创建的提示词

        Args:
            platform: 目标平台
            keywords: 关键词列表
            emotion_level: 情感级别 (0-100)
            image_description: 图片描述（如果有）

        Returns:
            完整的提示词
        """
        platform_info = cls.PLATFORM_STYLES.get(platform, cls.PLATFORM_STYLES["xiaohongshu"])
        emotion_info = cls.get_emotion_style(emotion_level)

        # 构建关键词部分
        keywords_str = ""
        if keywords:
            keywords_str = f"关键词：{', '.join(keywords)}\n"

        # 构建图片描述部分
        image_str = ""
        if image_description:
            image_str = f"\n图片内容参考：{image_description}\n"

        prompt = f"""请为{platform_info['name']}平台生成一条旅行相关的社交媒体文案。

【基本要求】
- 风格：{platform_info['style']}
- 情感基调：{emotion_info['name']}（{emotion_info['tone']}）
- 文案长度：{platform_info['length']}
- 格式参考：{platform_info['format']}

【内容要素】
{keywords_str}{image_str}
【创作要点】
1. 标题要吸引人，用【】包围，能激发用户点击欲望
2. 正文内容要自然流畅，符合{emotion_info['name']}的风格
3. 使用相关的emoji点缀，增加生动性
4. 在文末添加2-4个相关话题标签（#）
5. 内容要有画面感，让读者能够感同身受
6. 避免空洞和套话，要真实有感染力

请直接输出文案内容，不要其他解释。"""

        return prompt

    @classmethod
    def generate_image_analysis_prompt(cls, for_keywords: bool = True) -> str:
        """
        生成图片分析的提示词

        Args:
            for_keywords: 是否为提取关键词（True）还是完整描述（False）

        Returns:
            图片分析的提示词
        """
        if for_keywords:
            return """请仔细分析这张图片，提取5-10个关键词用于生成旅行相关的社交媒体文案。

关键词类型包括：
1. 场景/地点（如：海滩、雪山、咖啡馆、古镇）
2. 情绪/氛围（如：浪漫、宁静、欢快、温馨、治愈）
3. 活动或动作（如：散步、拍照、美食、聚会）
4. 视觉元素（如：日落、蓝天、绿树、建筑）
5. 旅行相关（如：度假、探索、打卡、攻略）

请只返回关键词，用逗号分隔，不要其他内容。"""
        else:
            return """请详细描述这张图片的内容，包括：
1. 主要场景和地点
2. 画面中的主要元素（人物、物品、建筑等）
3. 色彩和光线
4. 整体氛围和感觉
5. 可能的故事背景

请用自然流畅的语言描述，80-150字。"""

    @classmethod
    def generate_regenerate_prompt(
        cls,
        platform: str = "xiaohongshu",
        previous_content: str = "",
        feedback: str = ""
    ) -> str:
        """
        生成重新创作的提示词

        Args:
            platform: 目标平台
            previous_content: 之前的文案内容
            feedback: 用户反馈或修改要求

        Returns:
            重新创作的提示词
        """
        platform_info = cls.PLATFORM_STYLES.get(platform, cls.PLATFORM_STYLES["xiaohongshu"])

        prompt = f"""请基于以下内容重新生成一条{platform_info['name']}文案。

【之前的文案】
{previous_content}

【修改要求】
{feedback if feedback else "请换一种表达方式，保持相同的主题和情感基调"}

【风格要求】
- 风格：{platform_info['style']}
- 文案长度：{platform_info['length']}

请直接输出新的文案内容，不要其他解释。"""

        return prompt
