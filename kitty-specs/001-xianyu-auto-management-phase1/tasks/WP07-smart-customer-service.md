---
work_package_id: WP07
title: 智能客服（CC）模块
lane: "doing"
dependencies: [WP02, WP03]
base_branch: 001-xianyu-auto-management-phase1-WP06
base_commit: 31f8fa3aa53dc4f6f21cb114412c4dfae9eb6f6d
created_at: '2026-03-05T07:12:31.927386+00:00'
subtasks: [T028, T029, T030, T031, T032]
shell_pid: "49536"
agent: "claude-code"
history:
- date: '2026-03-05'
  action: created
---

# WP07: 智能客服（CC）模块

## Objective

实现 AI 智能客服功能，包括消息检测、AI 回复生成、自动回复。

## Subtasks

### T028: 创建消息 API 路由

**Steps**:
1. 创建 schemas/message.py
2. 创建 api/messages.py:
   - GET /api/messages - 消息列表
   - GET /api/messages/conversation - 对话记录
   - POST /api/messages/{id}/reply - 手动回复

### T029: 实现消息检测服务

**Steps**:
```python
class MessageDetector:
    async def check_new_messages(self, account_id: int):
        """检查新消息"""
        # 每30分钟检查一次
        # 返回新消息列表
```

### T030: 集成 MiniMax AI

**Steps**:
1. 创建 `backend/src/ai/minimax.py`:
   ```python
   from openai import OpenAI

   class MiniMaxClient:
       def __init__(self):
           self.api_key = os.getenv("MINIMAX_API_KEY")
           self.model = os.getenv("MINIMAX_MODEL", "abab6.5s")
           self.client = OpenAI(
               api_key=self.api_key,
               base_url="https://api.minimax.chat/v1"
           )

       async def generate_reply(self, messages: list) -> str:
           """生成回复内容"""
           response = self.client.chat.completions.create(
               model=self.model,
               messages=messages
           )
           return response.choices[0].message.content
   ```

### T031: 实现自动回复逻辑

**Steps**:
```python
async def auto_reply(message_id: int):
    # 1. 获取对话上下文
    # 2. 调用 AI 生成回复
    # 3. 发送回复
    # 4. 保存回复记录
```

### T032: 实现回复记录保存

**Steps**:
1. 保存原始消息
2. 保存 AI 生成的回复
3. 记录时间戳

## Dependencies

- WP02: 数据库模型
- WP03: 账号管理

## Implementation Command

```bash
spec-kitty implement WP07 --base WP03
```

## Activity Log

- 2026-03-05T07:12:33Z – claude-code – shell_pid=10960 – lane=doing – Assigned agent via workflow command
- 2026-03-05T07:17:14Z – claude-code – shell_pid=10960 – lane=for_review – Ready for review: 智能客服模块已完成
- 2026-03-05T08:02:49Z – claude-code – shell_pid=49536 – lane=doing – Started review via workflow command
