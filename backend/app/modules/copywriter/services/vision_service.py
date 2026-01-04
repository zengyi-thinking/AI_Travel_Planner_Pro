"""
Vision API Service
使用 OpenAI 兼容的视觉识别 API (Qwen2.5-VL-72B-Instruct)
"""

import os
import base64
from typing import List, Optional, Dict, Any
from openai import OpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class VisionService:
    """视觉识别服务 - 用于识别图片内容"""

    def __init__(self):
        """初始化视觉 API 客户端"""
        self.api_key = getattr(settings, 'VISION_API_KEY', os.getenv('VISION_API_KEY'))
        self.base_url = getattr(settings, 'VISION_API_BASE_URL', os.getenv('VISION_API_BASE_URL'))
        self.model = getattr(settings, 'VISION_MODEL', os.getenv('VISION_MODEL', 'Qwen2.5-VL-72B-Instruct'))

        if not self.api_key or not self.base_url:
            logger.warning("Vision API credentials not configured")

        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info(f"Vision API client initialized: {self.base_url}")
        except Exception as e:
            logger.error(f"Failed to initialize Vision API client: {e}")
            self.client = None

    async def analyze_image(
        self,
        image_url: Optional[str] = None,
        image_base64: Optional[str] = None,
        prompt: str = "请详细描述这张图片中的内容，包括场景、人物、物品、颜色、氛围等。"
    ) -> Dict[str, Any]:
        """
        分析图片内容

        Args:
            image_url: 图片 URL (可选)
            image_base64: Base64 编码的图片 (可选)
            prompt: 分析提示词

        Returns:
            包含分析结果的字典
        """
        if not self.client:
            return {
                "success": False,
                "error": "Vision API client not initialized",
                "description": None
            }

        try:
            # 构建消息内容
            content = [{"type": "text", "text": prompt}]

            # 添加图片
            if image_url:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_url}
                })
            elif image_base64:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                })
            else:
                return {
                    "success": False,
                    "error": "No image provided",
                    "description": None
                }

            # 调用 API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": content}]
            )

            description = response.choices[0].message.content

            logger.info(f"Image analysis successful: {len(description)} chars")
            return {
                "success": True,
                "description": description,
                "raw_response": response.model_dump()
            }

        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "description": None
            }

    async def extract_keywords_from_image(
        self,
        image_url: Optional[str] = None,
        image_base64: Optional[str] = None
    ) -> List[str]:
        """
        从图片中提取关键词，用于文案生成

        Args:
            image_url: 图片 URL
            image_base64: Base64 编码的图片

        Returns:
            关键词列表
        """
        prompt = """请分析这张图片，提取 5-10 个关键词，用于生成社交媒体文案。
关键词应该包括：
1. 场景/地点（如：海滩、山脉、城市、咖啡馆）
2. 情绪/氛围（如：浪漫、宁静、欢快、温馨）
3. 活动或动作（如：散步、拍照、聚会）
4. 视觉元素（如：日落、蓝天、美食）

请只返回关键词，用逗号分隔，不要其他内容。"""

        result = await self.analyze_image(image_url, image_base64, prompt)

        if result["success"] and result["description"]:
            # 解析关键词
            keywords_text = result["description"].strip()
            keywords = [k.strip() for k in keywords_text.split(",") if k.strip()]
            logger.info(f"Extracted keywords: {keywords}")
            return keywords

        return []

    async def analyze_images(
        self,
        images_base64: Optional[List[str]] = None,
        prompt: str = "请详细描述这些图片中的内容。"
    ) -> Dict[str, Any]:
        """
        分析多张图片内容

        Args:
            images_base64: 多张图片的 Base64 编码列表
            prompt: 分析提示词

        Returns:
            包含分析结果的字典
        """
        if not self.client:
            return {
                "success": False,
                "error": "Vision API client not initialized",
                "description": None
            }

        if not images_base64 or len(images_base64) == 0:
            return {
                "success": False,
                "error": "No images provided",
                "description": None
            }

        try:
            # 构建消息内容：文本提示 + 所有图片
            content = [{"type": "text", "text": prompt}]

            # 添加所有图片
            for img_b64 in images_base64:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                })

            # 调用 API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": content}]
            )

            description = response.choices[0].message.content

            logger.info(f"Multi-image analysis successful: {len(description)} chars from {len(images_base64)} images")
            return {
                "success": True,
                "description": description,
                "raw_response": response.model_dump()
            }

        except Exception as e:
            logger.error(f"Multi-image analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "description": None
            }


    async def generate_copywriting_from_image(
        self,
        image_url: Optional[str] = None,
        image_base64: Optional[str] = None,
        images_base64: Optional[List[str]] = None,
        platform: str = "xiaohongshu",
        emotion_level: int = 50,
        additional_keywords: Optional[List[str]] = None
    ) -> str:
        """
        基于图片生成社交媒体文案（支持多张图片）

        Args:
            image_url: 单张图片 URL（向后兼容）
            image_base64: 单张图片 Base64（向后兼容）
            images_base64: 多张图片 Base64 列表
            platform: 目标平台 (xiaohongshu/wechat/weibo)
            emotion_level: 情感基调 (0-100)
            additional_keywords: 额外的关键词

        Returns:
            生成的文案内容
        """
        # 处理图片列表：优先使用 images_base64，否则将单个 image_base64 转为列表
        if images_base64 is None and image_base64:
            images_base64 = [image_base64]
        
        # 确定情感风格
        if emotion_level < 33:
            emotion_style = "文艺忧郁、内敛深沉"
        elif emotion_level < 66:
            emotion_style = "轻松幽默、自然真实"
        else:
            emotion_style = "热情澎湃、活力满满"

        # 平台风格
        platform_styles = {
            "xiaohongshu": "小红书风格：活泼、真实、多用emoji、吸引眼球的标题、分点描述",
            "wechat": "朋友圈风格：温馨、个人化、简短精致、情感共鸣",
            "weibo": "微博风格：有趣、话题标签、互动性强、简洁有力"
        }

        style_desc = platform_styles.get(platform, platform_styles["xiaohongshu"])

        # 构建提示词
        additional_kw_str = f"，额外关键词：{', '.join(additional_keywords)}" if additional_keywords else ""
        image_count_str = f"{len(images_base64)}张" if images_base64 else ""
        prompt = f"""请根据这{image_count_str}图片，为{platform}平台生成一条旅行相关的社交媒体文案。

要求：
1. 风格：{style_desc}
2. 情感基调：{emotion_style}
3. 文案长度：100-200字
4. 包含：吸引人的标题（用【】包围）+ 正文 + 相关emoji
5. 如果适用，在文末添加2-3个相关话题标签（用 #）
6. 内容要基于图片中的实际场景和元素{additional_kw_str}

请直接输出文案，不要其他解释。"""

        # 使用多图分析
        result = await self.analyze_images(
            images_base64=images_base64,
            prompt=prompt
        )

        if result["success"] and result["description"]:
            return result["description"]

        # 降级方案：返回通用文案
        return f"""【旅行日记】今天的美景让人心旷神怡✨

分享这份美好，感受旅途中的每一个瞬间。{additional_kw_str}

#旅行 #美景"""

    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        将本地图片文件编码为 Base64

        Args:
            image_path: 图片文件路径

        Returns:
            Base64 编码的字符串（不含 data URI 前缀）
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to encode image: {e}")
            return None

