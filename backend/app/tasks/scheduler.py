"""
定时任务调度器
支持每1分钟+-随机秒执行
"""
import asyncio
import random
import logging
from datetime import datetime
from typing import Callable, Dict, Any, Optional
from app.core.database import SessionLocal
from app.services.log_service import LogService

logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器"""

    def __init__(self):
        self.tasks: Dict[str, Callable] = {}
        self.running = False
        self.interval = 60  # 基础间隔60秒
        self.random_delay = 30  # 随机延迟0-30秒

    def register_task(self, name: str, task: Callable):
        """注册任务"""
        self.tasks[name] = task
        logger.info(f"注册任务: {name}")

    async def run_task(self, name: str):
        """运行单个任务"""
        if name not in self.tasks:
            logger.warning(f"任务不存在: {name}")
            return

        task = self.tasks[name]
        logger.info(f"开始执行任务: {name}")

        try:
            # 创建数据库会话
            db = SessionLocal()
            log_service = LogService(db)

            # 执行任务
            if asyncio.iscoroutinefunction(task):
                await task(db)
            else:
                task(db)

            log_service.info("task", f"任务执行成功: {name}")
            logger.info(f"任务执行成功: {name}")

        except Exception as e:
            logger.error(f"任务执行失败: {name}, 错误: {e}")

            # 记录错误日志
            try:
                db = SessionLocal()
                log_service = LogService(db)
                log_service.error("task", f"任务执行失败: {name}, 错误: {str(e)}")
            except Exception:
                pass
        finally:
            try:
                db.close()
            except Exception:
                pass

    async def run_all_tasks(self):
        """运行所有注册的任务"""
        for name in self.tasks.keys():
            await self.run_task(name)

    async def start(self):
        """启动调度器"""
        self.running = True
        logger.info("定时任务调度器已启动")

        while self.running:
            try:
                # 计算随机延迟
                delay = self.interval + random.randint(0, self.random_delay)
                logger.debug(f"等待 {delay} 秒后执行任务")

                await asyncio.sleep(delay)

                if self.running:
                    await self.run_all_tasks()

            except Exception as e:
                logger.error(f"调度器循环异常: {e}")
                await asyncio.sleep(5)

    def stop(self):
        """停止调度器"""
        self.running = False
        logger.info("定时任务调度器已停止")

    def set_interval(self, interval: int, random_delay: int = 30):
        """设置执行间隔"""
        self.interval = interval * 60  # 转换为秒
        self.random_delay = random_delay
        logger.info(f"任务间隔设置为: {interval}分钟 ± {random_delay}秒")


# 全局调度器实例
scheduler = TaskScheduler()


# 任务装饰器
def task(name: str):
    """任务装饰器"""
    def decorator(func: Callable):
        scheduler.register_task(name, func)
        return func
    return decorator
