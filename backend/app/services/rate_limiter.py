"""
风控保护模块 - 操作限流
"""
import time
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """操作限流器"""

    def __init__(self):
        # 每小时操作次数限制
        self.max_per_hour = 20
        # 每分钟操作次数限制
        self.max_per_minute = 5
        # 操作记录
        self.operations: Dict[int, list] = defaultdict(list)
        # 全局锁
        self._lock = False

    def set_limits(self, max_per_hour: int, max_per_minute: int):
        """设置限流参数"""
        self.max_per_hour = max_per_hour
        self.max_per_minute = max_per_minute
        logger.info(f"限流设置: {max_per_hour}次/小时, {max_per_minute}次/分钟")

    def check_limit(self, account_id: int) -> bool:
        """
        检查是否达到限制

        Args:
            account_id: 账号ID

        Returns:
            True: 可以执行操作
            False: 达到限制
        """
        now = time.time()
        hour_ago = now - 3600
        minute_ago = now - 60

        # 清理过期记录
        self.operations[account_id] = [
            t for t in self.operations[account_id]
            if t > hour_ago
        ]

        ops = self.operations[account_id]

        # 检查分钟限制
        minute_ops = [t for t in ops if t > minute_ago]
        if len(minute_ops) >= self.max_per_minute:
            logger.warning(f"账号 {account_id} 达到分钟限流: {len(minute_ops)}/{self.max_per_minute}")
            return False

        # 检查小时限制
        if len(ops) >= self.max_per_hour:
            logger.warning(f"账号 {account_id} 达到小时限流: {len(ops)}/{self.max_per_hour}")
            return False

        return True

    def record_operation(self, account_id: int):
        """记录操作"""
        self.operations[account_id].append(time.time())

    def get_remaining(self, account_id: int) -> Dict[str, int]:
        """获取剩余次数"""
        now = time.time()
        hour_ago = now - 3600
        minute_ago = now - 60

        ops = self.operations[account_id]
        recent_ops = [t for t in ops if t > hour_ago]
        minute_ops = [t for t in ops if t > minute_ago]

        return {
            "hourly_remaining": max(0, self.max_per_hour - len(recent_ops)),
            "minute_remaining": max(0, self.max_per_minute - len(minute_ops))
        }

    def reset(self, account_id: Optional[int] = None):
        """重置记录"""
        if account_id:
            self.operations[account_id] = []
        else:
            self.operations.clear()


# 全局限流器
rate_limiter = RateLimiter()


class OperationTracker:
    """操作追踪器 - 记录操作日志"""

    def __init__(self):
        self.last_operation_time: Dict[int, datetime] = {}
        self.operation_count_today: Dict[int, int] = defaultdict(int)
        self.last_reset_date = datetime.now().date()

    def can_operate(self, account_id: int, min_interval: int = 5) -> bool:
        """
        检查是否可以执行操作（考虑时间间隔）

        Args:
            account_id: 账号ID
            min_interval: 最小操作间隔（秒）

        Returns:
            True: 可以执行
        """
        # 检查是否需要重置每日计数
        today = datetime.now().date()
        if today > self.last_reset_date:
            self.operation_count_today.clear()
            self.last_reset_date = today

        # 检查时间间隔
        last_time = self.last_operation_time.get(account_id)
        if last_time:
            elapsed = (datetime.now() - last_time).total_seconds()
            if elapsed < min_interval:
                logger.debug(f"账号 {account_id} 操作间隔不足: {elapsed}秒 < {min_interval}秒")
                return False

        return True

    def record_operation(self, account_id: int):
        """记录操作"""
        self.last_operation_time[account_id] = datetime.now()
        self.operation_count_today[account_id] += 1

    def get_today_count(self, account_id: int) -> int:
        """获取今日操作次数"""
        today = datetime.now().date()
        if today > self.last_reset_date:
            return 0
        return self.operation_count_today.get(account_id, 0)


# 全局操作追踪器
operation_tracker = OperationTracker()
