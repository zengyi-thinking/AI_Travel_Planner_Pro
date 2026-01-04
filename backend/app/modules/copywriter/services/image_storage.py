"""
Image Storage Service
处理图片上传和存储
"""

import os
import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path
from fastapi import UploadFile
import aiofiles
import logging

logger = logging.getLogger(__name__)


class ImageStorageService:
    """本地图片存储服务"""

    def __init__(self, upload_dir: Optional[str] = None):
        """
        初始化图片存储服务

        Args:
            upload_dir: 上传目录路径，默认为 backend/static/uploads
        """
        # 默认上传目录
        if upload_dir is None:
            # backend 目录的绝对路径
            backend_dir = Path(__file__).parent.parent.parent.parent.parent
            upload_dir = backend_dir / "static" / "uploads"

        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        # 创建按日期分类的子目录
        today = datetime.now().strftime("%Y%m%d")
        self.today_dir = self.upload_dir / today
        self.today_dir.mkdir(exist_ok=True)

        logger.info(f"Image storage initialized: {self.upload_dir}")

    def get_public_url(self, filename: str) -> str:
        """
        获取图片的公开访问 URL

        Args:
            filename: 文件名

        Returns:
            公开访问的 URL
        """
        today = datetime.now().strftime("%Y%m%d")
        return f"/static/uploads/{today}/{filename}"

    async def save_upload_file(self, file: UploadFile) -> tuple[str, str]:
        """
        保存上传的文件

        Args:
            file: FastAPI UploadFile 对象

        Returns:
            (filename, public_url) 元组
        """
        # 生成唯一文件名
        file_extension = Path(file.filename).suffix or ".jpg"
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = self.today_dir / unique_filename

        try:
            # 异步保存文件
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)

            logger.info(f"File saved: {file_path} ({len(content)} bytes)")

            public_url = self.get_public_url(unique_filename)
            return unique_filename, public_url

        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise

    async def save_base64_image(self, base64_data: str, extension: str = ".jpg") -> tuple[str, str]:
        """
        保存 Base64 编码的图片

        Args:
            base64_data: Base64 编码的图片数据（不含 data URI 前缀）
            extension: 文件扩展名

        Returns:
            (filename, public_url) 元组
        """
        import base64

        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}{extension}"
        file_path = self.today_dir / unique_filename

        try:
            # 解码 Base64 并保存
            image_data = base64.b64decode(base64_data)
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(image_data)

            logger.info(f"Base64 image saved: {file_path} ({len(image_data)} bytes)")

            public_url = self.get_public_url(unique_filename)
            return unique_filename, public_url

        except Exception as e:
            logger.error(f"Failed to save base64 image: {e}")
            raise

    def delete_file(self, filename: str) -> bool:
        """
        删除文件

        Args:
            filename: 文件名

        Returns:
            是否删除成功
        """
        try:
            # 尝试从今天的目录删除
            file_path = self.today_dir / filename
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True

            # 尝试从上传目录的子目录中查找
            for subdir in self.upload_dir.iterdir():
                if subdir.is_dir():
                    file_path = subdir / filename
                    if file_path.exists():
                        file_path.unlink()
                        logger.info(f"File deleted: {file_path}")
                        return True

            logger.warning(f"File not found: {filename}")
            return False

        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False

    def get_file_path(self, filename: str) -> Optional[Path]:
        """
        获取文件的完整路径

        Args:
            filename: 文件名

        Returns:
            文件的完整路径，如果不存在则返回 None
        """
        # 先检查今天的目录
        file_path = self.today_dir / filename
        if file_path.exists():
            return file_path

        # 搜索所有子目录
        for subdir in self.upload_dir.iterdir():
            if subdir.is_dir():
                file_path = subdir / filename
                if file_path.exists():
                    return file_path

        return None
