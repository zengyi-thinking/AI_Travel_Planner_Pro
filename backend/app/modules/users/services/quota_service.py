"""
Quota Management Service

This module handles usage quota checking and management for free and pro users.
"""

from datetime import date, datetime
from typing import Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.daos.user_dao import UserDAO
from app.modules.users.models.user import User
from app.common.exceptions.base import QuotaExceededException, NotFoundException
import logging

logger = logging.getLogger(__name__)


class QuotaService:
    """配额管理服务"""

    # 配额常量
    FREE_PLAN_LIMIT = 100  # 免费用户每月 100 次行程生成
    PRO_PLAN_LIMIT = -1  # Pro 用户无限次（-1 表示无限制）

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_dao = UserDAO(db)

    async def check_and_increment_plan_quota(self, user_id: int) -> User:
        """
        检查并增加行程生成配额

        Args:
            user_id: 用户 ID

        Returns:
            更新后的用户对象

        Raises:
            QuotaExceededException: 配额已用尽
        """
        user = await self.user_dao.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        # 检查是否需要重置配额（每月重置）
        await self._reset_quota_if_needed(user)

        # Pro 用户无限制
        if user.membership_level == 'pro':
            logger.info(f"Pro user {user_id} generating plan (no limit)")
            await self._increment_usage(user, 'plan')
            return user

        # 检查免费用户配额
        if user.plan_usage_count >= self.FREE_PLAN_LIMIT:
            logger.warning(f"User {user_id} exceeded plan quota ({user.plan_usage_count}/{self.FREE_PLAN_LIMIT})")
            raise QuotaExceededException(
                message=f"已达到免费计划配额上限（{self.FREE_PLAN_LIMIT} 次/月）",
                usage=user.plan_usage_count,
                limit=self.FREE_PLAN_LIMIT,
                quota_type="plan"
            )

        # 增加使用次数
        await self._increment_usage(user, 'plan')
        logger.info(f"User {user_id} plan quota: {user.plan_usage_count + 1}/{self.FREE_PLAN_LIMIT}")

        return user

    async def check_and_increment_copywriter_quota(self, user_id: int) -> User:
        """
        检查并增加文案生成配额

        Args:
            user_id: 用户 ID

        Returns:
            更新后的用户对象

        Raises:
            QuotaExceededException: 配额已用尽
        """
        user = await self.user_dao.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        # 检查是否需要重置配额（每月重置）
        await self._reset_quota_if_needed(user)

        # Pro 用户无限制
        if user.membership_level == 'pro':
            logger.info(f"Pro user {user_id} generating copywriting (no limit)")
            await self._increment_usage(user, 'copywriter')
            return user

        # 文案生成配额暂时和行程生成共享（或者可以单独设置）
        # 这里我们使用相同的限制
        if user.copywriter_usage_count >= self.FREE_PLAN_LIMIT:
            logger.warning(f"User {user_id} exceeded copywriter quota")
            raise QuotaExceededException(
                message=f"已达到免费计划配额上限（{self.FREE_PLAN_LIMIT} 次/月）",
                usage=user.copywriter_usage_count,
                limit=self.FREE_PLAN_LIMIT,
                quota_type="copywriter"
            )

        await self._increment_usage(user, 'copywriter')
        logger.info(f"User {user_id} copywriter quota: {user.copywriter_usage_count + 1}/{self.FREE_PLAN_LIMIT}")

        return user

    async def get_user_quota_info(self, user_id: int) -> dict:
        """
        获取用户配额信息

        Args:
            user_id: 用户 ID

        Returns:
            配额信息字典
        """
        user = await self.user_dao.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        # 检查是否需要重置配额
        await self._reset_quota_if_needed(user)

        is_pro = user.membership_level == 'pro'
        plan_limit = 0 if is_pro else self.FREE_PLAN_LIMIT
        remaining_plans = 0 if is_pro else (plan_limit - user.plan_usage_count)

        return {
            "membership_level": user.membership_level,
            "is_pro": is_pro,
            "plan_usage_count": user.plan_usage_count,
            "plan_limit": plan_limit,
            "remaining_plans": remaining_plans,
            "copywriter_usage_count": user.copywriter_usage_count,
            "copywriter_limit": plan_limit,  # 暂时使用相同限制
            "last_reset": user.last_quota_reset,
            "unlimited": is_pro
        }

    async def _reset_quota_if_needed(self, user: User) -> None:
        """
        如果需要，重置用户配额（每月第一天重置）

        Args:
            user: 用户对象
        """
        today = date.today()

        # 如果从未重置过，或者重置日期不是本月
        if user.last_quota_reset is None or user.last_quota_reset.month != today.month or user.last_quota_reset.year != today.year:
            logger.info(f"Resetting quota for user {user.id} (last reset: {user.last_quota_reset})")
            user.plan_usage_count = 0
            user.copywriter_usage_count = 0
            user.last_quota_reset = today
            await self.db.flush()

    async def _increment_usage(self, user: User, usage_type: str) -> None:
        """
        增加使用次数

        Args:
            user: 用户对象
            usage_type: 使用类型 ('plan' 或 'copywriter')
        """
        if usage_type == 'plan':
            user.plan_usage_count += 1
        elif usage_type == 'copywriter':
            user.copywriter_usage_count += 1

        await self.db.flush()
