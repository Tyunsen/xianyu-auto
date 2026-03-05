---
work_package_id: "WP09"
title: "前端基础和账号管理"
lane: "planned"
dependencies: ["WP01", "WP03"]
subtasks: ["T037", "T038", "T039", "T040"]
history:
  - date: "2026-03-05"
    action: "created"
---

# WP09: 前端基础和账号管理

## Objective

创建 Vue 3 前端基础结构和账号管理页面。

## Subtasks

### T037: 配置 Vue 3 + Element Plus

**Steps**:
1. 在 main.ts 中引入 Element Plus:
   ```typescript
   import { createApp } from 'vue'
   import ElementPlus from 'element-plus'
   import 'element-plus/dist/index.css'
   import App from './App.vue'

   const app = createApp(App)
   app.use(ElementPlus)
   app.mount('#app')
   ```

### T038: 创建基础布局和路由

**Steps**:
1. 创建 `frontend/src/router/index.ts`:
   ```typescript
   const routes = [
     { path: '/', redirect: '/accounts' },
     { path: '/accounts', component: () => import('@/pages/Accounts.vue') },
     { path: '/products', component: () => import('@/pages/Products.vue') },
     // ... 其他路由
   ]
   ```
2. 创建基础布局 `App.vue`:
   - 左侧导航栏
   - 顶部 Header
   - 主内容区

### T039: 实现账号列表页面

**Steps**:
1. 创建 `frontend/src/pages/Accounts.vue`:
   - 使用 Element Plus Table 组件
   - 显示账号列表
   - 支持搜索、筛选

### T040: 实现账号添加/编辑页面

**Steps**:
1. 创建账号表单 Dialog
2. 添加扫码登录功能
3. 实现账号状态显示

## Dependencies

- WP01: 项目基础设置
- WP03: 账号管理模块（后端）

## Implementation Command

```bash
spec-kitty implement WP09 --base WP01
```
