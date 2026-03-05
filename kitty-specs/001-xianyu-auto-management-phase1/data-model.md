# Data Model: 闲鱼自动管理系统

## 数据库设计

基于功能需求，设计以下数据表：

---

## 1. 账号表 (accounts)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| nickname | VARCHAR(100) | 闲鱼昵称 |
| cookies | TEXT | 登录凭证（加密存储） |
| status | VARCHAR(20) | 状态：online/offline/expired |
| last_login | TIMESTAMP | 最后登录时间 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

---

## 2. 商品表 (products)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| title | VARCHAR(200) | 商品标题 |
| price | DECIMAL(10,2) | 价格 |
| description | TEXT | 商品描述 |
| images | TEXT[] | 图片URL列表（JSON数组） |
| status | VARCHAR(20) | 状态：draft/published/offline |
| xianyu_id | VARCHAR(100) | 闲鱼商品ID |
| account_id | INTEGER | 关联账号ID |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

---

## 3. 卡密表 (card_keys)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| key | TEXT | 卡密内容 |
| product_id | INTEGER | 关联商品ID |
| status | VARCHAR(20) | 状态：available/used |
| used_at | TIMESTAMP | 使用时间 |
| used_order_id | INTEGER | 使用的订单ID |
| created_at | TIMESTAMP | 创建时间 |

---

## 4. 订单表 (orders)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| account_id | INTEGER | 关联账号ID |
| product_id | INTEGER | 关联商品ID |
| xianyu_order_id | VARCHAR(100) | 闲鱼订单ID |
| buyer_nickname | VARCHAR(100) | 买家昵称 |
| status | VARCHAR(20) | 状态：pending/paid/shipped/completed |
| card_key_id | INTEGER | 使用的卡密ID |
| amount | DECIMAL(10,2) | 订单金额 |
| created_at | TIMESTAMP | 创建时间 |
| paid_at | TIMESTAMP | 付款时间 |
| shipped_at | TIMESTAMP | 发货时间 |

---

## 5. 消息表 (messages)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| account_id | INTEGER | 关联账号ID |
| xianyu_message_id | VARCHAR(100) | 闲鱼消息ID |
| from_user | VARCHAR(100) | 发送者 |
| to_user | VARCHAR(100) | 接收者 |
| content | TEXT | 消息内容 |
| is_read | BOOLEAN | 是否已读 |
| reply_content | TEXT | 回复内容（AI生成） |
| created_at | TIMESTAMP | 创建时间 |

---

## 6. 告警表 (alerts)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| type | VARCHAR(50) | 类型：login_expired/ship_failed/low_stock等 |
| content | TEXT | 告警内容 |
| account_id | INTEGER | 关联账号ID（可为空） |
| is_resolved | BOOLEAN | 是否已处理 |
| created_at | TIMESTAMP | 创建时间 |

---

## 7. 黑名单表 (blacklist)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| nickname | VARCHAR(100) | 买家昵称 |
| reason | TEXT | 拉黑原因 |
| created_at | TIMESTAMP | 创建时间 |

---

## 8. 系统配置表 (settings)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| key | VARCHAR(100) | 配置键 |
| value | TEXT | 配置值 |
| updated_at | TIMESTAMP | 更新时间 |

---

## 9. 运行日志表 (logs)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| level | VARCHAR(20) | 日志级别：info/warning/error |
| category | VARCHAR(50) | 分类：task/message/ship等 |
| content | TEXT | 日志内容 |
| account_id | INTEGER | 关联账号ID（可为空） |
| created_at | TIMESTAMP | 创建时间 |

---

## 实体关系

```
Account (1) ----< (N) Product
Account (1) ----< (N) Order
Account (1) ----< (N) Message
Product (1) ----< (N) CardKey
Product (1) ----< (N) Order
Order (1) ----< (1) CardKey
```

---

## 索引设计

- accounts.status
- products.account_id
- products.status
- card_keys.product_id
- card_keys.status
- orders.account_id
- orders.status
- messages.account_id
- messages.is_read
- alerts.type
- alerts.is_resolved
- logs.category
- logs.created_at
