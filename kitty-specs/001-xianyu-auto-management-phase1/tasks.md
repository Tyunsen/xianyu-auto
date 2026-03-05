# Tasks: 闲鱼自动管理系统（第一期）

**Feature**: 001-xianyu-auto-management-phase1
**Created**: 2026-03-05
**Total Subtasks**: 50+
**Work Packages**: 14

---

## Work Package Overview

| WP | Title | Subtasks | Priority | Dependencies |
|----|-------|----------|----------|--------------|
| WP01 | 项目基础设置 | 5 | P0 | - |
| WP02 | 数据库模型和迁移 | 5 | P0 | WP01 |
| WP03 | 账号管理模块（后端） | 4 | P1 | WP02 |
| WP04 | 商品管理模块（后端） | 4 | P1 | WP02 |
| WP05 | 卡密管理模块（后端） | 4 | P1 | WP02 |
| WP06 | 订单和自动发货模块 | 5 | P1 | WP02, WP05 |
| WP07 | 智能客服（CC）模块 | 5 | P1 | WP02, WP03 |
| WP08 | 定时任务模块 | 4 | P1 | WP02, WP03 |
| WP09 | 前端基础和账号管理 | 4 | P2 | WP03 |
| WP10 | 前端商品和卡密管理 | 4 | P2 | WP04, WP05 |
| WP11 | 前端订单和统计页面 | 4 | P2 | WP06 |
| WP12 | 通知和告警模块 | 3 | P2 | WP02 |
| WP13 | 备份导出和系统设置 | 3 | P2 | WP02 |
| WP14 | 集成测试和优化 | 4 | P3 | WP01-WP13 |

---

## WP01: 项目基础设置

**Summary**: 创建项目结构、Docker配置、环境变量基础
**Priority**: P0 (必须首先完成)
**Estimated Size**: ~350 lines

**Included Subtasks**:
- [x] T001: 创建后端项目结构 (backend/src/)
- [x] T002: 创建前端项目结构 (frontend/)
- [x] T003: 配置 Docker Compose
- [x] T004: 配置环境变量 (.env.example)
- [x] T005: 安装基础依赖

**Implementation**:
1. 初始化后端 Python 项目结构
2. 初始化前端 Vue 3 项目
3. 创建 docker-compose.yml
4. 创建环境变量配置文件
5. 配置基础依赖

**Dependencies**: None

**Risks**: None

**Prompt File**: [WP01-project-setup.md](tasks/WP01-project-setup.md)

---

## WP02: 数据库模型和迁移

**Summary**: 创建 SQLAlchemy 模型、数据库迁移、Alembic 配置
**Priority**: P0
**Estimated Size**: ~400 lines

**Included Subtasks**:
- [x] T006: 配置 SQLAlchemy 和 Alembic
- [x] T007: 创建账号、商品、卡密模型
- [x] T008: 创建订单、消息、告警模型
- [x] T009: 创建配置、日志、黑名单模型
- [x] T010: 执行首次数据库迁移

**Implementation**:
1. 配置 database connection
2. 创建所有数据模型
3. 设置索引
4. 执行迁移

**Dependencies**: WP01

**Risks**: 需要确保 PostgreSQL 可用

**Prompt File**: [WP02-database-models.md](tasks/WP02-database-models.md)

---

## WP03: 账号管理模块（后端）

**Summary**: 账号 CRUD、登录状态检测、Cookie 管理
**Priority**: P1
**Estimated Size**: ~350 lines

**Included Subtasks**:
- [x] T011: 创建账号 API 路由 (CRUD)
- [x] T012: 实现登录状态检测服务
- [x] T013: 实现 Cookie 加密存储
- [x] T014: 实现登录失效告警

**Implementation**:
1. 创建账号路由
2. 实现状态检测
3. 加密存储凭证

**Dependencies**: WP02

**Risks**: 登录检测需要浏览器环境

**Prompt File**: [WP03-account-management.md](tasks/WP03-account-management.md)

---

## WP04: 商品管理模块（后端）

**Summary**: 商品 CRUD、批量导入、上架下架
**Priority**: P1
**Estimated Size**: ~350 lines

**Included Subtasks**:
- [x] T015: 创建商品 API 路由 (CRUD)
- [x] T016: 实现商品批量导入
- [x] T017: 实现手动上架功能
- [x] T018: 实现手动下架功能

**Implementation**:
1. 创建商品路由
2. 实现批量导入
3. 对接闲鱼 API 上架

**Dependencies**: WP02, WP03

**Risks**: 需要 Playwright 浏览器环境

**Prompt File**: [WP04-product-management.md](tasks/WP04-product-management.md)

---

## WP05: 卡密管理模块（后端）

**Summary**: 卡密 CRUD、库存管理、批量导入
**Priority**: P1
**Estimated Size**: ~300 lines

**Included Subtasks**:
- [x] T019: 创建卡密 API 路由
- [x] T020: 实现卡密批量导入
- [x] T021: 实现库存统计
- [x] T022: 实现卡密使用记录

**Implementation**:
1. 创建卡密路由
2. 实现批量导入
3. 库存统计

**Dependencies**: WP02

**Risks**: None

**Prompt File**: [WP05-cardkey-management.md](tasks/WP05-cardkey-management.md)

---

## WP06: 订单和自动发货模块

**Summary**: 订单管理、自动发货、自动确认、免拼发货
**Priority**: P1
**Estimated Size**: ~400 lines

**Included Subtasks**:
- [x] T023: 创建订单 API 路由
- [x] T024: 实现订单监控服务
- [x] T025: 实现自动发货
- [x] T026: 实现自动确认发货
- [x] T027: 实现免拼发货

**Implementation**:
1. 创建订单路由
2. 实现自动发货逻辑
3. 对接闲鱼消息发送

**Dependencies**: WP02, WP05, WP03

**Risks**: 闲鱼 API 稳定性

**Prompt File**: [WP06-order-fulfillment.md](tasks/WP06-order-fulfillment.md)

---

## WP07: 智能客服（CC）模块

**Summary**: 消息检测、AI回复生成、自动回复
**Priority**: P1
**Estimated Size**: ~450 lines

**Included Subtasks**:
- [x] T028: 创建消息 API 路由
- [x] T029: 实现消息检测服务
- [x] T030: 集成 MiniMax AI
- [x] T031: 实现自动回复逻辑
- [x] T032: 实现回复记录保存

**Implementation**:
1. 创建消息路由
2. 实现 AI 集成
3. 实现自动回复

**Dependencies**: WP02, WP03

**Risks**: AI API 成本和响应质量

**Prompt File**: [WP07-smart-customer-service.md](tasks/WP07-smart-customer-service.md)

---

## WP08: 定时任务模块

**Summary**: APScheduler 配置、自动擦亮、自动签到
**Priority**: P1
**Estimated Size**: ~350 lines

**Included Subtasks**:
- [x] T033: 配置 APScheduler
- [x] T034: 实现自动擦亮任务
- [x] T035: 实现自动签到任务
- [x] T036: 实现任务日志记录

**Implementation**:
1. 配置调度器
2. 实现定时任务
3. 日志记录

**Dependencies**: WP02, WP03

**Risks**: 任务执行时间

**Prompt File**: [WP08-scheduled-tasks.md](tasks/WP08-scheduled-tasks.md)

---

## WP09: 前端基础和账号管理

**Summary**: Vue 3 基础组件、账号管理页面
**Priority**: P2
**Estimated Size**: ~400 lines

**Included Subtasks**:
- [x] T037: 配置 Vue 3 + Element Plus
- [x] T038: 创建基础布局和路由
- [x] T039: 实现账号列表页面
- [x] T040: 实现账号添加/编辑页面

**Implementation**:
1. 初始化前端
2. 创建页面组件

**Dependencies**: WP01, WP03

**Risks**: None

**Prompt File**: [WP09-frontend-account.md](tasks/WP09-frontend-account.md)

---

## WP10: 前端商品和卡密管理

**Summary**: 商品管理页面、卡密管理页面
**Priority**: P2
**Estimated Size**: ~400 lines

**Included Subtasks**:
- [x] T041: 实现商品列表页面
- [x] T042: 实现商品编辑页面
- [x] T043: 实现卡密列表页面
- [x] T044: 实现卡密导入功能

**Implementation**:
1. 创建商品页面
2. 创建卡密页面

**Dependencies**: WP04, WP05, WP09

**Risks**: None

**Prompt File**: [WP10-frontend-product-cardkey.md](tasks/WP10-frontend-product-cardkey.md)

---

## WP11: 前端订单和统计页面

**Summary**: 订单列表页面、数据统计页面
**Priority**: P2
**Estimated Size**: ~350 lines

**Included Subtasks**:
- [ ] T045: 实现订单列表页面
- [ ] T046: 实现消息对话页面
- [ ] T047: 实现数据统计页面
- [ ] T048: 实现日志查看页面

**Implementation**:
1. 创建订单页面
2. 创建统计页面

**Dependencies**: WP06, WP07, WP09

**Risks**: None

**Prompt File**: [WP11-frontend-order-stats.md](tasks/WP11-frontend-order-stats.md)

---

## WP12: 通知和告警模块

**Summary**: 邮件通知、告警管理
**Priority**: P2
**Estimated Size**: ~300 lines

**Included Subtasks**:
- [ ] T049: 配置邮件服务
- [ ] T050: 实现告警检测服务
- [ ] T051: 实现邮件通知发送

**Implementation**:
1. 邮件配置
2. 告警逻辑

**Dependencies**: WP02, WP03

**Risks**: 邮件发送稳定性

**Prompt File**: [WP12-notification-alert.md](tasks/WP12-notification-alert.md)

---

## WP13: 备份导出和系统设置

**Summary**: 数据备份导出、系统设置
**Priority**: P2
**Estimated Size**: ~250 lines

**Included Subtasks**:
- [ ] T052: 实现数据导出功能
- [ ] T053: 实现数据导入功能
- [ ] T054: 实现系统设置页面

**Implementation**:
1. 导出功能
2. 设置页面

**Dependencies**: WP02

**Risks**: None

**Prompt File**: [WP13-backup-settings.md](tasks/WP13-backup-settings.md)

---

## WP14: 集成测试和优化

**Summary**: 单元测试、集成测试、性能优化
**Priority**: P3
**Estimated Size**: ~300 lines

**Included Subtasks**:
- [ ] T055: 编写核心功能单元测试
- [ ] T056: 编写集成测试
- [ ] T057: 性能优化
- [ ] T058: 代码审查和修复

**Implementation**:
1. 测试覆盖
2. 性能优化

**Dependencies**: WP01-WP13

**Risks**: None

**Prompt File**: [WP14-testing-optimization.md](tasks/WP14-testing-optimization.md)

---

## MVP Scope

**建议首先实现**: WP01 + WP02 + WP03 + WP04 + WP05 + WP09

这些工作包完成后，系统将具备：
- 基础项目结构
- 数据库模型
- 账号管理（后端+前端）
- 商品管理（后端+前端）
- 卡密管理（后端+前端）

---

## Parallelization Opportunities

以下工作包可以并行开发：
- WP03, WP04, WP05 可以并行（都依赖 WP02）
- WP09, WP10, WP11 可以并行（都依赖后端 API）
- WP12, WP13 可以并行（都依赖 WP02）

---

## Notes

- 核心功能必须有单元测试（根据 Constitution）
- 使用 simplify 技能审查代码质量
- 重大节点进行 git 提交
