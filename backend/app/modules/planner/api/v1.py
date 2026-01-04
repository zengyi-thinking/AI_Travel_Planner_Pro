"""
Travel Planner API Routes (v1)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_user
from app.modules.planner.schemas.plan_schema import PlanCreate, PlanUpdate, PlanResponse
from app.modules.planner.services.plan_service import PlanService

router = APIRouter()


class GenerateDetailRequest(BaseModel):
    use_strict_json: bool = Field(True, description="是否使用严格JSON格式")


class OptimizeRequest(BaseModel):
    feedback: str = Field(..., min_length=1, max_length=1000, description="用户反馈")
    affected_days: list[int] = Field(default_factory=list, description="需要优化的天数列表")
    use_strict_json: bool = Field(True, description="是否使用严格JSON格式")


@router.post("/generate", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_itinerary(
    itinerary_data: PlanCreate,
    use_strict_json: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建基础行程（仅信息，不含详细日程）"""
    plan_service = PlanService(db)
    itinerary = await plan_service.generate_itinerary(current_user.id, itinerary_data, use_strict_json)
    return itinerary


@router.post("/itineraries/{itinerary_id}/generate-detail", response_model=PlanResponse)
async def generate_detailed_itinerary(
    itinerary_id: int,
    request: GenerateDetailRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """生成详细行程（包含每日活动安排）"""
    plan_service = PlanService(db)
    itinerary = await plan_service.generate_detailed_itinerary(
        current_user.id, 
        itinerary_id, 
        request.use_strict_json
    )
    return itinerary


@router.post("/itineraries/{itinerary_id}/optimize", response_model=PlanResponse)
async def optimize_itinerary(
    itinerary_id: int,
    feedback: OptimizeRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """根据用户反馈优化行程"""
    plan_service = PlanService(db)
    itinerary = await plan_service.optimize_itinerary(
        current_user.id,
        itinerary_id,
        feedback.feedback,
        feedback.affected_days,
        feedback.use_strict_json
    )
    return itinerary


@router.get("/itineraries", response_model=list[PlanResponse])
async def get_my_itineraries(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    page: int = 1,
    size: int = 10
):
    """获取我的行程列表"""
    plan_service = PlanService(db)
    itineraries = await plan_service.get_user_itineraries(user_id=current_user.id, page=page, size=size)
    # 使用 mode='json' 来正确序列化 datetime 对象
    result = [itinerary.model_dump(mode='json') for itinerary in itineraries]
    return result


@router.get("/itineraries/{itinerary_id}", response_model=PlanResponse)
async def get_itinerary(
    itinerary_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取行程详情"""
    plan_service = PlanService(db)
    itinerary = await plan_service.get_itinerary(itinerary_id=itinerary_id, user_id=current_user.id)
    if not itinerary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")
    return itinerary


@router.put("/itineraries/{itinerary_id}", response_model=PlanResponse)
async def update_itinerary(
    itinerary_id: int,
    itinerary_data: PlanUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新行程基本信息"""
    plan_service = PlanService(db)
    itinerary = await plan_service.update_itinerary(itinerary_id=itinerary_id, user_id=current_user.id, itinerary_data=itinerary_data.model_dump(exclude_unset=True))
    if not itinerary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")
    return itinerary


@router.delete("/itineraries/{itinerary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_itinerary(
    itinerary_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除行程"""
    plan_service = PlanService(db)
    success = await plan_service.delete_itinerary(itinerary_id=itinerary_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")


@router.get("/itineraries/{itinerary_id}/export/pdf")
async def export_itinerary_pdf(
    itinerary_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """导出行程为 PDF"""
    from app.modules.planner.services.pdf_service_v2 import PDFExportServiceV2
    from fastapi.responses import Response
    from sqlalchemy import select
    from app.modules.planner.models.itinerary import Itinerary

    # Query database model directly to get metadata_json
    result = await db.execute(
        select(Itinerary)
        .where(Itinerary.id == itinerary_id)
        .where(Itinerary.user_id == current_user.id)
    )
    itinerary = result.scalar_one_or_none()

    if not itinerary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")

    # Get metadata from metadata_json
    metadata = itinerary.metadata_json or {}

    # Convert to dict for PDF service
    itinerary_dict = {
        "title": itinerary.title,
        "destination": itinerary.destination,
        "departure": itinerary.departure,
        "days": itinerary.days,
        "budget": float(itinerary.budget) if itinerary.budget else 0,
        "travel_style": itinerary.travel_style,
        "summary": metadata.get("summary", ""),
        "highlights": metadata.get("highlights", []),
        "best_season": metadata.get("best_season", ""),
        "weather": metadata.get("weather", ""),
        "actual_cost": metadata.get("actual_cost", 0),
        "cost_breakdown": metadata.get("cost_breakdown", {}),
        "days_detail": [
            {
                "day_number": day.day_number,
                "title": day.title,
                "date": day.date,
                "summary": "",
                "activities": day.activities if day.activities else [],
                "total_cost": 0,
            }
            for day in itinerary.days_detail
        ],
        "preparation": metadata.get("preparation", {}),
        "tips": metadata.get("tips", {}),
    }

    # Generate PDF
    pdf_service = PDFExportServiceV2()
    pdf_bytes = pdf_service.generate_itinerary_pdf(itinerary_dict)

    # Return PDF file
    # URL encode filename to support Chinese characters
    from urllib.parse import quote
    filename = f"{itinerary.title}.pdf"
    encoded_filename = quote(filename, safe='')

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )
