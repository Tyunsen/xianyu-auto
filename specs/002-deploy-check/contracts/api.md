# API Contracts: 项目检查与Docker部署验收

本项目为部署验收项目，API接口已在主项目中定义。

## 引用API文档

请参考: [../../kitty-specs/001-xianyu-auto-management-phase1/contracts/api.md](../../kitty-specs/001-xianyu-auto-management-phase1/contracts/api.md)

## 验收检查项

### 账号API
- [ ] GET /api/accounts 返回账号列表
- [ ] POST /api/accounts 创建账号
- [ ] DELETE /api/accounts/{id} 删除账号
- [ ] POST /api/accounts/{id}/refresh-cookies 更新Cookie

### 商品API
- [ ] GET /api/products 返回商品列表
- [ ] POST /api/products 创建商品
- [ ] PUT /api/products/{id} 更新商品
- [ ] DELETE /api/products/{id} 删除商品

### 卡密API
- [ ] GET /api/card-keys 返回卡密列表
- [ ] POST /api/card-keys 创建卡密
- [ ] POST /api/card-keys/import 批量导入

### 订单API
- [ ] GET /api/orders 返回订单列表
- [ ] POST /api/orders/{id}/ship 手动发货

### 消息API
- [ ] GET /api/messages 返回消息列表

### 统计API
- [ ] GET /api/statistics/overview 返回统计概览

### 设置API
- [ ] GET /api/settings 获取设置
- [ ] PUT /api/settings 更新设置
