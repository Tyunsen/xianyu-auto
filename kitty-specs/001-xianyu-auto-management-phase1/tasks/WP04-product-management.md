---
work_package_id: WP04
title: 商品管理模块（后端）
lane: "doing"
dependencies: [WP02]
base_branch: 001-xianyu-auto-management-phase1-WP02
base_commit: e7826b8acee95959df53463c6f1e97a3439968cb
created_at: '2026-03-05T07:03:26.966982+00:00'
subtasks: [T015, T016, T017, T018]
shell_pid: "41040"
agent: "claude-code"
history:
- date: '2026-03-05'
  action: created
---

# WP04: 商品管理模块（后端）

## Objective

实现商品的后端管理功能，包括 CRUD、批量导入、手动上下架。

## Subtasks

### T015: 创建商品 API 路由 (CRUD)

**Steps**:
1. 创建 `backend/src/schemas/product.py`
2. 创建 `backend/src/api/products.py`:
   - GET /api/products - 列表（支持分页、搜索）
   - POST /api/products - 创建
   - GET /api/products/{id} - 详情
   - PUT /api/products/{id} - 更新
   - DELETE /api/products/{id} - 删除

### T016: 实现商品批量导入

**Steps**:
1. 创建导入 API:
   ```python
   @router.post("/import")
   async def import_products(file: UploadFile, db: Session = Depends(get_db)):
       # 支持 CSV/Excel
       # 解析文件
       # 批量插入
       return {"imported": 50, "failed": 0}
   ```

### T017: 实现手动上架功能

**Steps**:
1. 创建发布 API:
   ```python
   @router.post("/{product_id}/publish")
   async def publish_product(product_id: int, db: Session = Depends(get_db)):
       # 使用 Playwright 发布到闲鱼
       # 保存 xianyu_id
       return {"status": "published", "xianyu_id": "xy123"}
   ```

### T018: 实现手动下架功能

**Steps**:
1. 创建下架 API:
   ```python
   @router.post("/{product_id}/unpublish")
   async def unpublish_product(product_id: int, db: Session = Depends(get_db)):
       # 使用 Playwright 下架
       return {"status": "offline"}
   ```

## Dependencies

- WP02: 数据库模型和迁移

## Implementation Command

```bash
spec-kitty implement WP04 --base WP02
```

## Activity Log

- 2026-03-05T07:03:29Z – claude-code – shell_pid=41040 – lane=doing – Assigned agent via workflow command
