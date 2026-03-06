# Data Model: 网页端咸鱼扫码登录

## 核心实体

### Account (账号)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto-increment | 主键 |
| nickname | String(100) | NOT NULL | 账号昵称 |
| cookies | Text | NOT NULL, Encrypted | 加密存储的Cookie |
| status | String(20) | Default: "offline" | 账号状态 |
| last_login | DateTime | Nullable | 最后登录时间 |
| created_at | DateTime | Auto | 创建时间 |
| updated_at | DateTime | Auto | 更新时间 |

**- `online`状态枚举**:
 - 在线（Cookie有效）
- `offline` - 离线（未登录）
- `expired` - 过期（Cookie失效）
- `error` - 错误（登录异常）

### 状态转换

```
[创建账号]
    ↓
[offline] ---点击扫码登录---> [等待扫码]
    ↑                              ↓
    ↑                        [登录成功] ---> [online]
    ↑                              ↓
    ↑                        [登录失败/超时] --->
    ↑                              ↓
[定时检测] ---Cookie失效---> [expired]
    ↑                              ↓
    ↑                        [重新登录成功]---> [online]
```

## API 数据结构

### 账号列表响应
```typescript
interface Account {
  id: number
  nickname: string
  status: "online" | "offline" | "expired" | "error"
  last_login: string | null  // ISO格式
  created_at: string
  updated_at: string | null
}
```

### 二维码登录响应
```typescript
// Start QR Login Response
interface QRLoginStartResponse {
  success: boolean
  qr_code: string          // base64编码的PNG图片
  message: string
}

// Check QR Login Response
interface QRLoginCheckResponse {
  success: boolean
  status: "waiting" | "success" | "error"
  message: string
}
```

## 关系

- Account 与 Alert: 一对多（一个账号可以有多个告警）
- Account 与 LoginSession: 一对多（一个账号可以有多次登录记录）

## 现有代码

数据模型已在 `backend/src/models/account.py` 中实现，API Schema 在 `backend/src/schemas/account.py` 中定义。
