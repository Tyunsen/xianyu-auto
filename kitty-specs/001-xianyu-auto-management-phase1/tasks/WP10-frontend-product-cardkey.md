---
work_package_id: "WP10"
title: "前端商品和卡密管理"
lane: "planned"
dependencies: ["WP04", "WP05", "WP09"]
subtasks: ["T041", "T042", "T043", "T044"]
history:
  - date: "2026-03-05"
    action: "created"
---

# WP10: 前端商品和卡密管理

## Objective

创建商品管理和卡密管理页面。

## Subtasks

### T041: 实现商品列表页面

**Steps**:
1. 创建 `frontend/src/pages/Products.vue`
2. 使用 Table + Pagination
3. 支持搜索、筛选
4. 上架/下架操作按钮

### T042: 实现商品编辑页面

**Steps**:
1. 创建商品表单 Dialog
2. 支持图片上传
3. 支持富文本描述

### T043: 实现卡密列表页面

**Steps**:
1. 创建 `frontend/src/pages/CardKeys.vue`
2. 显示卡密列表和库存统计
3. 状态筛选

### T044: 实现卡密导入功能

**Steps**:
1. 创建导入 Dialog
2. 支持 CSV/Excel 上传
3. 导入进度显示

## Dependencies

- WP04: 商品管理（后端）
- WP05: 卡密管理（后端）
- WP09: 前端基础

## Implementation Command

```bash
spec-kitty implement WP10 --base WP09
```
