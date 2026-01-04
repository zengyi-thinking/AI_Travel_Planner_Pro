"""
Copywriter Content Service
集成视觉识别和 AI 文案生成
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.copywriter.daos.content_dao import ContentDAO
from app.modules.copywriter.models.content import Content
from app.modules.copywriter.schemas.content_schema import ContentCreate
from app.modules.copywriter.services.vision_service import VisionService
from app.modules.copywriter.prompts.templates import CopywritingPrompts
from app.core.config import settings
import anthropic
import logging

logger = logging.getLogger(__name__)


class ContentService:
    """文案生成服务 - 集成视觉识别和 AI 生成"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.content_dao = ContentDAO(db)
        self.vision_service = VisionService()

        # 初始化 Anthropic 客户端（用于纯文本文案生成）
        self.anthropic_api_key = getattr(settings, 'ANTHROPIC_AUTH_TOKEN', None)
        self.anthropic_model = getattr(settings, 'ANTHROPIC_MODEL', 'MiniMax-M2.1')

        if self.anthropic_api_key:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
                logger.info("Anthropic client initialized for copywriting")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
                self.anthropic_client = None
        else:
            self.anthropic_client = None

    async def generate_content(self, user_id: int, payload: ContentCreate) -> Content:
        platform = payload.platform or "xiaohongshu"
        keywords = payload.keywords or []
        emotion_level = payload.emotion_level or 50
        images = payload.images or []

        output_content = ""
        image_description = None

        # 步骤 1: 如果有图片，先分析图片获取描述和关键词
        if images:
            logger.info(f"Analyzing {len(images)} image(s)...")
            image_url = images[0]
            image_base64 = None
            
            # 将本地图片转为 base64（因为视觉 API 无法访问 localhost）
            if image_url.startswith("http://localhost") or image_url.startswith("/static/"):
                import os
                import base64
                # 从 URL 提取文件路径
                if "/static/uploads/" in image_url:
                    file_path = image_url.split("/static/uploads/")[-1]
                    full_path = os.path.join("static/uploads", file_path)
                    if os.path.exists(full_path):
                        with open(full_path, "rb") as f:
                            image_base64 = base64.b64encode(f.read()).decode("utf-8")
                            logger.info(f"Image converted to base64: {len(image_base64)} chars")

            # 获取图片描述
            analysis_result = await self.vision_service.analyze_image(
                image_base64=image_base64,
                prompt=CopywritingPrompts.generate_image_analysis_prompt(for_keywords=False)
            )

            if analysis_result["success"]:
                image_description = analysis_result["description"]
                logger.info(f"Image description: {image_description[:100]}...")

            # 从图片提取关键词
            extracted_keywords = await self.vision_service.extract_keywords_from_image(
                image_base64=image_base64
            )
            if extracted_keywords:
                keywords = list(set(keywords + extracted_keywords))
                logger.info(f"Combined keywords: {keywords}")

        # 步骤 2: 生成文案
        if images:
            logger.info("Generating copywriting with vision API...")
            output_content = await self.vision_service.generate_copywriting_from_image(
                image_base64=image_base64,
                platform=platform,
                emotion_level=emotion_level,
                additional_keywords=keywords if keywords else None
            )
        else:
            logger.info("Generating copywriting with Anthropic API...")
            output_content = await self._generate_with_anthropic(
                platform=platform,
                keywords=keywords,
                emotion_level=emotion_level,
                image_description=image_description
            )

        # 步骤 3: 保存到数据库
        content = Content(
            user_id=user_id,
            content_type="copywriting",
            platform=platform,
            output_content=output_content,
            input_data={
                "keywords": keywords,
                "emotion_level": emotion_level,
                "images": images,
                "image_description": image_description
            },
        )
        return await self.content_dao.create(content)

    async def _generate_with_anthropic(self, platform: str, keywords: List[str], emotion_level: int, image_description: Optional[str] = None) -> str:
        if not self.anthropic_client:
            return self._generate_fallback_content(platform, keywords)

        try:
            prompt = CopywritingPrompts.generate_copywriting_prompt(
                platform=platform,
                keywords=keywords,
                emotion_level=emotion_level,
                image_description=image_description
            )

            response = self.anthropic_client.messages.create(
                model=self.anthropic_model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.content[0].text
            logger.info(f"Anthropic generated {len(output)} chars")
            return output

        except Exception as e:
            logger.error(f"Anthropic API failed: {e}")
            return self._generate_fallback_content(platform, keywords)

    def _generate_fallback_content(self, platform: str, keywords: List[str]) -> str:
        keywords_str = "、".join(keywords) if keywords else "旅行"

        if platform == "xiaohongshu":
            return f"""【{keywords_str}的美好时光✨】

发现生活的美好，分享旅途的精彩🌟

今天感受到了{keywords_str}的魅力，每一处风景都让人心驰神往💕

✨ 推荐理由：
· 风景绝美，随手一拍都是大片
· 氛围超棒，让人流连忘返
· 适合放松心情，远离喧嚣

📍地点：{keywords_str}
📝tips：记得提前做好攻略哦~

#{keywords_str} #旅行 #美好时光 #生活记录"""

        elif platform == "wechat":
            return f"""{keywords_str}的美好时光✨

在旅途中发现不一样的风景，感受生活的美好。

每一处风景都值得记录，每一刻都值得珍藏💕

#{keywords_str} #旅行"""

        else:
            return f"""【{keywords_str}之旅】

被今天的风景美到了！{keywords_str}真的太治愈了🌟

强烈推荐给大家，绝对值得一看！

#{keywords_str} #旅行推荐 #美好生活"""

    async def list_contents(self, user_id: int, page: int, size: int) -> List[Content]:
        return await self.content_dao.list_by_user(user_id, page, size)

    async def rate_content(self, user_id: int, content_id: int, rating: int) -> Optional[Content]:
        content = await self.content_dao.get_by_id(content_id, user_id)
        if not content:
            return None
        return await self.content_dao.update(content, rating=rating)

    async def regenerate_content(self, user_id: int, content_id: int, feedback: str = "") -> Optional[Content]:
        original_content = await self.content_dao.get_by_id(content_id, user_id)
        if not original_content:
            return None

        platform = original_content.platform or "xiaohongshu"
        input_data = original_content.input_data or {}
        keywords = input_data.get("keywords", [])
        emotion_level = input_data.get("emotion_level", 50)
        images = input_data.get("images", [])

        new_payload = ContentCreate(
            platform=platform,
            keywords=keywords,
            emotion_level=emotion_level,
            images=images
        )

        return await self.generate_content(user_id, new_payload)
