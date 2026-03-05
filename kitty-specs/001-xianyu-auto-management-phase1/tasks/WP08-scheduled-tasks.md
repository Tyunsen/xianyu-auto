---
work_package_id: WP08
title: 定时任务模块
lane: "doing"
dependencies: [WP02, WP03]
base_branch: 001-xianyu-auto-management-phase1-WP07
base_commit: 01bc0f5b2ed20b0f7b4d8898c1999619dabb0ae3
created_at: '2026-03-05T07:17:39.389230+00:00'
subtasks: [T033, T034, T035, T036]
shell_pid: "41372"
history:
- date: '2026-03-05'
  action: created
---

# WP08: 定时任务模块

## Objective

实现 APScheduler 定时任务，包括自动擦亮、自动签到。

**定时执行时间**: 中午12-13点

## Subtasks

### T033: 配置 APScheduler

**Steps**:
1. 安装: `pip install apscheduler`
2. 创建 `backend/src/tasks/scheduler.py`:
   ```python
   from apscheduler.schedulers.asyncio import AsyncIOScheduler
   from apscheduler.triggers.cron import CronTrigger

   scheduler = AsyncIOScheduler()

   def setup_scheduler():
       # 定时任务将在 WP06, WP07 实现后添加
       pass
   ```

### T034: 实现自动擦亮任务

**Steps**:
```python
@scheduler.scheduled_job(CronTrigger(hour=12, minute=0))
async def auto_refresh():
    """每天中午12点擦亮"""
    for product in get_published_products():
        # 使用 Playwright 擦亮商品
        log(f"擦亮商品: {product.title}")
```

### T035: 实现自动签到任务

**Steps**:
```python
@scheduler.scheduled_job(CronTrigger(hour=12, minute=30))
async def auto_sign_in():
    """每天中午12:30签到"""
    for account in get_active_accounts():
        # 使用 Playwright 签到
        log(f"账号签到: {account.nickname}")
```

### T036: 实现任务日志记录

**Steps**:
1. 创建 `backend/src/services/log_service.py`:
   ```python
   def log_task(category: str, content: str, level: str = "info"):
       # 记录到 logs 表
       pass
   ```

## Dependencies

- WP02: 数据库模型
- WP03: 账号管理

## Implementation Command

```bash
spec-kitty implement WP08 --base WP03
```
