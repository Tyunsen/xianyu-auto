---
work_package_id: WP06
title: 订单和自动发货模块
lane: "done"
dependencies: [WP02, WP05, WP03]
base_branch: 001-xianyu-auto-management-phase1-WP05
base_commit: 98e8445ecc0e33cea444a688b598378c1bded668
created_at: '2026-03-05T07:08:10.804529+00:00'
subtasks: [T023, T024, T025, T026, T027]
shell_pid: "46808"
agent: "claude-code"
reviewed_by: "Tyunsen"
review_status: "approved"
history:
- date: '2026-03-05'
  action: created
---

# WP06: 订单和自动发货模块

## Objective

实现订单管理和自动发货功能。

## Subtasks

### T023: 创建订单 API 路由

**Steps**:
1. 创建 schemas/order.py
2. 创建 api/orders.py:
   - GET /api/orders - 列表（支持状态筛选）
   - GET /api/orders/{id} - 详情
   - POST /api/orders/{id}/ship - 手动发货

### T024: 实现订单监控服务

**Steps**:
1. 创建 `backend/src/services/order_monitor.py`:
   ```python
   class OrderMonitor:
       async def check_pending_orders(self):
           """检查待发货订单"""
           # 使用 Playwright 检查闲鱼订单
           # 同步到本地数据库
   ```

### T025: 实现自动发货

**Steps**:
```python
async def auto_ship_order(order_id: int):
    # 1. 获取可用卡密
    card_key = get_available_card_key(order.product_id)
    # 2. 发送卡密给买家
    send_message(order.buyer_nickname, f"您的卡密: {card_key.key}")
    # 3. 更新状态
    update_order_status(order_id, "shipped")
```

### T026: 实现自动确认发货

**Steps**:
```python
async def confirm_shipment(order_id: int):
    # 使用 Playwright 点击确认发货按钮
    pass
```

### T027: 实现免拼发货

**Steps**:
```python
async def direct_ship(order_id: int):
    # 跳过拼单，直接发货
    pass
```

## Dependencies

- WP02: 数据库模型
- WP05: 卡密管理
- WP03: 账号管理

## Implementation Command

```bash
spec-kitty implement WP06 --base WP05
```

## Activity Log

- 2026-03-05T07:08:13Z – claude-code – shell_pid=40524 – lane=doing – Assigned agent via workflow command
- 2026-03-05T07:12:09Z – claude-code – shell_pid=40524 – lane=for_review – Ready for review: 订单和自动发货模块已完成
- 2026-03-05T08:02:30Z – claude-code – shell_pid=46808 – lane=doing – Started review via workflow command
- 2026-03-05T08:02:42Z – claude-code – shell_pid=46808 – lane=done – Review passed: 订单管理API和自动发货服务完整
