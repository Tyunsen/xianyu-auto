---
work_package_id: WP02
title: 数据库模型和迁移
lane: "doing"
dependencies: [WP01]
base_branch: 001-xianyu-auto-management-phase1-WP01
base_commit: bb16aba76afd2b0a23c9ee06ed95f03f4b8e67a1
created_at: '2026-03-05T06:50:27.801681+00:00'
subtasks: [T006, T007, T008, T009, T010]
shell_pid: "48896"
agent: "claude-code"
history:
- date: '2026-03-05'
  action: created
---

# WP02: 数据库模型和迁移

## Objective

创建完整的数据库模型和 Alembic 迁移配置。

## Context

**数据库**: PostgreSQL
**ORM**: SQLAlchemy
**迁移工具**: Alembic

**数据表**:
1. accounts - 账号表
2. products - 商品表
3. card_keys - 卡密表
4. orders - 订单表
5. messages - 消息表
6. alerts - 告警表
7. blacklist - 黑名单表
8. settings - 系统配置表
9. logs - 运行日志表

## Subtasks

### T006: 配置 SQLAlchemy 和 Alembic

**Purpose**: 设置数据库连接和迁移工具

**Steps**:
1. 更新 `backend/src/database.py`:
   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker
   from sqlalchemy.pool import NullPool
   import os

   DATABASE_URL = os.getenv(
       "DATABASE_URL",
       "postgresql://xianyu:xianyu123@localhost:5432/xianyu_auto"
   )

   engine = create_engine(
       DATABASE_URL,
       poolclass=NullPool,  # 避免多线程问题
       echo=os.getenv("DEBUG", "false").lower() == "true"
   )

   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

   Base = declarative_base()

   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   ```
2. 初始化 Alembic:
   ```bash
   cd backend
   alembic init alembic
   ```
3. 配置 `alembic.ini` 和 `alembic/env.py`

**Files**:
- `backend/src/database.py`
- `backend/alembic.ini`
- `backend/alembic/env.py`

**Validation**:
- [ ] 数据库连接成功
- [ ] Alembic 配置正确

---

### T007: 创建账号、商品、卡密模型

**Purpose**: 创建基础数据模型

**Steps**:
1. 创建 `backend/src/models/account.py`:
   ```python
   from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
   from sqlalchemy.sql import func
   from src.database import Base
   import enum

   class AccountStatus(str, enum.Enum):
       ONLINE = "online"
       OFFLINE = "offline"
       EXPIRED = "expired"

   class Account(Base):
       __tablename__ = "accounts"

       id = Column(Integer, primary_key=True, index=True)
       nickname = Column(String(100), nullable=False)
       cookies = Column(String, nullable=False)  # 加密存储
       status = Column(String(20), default="offline")
       last_login = Column(DateTime, nullable=True)
       created_at = Column(DateTime, server_default=func.now())
       updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
   ```
2. 创建 `backend/src/models/product.py`:
   ```python
   class ProductStatus(str, enum.Enum):
       DRAFT = "draft"
       PUBLISHED = "published"
       OFFLINE = "offline"

   class Product(Base):
       __tablename__ = "products"

       id = Column(Integer, primary_key=True, index=True)
       title = Column(String(200), nullable=False)
       price = Column(Numeric(10, 2), nullable=False)
       description = Column(Text, nullable=True)
       images = Column(String, nullable=True)  # JSON 数组
       status = Column(String(20), default="draft")
       xianyu_id = Column(String(100), nullable=True)
       account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
       created_at = Column(DateTime, server_default=func.now())
       updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
   ```
3. 创建 `backend/src/models/card_key.py`:
   ```python
   class CardKeyStatus(str, enum.Enum):
       AVAILABLE = "available"
       USED = "used"

   class CardKey(Base):
       __tablename__ = "card_keys"

       id = Column(Integer, primary_key=True, index=True)
       key = Column(Text, nullable=False)
       product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
       status = Column(String(20), default="available")
       used_at = Column(DateTime, nullable=True)
       used_order_id = Column(Integer, nullable=True)
       created_at = Column(DateTime, server_default=func.now())
   ```

**Files**:
- `backend/src/models/__init__.py`
- `backend/src/models/account.py`
- `backend/src/models/product.py`
- `backend/src/models/card_key.py`

**Validation**:
- [ ] 模型定义正确
- [ ] 关系定义正确

---

### T008: 创建订单、消息、告警模型

**Purpose**: 创建业务数据模型

**Steps**:
1. 创建 `backend/src/models/order.py`:
   ```python
   class OrderStatus(str, enum.Enum):
       PENDING = "pending"
       PAID = "paid"
       SHIPPED = "shipped"
       COMPLETED = "completed"

   class Order(Base):
       __tablename__ = "orders"

       id = Column(Integer, primary_key=True, index=True)
       account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
       product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
       xianyu_order_id = Column(String(100), nullable=True)
       buyer_nickname = Column(String(100), nullable=False)
       status = Column(String(20), default="pending")
       card_key_id = Column(Integer, nullable=True)
       amount = Column(Numeric(10, 2), nullable=False)
       created_at = Column(DateTime, server_default=func.now())
       paid_at = Column(DateTime, nullable=True)
       shipped_at = Column(DateTime, nullable=True)
   ```
2. 创建 `backend/src/models/message.py`:
   ```python
   class Message(Base):
       __tablename__ = "messages"

       id = Column(Integer, primary_key=True, index=True)
       account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
       xianyu_message_id = Column(String(100), nullable=True)
       from_user = Column(String(100), nullable=False)
       to_user = Column(String(100), nullable=False)
       content = Column(Text, nullable=False)
       is_read = Column(Boolean, default=False)
       reply_content = Column(Text, nullable=True)
       created_at = Column(DateTime, server_default=func.now())
   ```
3. 创建 `backend/src/models/alert.py`:
   ```python
   class AlertType(str, enum.Enum):
       LOGIN_EXPIRED = "login_expired"
       SHIP_FAILED = "ship_failed"
       LOW_STOCK = "low_stock"
       SYSTEM_ERROR = "system_error"

   class Alert(Base):
       __tablename__ = "alerts"

       id = Column(Integer, primary_key=True, index=True)
       type = Column(String(50), nullable=False)
       content = Column(Text, nullable=False)
       account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
       is_resolved = Column(Boolean, default=False)
       created_at = Column(DateTime, server_default=func.now())
   ```

**Files**:
- `backend/src/models/order.py`
- `backend/src/models/message.py`
- `backend/src/models/alert.py`

**Validation**:
- [ ] 模型定义正确
- [ ] 外键关系正确

---

### T009: 创建配置、日志、黑名单模型

**Purpose**: 创建系统数据模型

**Steps**:
1. 创建 `backend/src/models/settings.py`:
   ```python
   class Setting(Base):
       __tablename__ = "settings"

       id = Column(Integer, primary_key=True, index=True)
       key = Column(String(100), unique=True, nullable=False)
       value = Column(Text, nullable=True)
       updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
   ```
2. 创建 `backend/src/models/blacklist.py`:
   ```python
   class Blacklist(Base):
       __tablename__ = "blacklist"

       id = Column(Integer, primary_key=True, index=True)
       nickname = Column(String(100), unique=True, nullable=False)
       reason = Column(Text, nullable=True)
       created_at = Column(DateTime, server_default=func.now())
   ```
3. 创建 `backend/src/models/log.py`:
   ```python
   class LogLevel(str, enum.Enum):
       INFO = "info"
       WARNING = "warning"
       ERROR = "error"

   class LogCategory(str, enum.Enum):
       TASK = "task"
       MESSAGE = "message"
       SHIP = "ship"
       SYSTEM = "system"

   class Log(Base):
       __tablename__ = "logs"

       id = Column(Integer, primary_key=True, index=True)
       level = Column(String(20), nullable=False)
       category = Column(String(50), nullable=False)
       content = Column(Text, nullable=False)
       account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
       created_at = Column(DateTime, server_default=func.now())
   ```

**Files**:
- `backend/src/models/settings.py`
- `backend/src/models/blacklist.py`
- `backend/src/models/log.py`

**Validation**:
- [ ] 所有模型创建完成

---

### T010: 执行首次数据库迁移

**Purpose**: 创建数据库表

**Steps**:
1. 生成迁移文件:
   ```bash
   cd backend
   alembic revision --autogenerate -m "initial migration"
   ```
2. 执行迁移:
   ```bash
   alembic upgrade head
   ```
3. 验证表创建:
   ```bash
   alembic current
   psql -h localhost -U xianyu -d xianyu_auto -c "\dt"
   ```

**Validation**:
- [ ] 迁移成功执行
- [ ] 9张表全部创建
- [ ] 索引创建正确

---

## Definition of Done

- [ ] SQLAlchemy 配置正确
- [ ] 所有 9 个数据模型创建完成
- [ ] Alembic 迁移成功执行
- [ ] 数据库表创建正确

## Dependencies

- WP01: 项目基础设置

## Risks

- PostgreSQL 连接配置
- 迁移冲突处理

## Reviewer Guidance

1. 检查模型字段类型是否正确
2. 检查外键关系是否正确
3. 检查索引是否合理

## Implementation Command

```bash
# 依赖 WP01
spec-kitty implement WP02 --base WP01
```

## Activity Log

- 2026-03-05T06:50:30Z – claude-code – shell_pid=35376 – lane=doing – Assigned agent via workflow command
- 2026-03-05T06:55:31Z – claude-code – shell_pid=35376 – lane=for_review – Ready for review: 数据库模型和迁移已完成
- 2026-03-05T07:59:43Z – claude-code – shell_pid=48896 – lane=doing – Started review via workflow command
