---
work_package_id: WP05
title: 卡密管理模块（后端）
lane: "doing"
dependencies: [WP02]
base_branch: 001-xianyu-auto-management-phase1-WP02
base_commit: e7826b8acee95959df53463c6f1e97a3439968cb
created_at: '2026-03-05T07:06:12.874352+00:00'
subtasks: [T019, T020, T021, T022]
shell_pid: "24440"
agent: "claude-code"
history:
- date: '2026-03-05'
  action: created
---

# WP05: 卡密管理模块（后端）

## Objective

实现卡密的后端管理功能，包括 CRUD、批量导入、库存统计。

## Subtasks

### T019: 创建卡密 API 路由

**Steps**:
1. 创建 `backend/src/schemas/card_key.py`
2. 创建 `backend/src/api/card_keys.py`:
   - GET /api/card-keys - 列表
   - POST /api/card-keys - 创建
   - DELETE /api/card-keys/{id} - 删除
   - GET /api/card-keys/stats - 库存统计

### T020: 实现卡密批量导入

**Steps**:
```python
@router.post("/import")
async def import_card_keys(file: UploadFile, product_id: int, db: Session = Depends(get_db)):
    # 解析 CSV/Excel
    # 批量插入
    return {"imported": 100, "failed": 0}
```

### T021: 实现库存统计

**Steps**:
```python
@router.get("/stats")
async def get_card_key_stats(product_id: int, db: Session = Depends(get_db)):
    total = db.query(CardKey).filter(CardKey.product_id == product_id).count()
    available = db.query(CardKey).filter(
        CardKey.product_id == product_id,
        CardKey.status == "available"
    ).count()
    return {"total": total, "available": available, "used": total - available}
```

### T022: 实现卡密Steps**:
1使用记录

**. 在 Order 创建时自动分配卡密
2. 更新卡密状态为 used
3. 记录 used_at 和 used_order_id

## Dependencies

- WP02: 数据库模型和迁移

## Implementation Command

```bash
spec-kitty implement WP05 --base WP02
```

## Activity Log

- 2026-03-05T07:06:15Z – claude-code – shell_pid=24440 – lane=doing – Assigned agent via workflow command
