"""
Plan Schemas V2.0 - 重新设计，更符合用户需求

This module contains Pydantic models for travel plan data.
基于用户真实需求设计，隐藏技术细节，突出实用信息。
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime


class TransportationInfo(BaseModel):
    """交通信息"""
    method: str = Field(..., description="交通方式：地铁/公交/打车/自驾/步行/飞机/高铁")
    from_location: str = Field(..., description="出发地点")
    to_location: str = Field(..., description="目的地")
    duration: str = Field(..., description="耗时描述：30分钟/1小时/约2小时")
    cost: float = Field(..., ge=0, description="费用")
    tips: Optional[str] = Field(None, description="实用提示")


class Activity(BaseModel):
    """
    活动信息 - 用户友好的设计
    隐藏_coordinates（仅用于地图），突出用户关心的信息
    """
    # 基本信息
    title: str = Field(..., description="活动标题")
    type: str = Field(..., description="活动类型：attraction/meal/transport/accommodation/shopping/entertainment")
    time: str = Field(..., description="开始时间")
    duration: str = Field(..., description="预计时长：2小时/半天/1.5小时")

    # 景点/活动信息
    description: str = Field(..., description="详细描述")
    highlights: Optional[List[str]] = Field(default=[], description="推荐理由/特色")
    address: Optional[str] = Field(None, description="地址（transport类型可能为空）")
    ticket_price: Optional[float] = Field(None, description="门票价格")
    need_booking: bool = Field(default=False, description="是否需要提前预订")
    booking_info: Optional[str] = Field(None, description="预订方式提示")

    # 餐饮信息（如果是meal类型）
    cuisine: Optional[str] = Field(None, description="菜系/类型")
    average_cost: float = Field(default=0, ge=0, description="人均消费")
    recommended_dishes: Optional[List[str]] = Field(default=[], description="必点菜品")
    wait_time: Optional[str] = Field(None, description="是否需要排队")
    opening_hours: Optional[str] = Field(None, description="营业时间")

    # 贴士信息
    best_time: Optional[str] = Field(None, description="最佳游览时间")
    tips: Optional[List[str]] = Field(default=[], description="注意事项")
    dress_code: Optional[str] = Field(None, description="穿衣建议")

    # 交通信息
    transportation: Optional[TransportationInfo] = Field(None, description="到达方式")
    parking_info: Optional[str] = Field(None, description="停车信息")

    # 技术数据（用于地图展示）
    coordinates: Optional[Dict[str, float]] = Field(
        None,
        description="经纬度坐标（用于地图展示）"
    )


class AccommodationInfo(BaseModel):
    """住宿信息"""
    name: str = Field(..., description="名称")
    address: str = Field(..., description="地址")
    type: str = Field(..., description="类型：酒店/民宿/青旅")
    facilities: List[str] = Field(default=[], description="设施：WiFi/停车场/早餐")
    rating: Optional[float] = Field(None, ge=0, le=5, description="评分")
    booking_status: Optional[str] = Field(None, description="预订状态")


class CostBreakdown(BaseModel):
    """费用明细"""
    transportation: float = Field(..., ge=0, description="交通费用")
    accommodation: float = Field(..., ge=0, description="住宿费用")
    food: float = Field(..., ge=0, description="餐饮费用")
    tickets: float = Field(..., ge=0, description="门票费用")
    shopping: float = Field(..., ge=0, description="购物费用")
    other: float = Field(..., ge=0, description="其他费用")


class PreparationInfo(BaseModel):
    """行前准备"""
    documents: List[str] = Field(default=[], description="必备证件")
    essentials: List[str] = Field(default=[], description="必带物品")
    suggestions: List[str] = Field(default=[], description="建议携带")
    booking_reminders: List[str] = Field(default=[], description="预订提醒")


class TravelTips(BaseModel):
    """实用提示"""
    transportation: Optional[str] = Field(None, description="交通提示")
    accommodation: Optional[str] = Field(None, description="住宿提示")
    food: Optional[str] = Field(None, description="餐饮提示")
    shopping: Optional[str] = Field(None, description="购物提示")
    safety: Optional[str] = Field(None, description="安全提示")
    other: Optional[List[str]] = Field(default=[], description="其他提醒")


class DayPlan(BaseModel):
    """
    每日行程计划
    """
    day_number: int = Field(..., ge=1, description="第几天")
    title: str = Field(..., description="主题")
    date: Optional[str] = Field(None, description="日期 YYYY-MM-DD")
    summary: Optional[str] = Field(None, description="概述")
    activities: List[Activity] = Field(default=[], description="活动列表（按时间排序）")
    notes: Optional[str] = Field(None, description="今日小结")
    total_cost: Optional[float] = Field(None, ge=0, description="今日总花费")
    accommodation: Optional[AccommodationInfo] = Field(None, description="住宿信息")


class PlanBase(BaseModel):
    """
    基础行程信息
    """
    title: str = Field(..., min_length=1, max_length=200, description="行程标题")
    destination: str = Field(..., min_length=1, max_length=200, description="目的地")
    departure: Optional[str] = Field(None, max_length=200, description="出发地")
    days: int = Field(..., ge=1, le=30, description="天数")
    budget: Optional[float] = Field(None, ge=0, description="预算")
    travel_style: str = Field(
        "leisure",
        pattern="^(leisure|adventure|foodie)$",
        description="旅行风格：leisure/adventure/foodie"
    )


class PlanCreate(PlanBase):
    """
    创建行程请求
    """
    pass


class PlanUpdate(BaseModel):
    """
    更新行程请求
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    budget: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(draft|active|completed|archived)$")


class PlanResponse(PlanBase):
    """
    行程响应 - 完整信息
    """
    id: int
    user_id: int
    status: str
    ai_generated: bool

    # 展示信息
    cover_image: Optional[str] = Field(None, description="封面图片URL")
    summary: Optional[str] = Field(None, description="行程概述")
    highlights: Optional[List[str]] = Field(default=[], description="行程亮点")
    best_season: Optional[str] = Field(None, description="最佳旅行时间")
    weather: Optional[str] = Field(None, description="天气提示")

    # 费用信息
    actual_cost: Optional[float] = Field(None, description="实际花费")
    cost_breakdown: Optional[CostBreakdown] = Field(None, description="费用明细")

    # 行程详情
    days_detail: List[DayPlan] = []

    # 行前准备
    preparation: Optional[PreparationInfo] = Field(None, description="行前准备")

    # 实用提示
    tips: Optional[TravelTips] = Field(None, description="实用提示")

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlanListResponse(BaseModel):
    """
    行程列表响应（简化版）
    """
    id: int
    title: str
    destination: str
    departure: Optional[str]
    days: int
    budget: Optional[float]
    actual_cost: Optional[float]
    travel_style: str
    status: str
    cover_image: Optional[str]
    summary: Optional[str]
    highlights: Optional[List[str]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GenerateDetailRequest(BaseModel):
    """
    生成详细行程请求
    """
    use_strict_json: bool = Field(default=True, description="是否使用严格JSON格式")


class OptimizeRequest(BaseModel):
    """
    优化行程请求
    """
    feedback: str = Field(..., min_length=1, description="用户反馈")
    affected_days: Optional[List[int]] = Field(default=[], description="受影响的天数列表")
    use_strict_json: bool = Field(default=True, description="是否使用严格JSON格式")
