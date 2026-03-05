# Quickstart: 项目检查与Docker部署验收

## 验收流程

### 1. 准备工作

#### 1.1 获取咸鱼Cookie（用户负责）

用户需要在Windows上获取咸鱼Cookie：

1. 在电脑浏览器访问 https://2.taobao.com 并登录
2. 按F12打开开发者工具
3. 切换到 Application(应用) → Cookies → https://2.taobao.com
4. 复制所有Cookie值发给开发者

#### 1.2 服务器准备

确保服务器已安装：
- Docker
- docker-compose

### 2. Docker部署

```bash
# 拉取最新代码
git pull

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

访问 http://localhost 查看前端页面

### 3. 验收检查

| 检查项 | 预期结果 |
|--------|----------|
| Docker服务运行 | 所有容器状态为running |
| 前端页面加载 | 无500/404错误 |
| 后端API | 返回200状态码 |
| 数据库连接 | 能正常读写数据 |

### 4. 获取Cookie后的配置

用户提供Cookie后，开发者通过API配置：

```bash
# 创建账号并设置Cookie
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"nickname": "your_nickname"}'

# 刷新Cookie
curl -X POST "http://localhost:8000/api/accounts/{id}/refresh-cookies" \
  -H "Content-Type: application/json" \
  -d '{"cookies": "your_cookie_string"}'
```

## 常见问题

### Q: Docker启动失败

A: 检查docker-compose.yml配置，确保端口未被占用

### Q: 前端页面空白

A: 检查前端Docker构建日志，确认npm run build是否成功

### Q: API请求失败

A: 检查后端日志，确认数据库连接是否正常
