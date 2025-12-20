"""
Plan Service

This module contains business logic for travel planning.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.planner.daos.plan_dao import PlanDAO
from app.modules.planner.schemas.plan_schema import PlanCreate, PlanUpdate, PlanResponse
from app.common.exceptions.base import NotFoundException
from typing import List

import logging

logger = logging.getLogger(__name__)


class PlanService:
    """
    Service class for travel plan business logic.
    """

    def __init__(self, db_session: AsyncSession):
        self.plan_dao = PlanDAO(db_session)

    async def generate_plan(
        self,
        user_id: int,
        plan_data: PlanCreate
    ) -> PlanResponse:
        """
        Generate AI-powered travel plan.
        """
        # TODO: Implement AI plan generation
        # This will use the PlannerAgent to generate a plan
        pass

    async def get_user_plans(
        self,
        user_id: int,
        page: int,
        size: int
    ) -> List[PlanResponse]:
        """
        Get user's travel plans.
        """
        plans = await self.plan_dao.get_user_plans(user_id, page, size)
        return [PlanResponse.from_orm(plan) for plan in plans]

    async def get_plan_by_id(self, plan_id: int, user_id: int) -> PlanResponse | None:
        """
        Get plan by ID.
        """
        plan = await self.plan_dao.get_plan_by_id(plan_id, user_id)
        if not plan:
            raise NotFoundException("Plan not found")
        return PlanResponse.from_orm(plan)

    async def update_plan(
        self,
        plan_id: int,
        user_id: int,
        plan_data: PlanUpdate
    ) -> PlanResponse:
        """
        Update travel plan.
        """
        plan = await self.plan_dao.update_plan(plan_id, user_id, plan_data.dict(exclude_unset=True))
        return PlanResponse.from_orm(plan)

    async def delete_plan(self, plan_id: int, user_id: int) -> None:
        """
        Delete travel plan.
        """
        await self.plan_dao.delete_plan(plan_id, user_id)
