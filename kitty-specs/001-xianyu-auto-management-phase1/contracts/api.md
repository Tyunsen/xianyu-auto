# API Contracts: 闲鱼自动管理系统

## REST API 设计

---

## 账号管理 API

### 获取账号列表

```
GET /api/accounts

Response 200:
{
  "items": [
    {
      "id": 1,
      "nickname": "卖家昵称",
      "status": "online",
      "last_login": "2026-03-05T10:00:00Z"
    }
  ],
  "total": 1
}
```

### 添加账号

```
POST /api/accounts

Request:
{
  "nickname": "卖家昵称"
}

Response 201:
{
  "id": 1,
  "nickname": "卖家昵称",
  "status": "pending_login",
  "message": "请在弹出的浏览器中完成登录"
}
```

### 删除账号

```
DELETE /api/accounts/{id}

Response 204: No Content
```

### 检查账号登录状态

```
POST /api/accounts/{id}/check-status

Response 200:
{
  "status": "online",
  "last_check": "2026-03-05T10:00:00Z"
}
```

---

## 商品管理 API

### 获取商品列表

```
GET /api/products?status=published&page=1&page_size=20

Response 200:
{
  "items": [
    {
      "id": 1,
      "title": "商品标题",
      "price": 99.00,
      "status": "published",
      "images": ["url1", "url2"],
      "created_at": "2026-03-05T10:00:00Z"
    }
  ],
  "total": 100
}
```

### 添加商品

```
POST /api/products

Request:
{
  "title": "商品标题",
  "price": 99.00,
  "description": "商品描述",
  "images": ["url1", "url2"]
}

Response 201:
{
  "id": 1,
  "title": "商品标题",
  "price": 99.00,
  "status": "draft"
}
```

### 修改商品

```
PUT /api/products/{id}

Request:
{
  "title": "新标题",
  "price": 88.00
}

Response 200:
{
  "id": 1,
  "title": "新标题",
  "price": 88.00
}
```

### 删除商品

```
DELETE /api/products/{id}

Response 204: No Content
```

### 上架商品

```
POST /api/products/{id}/publish

Response 200:
{
  "id": 1,
  "status": "published",
  "xianyu_id": "xy123456"
}
```

### 下架商品

```
POST /api/products/{id}/unpublish

Response 200:
{
  "id": 1,
  "status": "offline"
}
```

### 批量导入商品

```
POST /api/products/import

Request (multipart/form-data):
file: CSV/Excel文件

Response 201:
{
  "imported": 50,
  "failed": 0,
  "errors": []
}
```

---

## 卡密管理 API

### 获取卡密列表

```
GET /api/card-keys?product_id=1&status=available

Response 200:
{
  "items": [
    {
      "id": 1,
      "key": "XXXX-XXXX-XXXX",
      "product_id": 1,
      "status": "available"
    }
  ],
  "total": 100,
  "available_count": 80
}
```

### 添加卡密

```
POST /api/card-keys

Request:
{
  "key": "XXXX-XXXX-XXXX",
  "product_id": 1
}

Response 201:
{
  "id": 1,
  "key": "XXXX-XXXX-XXXX",
  "product_id": 1,
  "status": "available"
}
```

### 批量导入卡密

```
POST /api/card-keys/import

Request (multipart/form-data):
file: CSV/Excel文件
product_id: 1

Response 201:
{
  "imported": 100,
  "failed": 0
}
```

### 删除卡密

```
DELETE /api/card-keys/{id}

Response 204: No Content
```

---

## 订单管理 API

### 获取订单列表

```
GET /api/orders?status=paid&page=1

Response 200:
{
  "items": [
    {
      "id": 1,
      "xianyu_order_id": "order123",
      "buyer_nickname": "买家昵称",
      "product_id": 1,
      "status": "paid",
      "amount": 99.00,
      "paid_at": "2026-03-05T10:00:00Z"
    }
  ],
  "total": 50
}
```

### 手动发货

```
POST /api/orders/{id}/ship

Response 200:
{
  "id": 1,
  "status": "shipped",
  "shipped_at": "2026-03-05T10:05:00Z"
}
```

---

## 消息管理 API

### 获取消息列表

```
GET /api/messages?account_id=1&is_read=false

Response 200:
{
  "items": [
    {
      "id": 1,
      "account_id": 1,
      "from_user": "买家昵称",
      "content": "这个商品怎么买？",
      "is_read": false,
      "created_at": "2026-03-05T10:00:00Z"
    }
  ],
  "total": 10
}
```

### 获取对话记录

```
GET /api/messages/conversation?account_id=1&user=买家昵称

Response 200:
{
  "messages": [
    {
      "from_user": "买家昵称",
      "content": "这个商品怎么买？",
      "created_at": "2026-03-05T10:00:00Z"
    },
    {
      "from_user": "卖家昵称",
      "content": "亲爱的，这边直接拍下就会发货哦~",
      "created_at": "2026-03-05T10:01:00Z"
    }
  ]
}
```

---

## 告警管理 API

### 获取告警列表

```
GET /api/alerts?is_resolved=false

Response 200:
{
  "items": [
    {
      "id": 1,
      "type": "login_expired",
      "content": "账号登录已失效，请重新登录",
      "account_id": 1,
      "is_resolved": false,
      "created_at": "2026-03-05T10:00:00Z"
    }
  ],
  "total": 5
}
```

### 处理告警

```
POST /api/alerts/{id}/resolve

Response 200:
{
  "id": 1,
  "is_resolved": true
}
```

---

## 黑名单 API

### 获取黑名单

```
GET /api/blacklist

Response 200:
{
  "items": [
    {
      "id": 1,
      "nickname": "恶意买家",
      "reason": "骗钱",
      "created_at": "2026-03-05T10:00:00Z"
    }
  ]
}
```

### 添加黑名单

```
POST /api/blacklist

Request:
{
  "nickname": "恶意买家",
  "reason": "骗钱"
}

Response 201:
{
  "id": 1,
  "nickname": "恶意买家"
}
```

### 删除黑名单

```
DELETE /api/blacklist/{id}

Response 204: No Content
```

---

## 数据统计 API

### 获取统计概览

```
GET /api/statistics/overview?start_date=2026-01-01&end_date=2026-03-05

Response 200:
{
  "total_orders": 100,
  "total_sales": 9900.00,
  "total_products": 50,
  "total_card_keys": 1000,
  "available_card_keys": 800,
  "orders_by_day": [
    {"date": "2026-03-01", "count": 10, "amount": 990.00}
  ]
}
```

---

## 系统设置 API

### 获取设置

```
GET /api/settings

Response 200:
{
  "ai_enabled": true,
  "auto_ship_enabled": true,
  "auto_sign_enabled": true,
  "stock_warning_threshold": 10,
  "notification_email": "user@example.com"
}
```

### 更新设置

```
PUT /api/settings

Request:
{
  "ai_enabled": true,
  "auto_ship_enabled": true,
  "stock_warning_threshold": 20
}

Response 200:
{
  "ai_enabled": true,
  "auto_ship_enabled": true,
  "stock_warning_threshold": 20
}
```

---

## 日志 API

### 获取运行日志

```
GET /api/logs?level=error&category=task&page=1

Response 200:
{
  "items": [
    {
      "id": 1,
      "level": "error",
      "category": "ship",
      "content": "发货失败：卡密不足",
      "account_id": 1,
      "created_at": "2026-03-05T10:00:00Z"
    }
  ],
  "total": 1000
}
```

---

## WebSocket 实时推送

### 连接

```
WS /ws/logs
```

推送内容：
```json
{
  "type": "log",
  "data": {
    "level": "info",
    "category": "task",
    "content": "自动签到任务执行成功"
  }
}
```
