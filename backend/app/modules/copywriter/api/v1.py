"""
Copywriter Module API Routes (v1)
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_active_user
from app.modules.copywriter.schemas.content_schema import ContentCreate, ContentResponse, ContentRating
from app.modules.copywriter.services.content_service import ContentService
from app.modules.copywriter.services.image_storage import ImageStorageService
from app.modules.users.services.quota_service import QuotaService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# 初始化图片存储服务
image_storage = ImageStorageService()


@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    content_data: ContentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    # 检查配额
    quota_service = QuotaService(db)
    await quota_service.check_and_increment_copywriter_quota(current_user.id)
    
    service = ContentService(db)
    content = await service.generate_content(current_user.id, content_data)
    return ContentResponse.model_validate(content)


@router.get("/contents", response_model=list[ContentResponse])
async def get_my_contents(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),
    page: int = 1,
    size: int = 20
):
    service = ContentService(db)
    contents = await service.list_contents(current_user.id, page=page, size=size)
    return [ContentResponse.model_validate(item) for item in contents]


@router.post("/contents/{content_id}/rate", response_model=ContentResponse)
async def rate_content(
    content_id: int,
    payload: ContentRating,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ContentService(db)
    content = await service.rate_content(current_user.id, content_id, payload.rating)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return ContentResponse.model_validate(content)


@router.post("/upload-image")
async def upload_image(
    request: Request,
    image: UploadFile = File(...),
    current_user = Depends(get_current_active_user)
):
    """上传图片并返回访问 URL"""
    try:
        # 验证文件类型
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        file_ext = "." + image.filename.split(".")[-1].lower() if "." in image.filename else ""

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )

        # 保存文件
        filename, public_url = await image_storage.save_upload_file(image)

        logger.info(f"Image uploaded: {filename} by user {current_user.id}")

        # 动态获取当前请求的基础URL，避免硬编码
        base_url = str(request.base_url).rstrip("/")

        return {
            "image_url": f"{base_url}{public_url}",
            "filename": filename,
            "public_url": public_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image"
        )
