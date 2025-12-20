"""
Travel Planner API Routes (v1)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.async import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_active_user
from app.modules.planner.schemas.plan_schema import ItineraryCreate, ItineraryUpdate, ItineraryResponse
from app.modules.planner.services.plan_service import PlanService

router = APIRouter()

@router.post("/generate", response_model=ItineraryResponse, status_code=status.HTTP_201_CREATED)
async def generate_itinerary(
    itinerary_data: ItineraryCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    plan_service = PlanService(db)
    itinerary = await plan_service.generate_itinerary(user_id=current_user.id, itinerary_data=itinerary_data)
    return itinerary

@router.get("/itineraries", response_model=list[ItineraryResponse])
async def get_my_itineraries(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    plan_service = PlanService(db)
    itineraries = await plan_service.get_user_itineraries(user_id=current_user.id, skip=skip, limit=limit)
    return itineraries

@router.get("/itineraries/{itinerary_id}", response_model=ItineraryResponse)
async def get_itinerary(
    itinerary_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    plan_service = PlanService(db)
    itinerary = await plan_service.get_itinerary(itinerary_id=itinerary_id, user_id=current_user.id)
    if not itinerary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")
    return itinerary

@router.put("/itineraries/{itinerary_id}", response_model=ItineraryResponse)
async def update_itinerary(
    itinerary_id: int,
    itinerary_data: ItineraryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    plan_service = PlanService(db)
    itinerary = await plan_service.update_itinerary(itinerary_id=itinerary_id, user_id=current_user.id, itinerary_data=itinerary_data)
    if not itinerary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")
    return itinerary

@router.delete("/itineraries/{itinerary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_itinerary(
    itinerary_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    plan_service = PlanService(db)
    success = await plan_service.delete_itinerary(itinerary_id=itinerary_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")
