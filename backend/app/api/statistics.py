from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StatisticsResponse(BaseModel):
    total_accounts: int
    active_accounts: int
    total_products: int
    on_shelf_products: int
    total_cards: int
    unused_cards: int
    total_orders: int
    pending_orders: int
    completed_orders: int
    total_revenue: int
    today_orders: int
    today_revenue: int
    unread_messages: int
    pending_alerts: int


class DashboardResponse(BaseModel):
    statistics: StatisticsResponse
    recent_orders: list
    recent_alerts: list
