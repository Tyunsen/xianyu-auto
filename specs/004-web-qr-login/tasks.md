# Tasks: 网页端咸鱼扫码登录

**Feature**: 004-web-qr-login | **Generated**: 2026-03-06

## Summary

- **Total Tasks**: 14
- **User Stories**: 3
- **Parallel Opportunities**: 2
- **Completed**: 6

## Dependencies Graph

```
Phase 1: Setup (已完成)
    │
Phase 2: Foundational (已完成)
    │
    ├──▶ Phase 3: US1 网页端扫码登录 ──────▶ Phase 5: Polish
    │       (前端UI完善) ✅ 已完成
    │
    ├──▶ Phase 4: US2 登录状态检测 ─────────▶ Phase 5: Polish
    │       (定时任务)
    │
    └──▶ Phase 5: US3 状态展示 ──────────────▶ Phase 5: Polish
            (列表功能) ✅ 已完成
```

## MVP Scope

**建议MVP**: 仅包含 **US1 - 网页端扫码登录**

- 用户可以直接在网页上扫码登录咸鱼账号
- 完成后账号状态显示"在线"
- 这是用户最核心的需求

---

## Phase 1: Setup

项目初始化（已在之前完成）

- [X] T001 验证 Playwright 依赖已在 Dockerfile 中正确配置
- [X] T002 验证 Docker Compose 配置正确

---

## Phase 2: Foundational

基础功能验证（已在之前完成）

- [X] T003 [P] 验证后端 playwright_helper.py 二维码生成功能正常
- [X] T004 [P] 验证后端 API 端点正确注册

---

## Phase 3: User Story 1 - 网页端扫码登录

**Goal**: 管理员可以在网页前端扫码登录咸鱼账号，无需手动复制Cookie

**Independent Test**: 管理员点击"扫码登录" → 显示二维码 → 扫码成功 → 账号状态变为"在线"

### Implementation Tasks

- [X] T005 [P] [US1] 在 frontend/src/pages/Accounts.vue 添加"扫码登录"按钮和二维码对话框
- [X] T006 [US1] 实现二维码显示和轮询检测逻辑
- [X] T007 [US1] 登录成功后自动刷新账号列表
- [X] T008 [US1] 添加超时错误处理和重试提示

### Test Scenarios

1. 点击"扫码登录"按钮弹出二维码对话框
2. 二维码正确显示在对话框中
3. 扫码后账号状态变为"在线"
4. 超时显示错误提示

---

## Phase 4: User Story 2 - 登录状态自动检测

**Goal**: 定时检测账号登录状态，过期时发送邮件通知

**Independent Test**: 定时任务执行 → 检测所有账号 → 过期账号标记并通知

### Implementation Tasks

- [ ] T009 [P] [US2] 验证 login_check_task.py 定时任务正确执行
- [ ] T010 [US2] 验证邮件通知在检测到过期时发送

### Test Scenarios

1. 手动触发检测所有账号状态
2. 过期账号状态正确更新为"expired"

---

## Phase 5: User Story 3 - 多账号管理与状态展示

**Goal**: 管理员可以清晰查看所有账号的登录状态

**Independent Test**: 查看账号列表 → 看到每个账号的实时状态 → 可进行操作

### Implementation Tasks

- [X] T011 [US3] 添加"刷新状态"按钮功能
- [X] T012 [US3] 添加"重新登录"按钮（对于过期账号）

### Test Scenarios

1. 账号列表显示正确的状态标签（在线/离线/过期）
2. 点击"刷新状态"立即检测并更新显示

---

## Phase 6: Polish & Cross-Cutting

- [ ] T013 端到端测试完整扫码登录流程
- [ ] T014 更新 README.md 添加新功能说明

---

## Parallel Execution Examples

### US1 内部并行
```
T005 (前端UI) ─┐
                ├─▶ T007 (登录成功后刷新)
T006 (轮询)  ───┘
```

### US2/US3 可以并行
```
T009 (定时任务) ──┐
                   ├─▶ T011/T012 (状态展示)
T010 (邮件通知) ──┘
```

---

## Implementation Strategy

### MVP (Phase 3: US1) ✅ 已完成
1. 修改 Accounts.vue 添加扫码登录UI
2. 测试端到端流程

### Incremental Delivery
1. **Sprint 1**: 完成 US1 - 网页端扫码登录 ✅
2. **Sprint 2**: 完成 US2 - 登录状态检测
3. **Sprint 3**: 完成 US3 - 状态展示
