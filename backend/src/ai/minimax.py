"""
MiniMax AI 客户端
"""
import os
from typing import List, Dict, Optional
from openai import OpenAI


class MiniMaxClient:
    """MiniMax AI 客户端"""

    def __init__(self):
        """初始化客户端"""
        self.api_key = os.getenv("MINIMAX_API_KEY")
        self.model = os.getenv("MINIMAX_MODEL", "abab6.5s")

        if not self.api_key:
            raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.minimax.chat/v1"
        )

    def generate_reply(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        生成回复内容

        Args:
            messages: 对话历史消息列表 [{"role": "user", "content": "..."}]
            system_prompt: 系统提示词

        Returns:
            AI 生成的回复内容
        """
        # 构建消息列表
        chat_messages = []

        if system_prompt:
            chat_messages.append({
                "role": "system",
                "content": system_prompt
            })

        chat_messages.extend(messages)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"MiniMax API 调用失败: {e}")
            return "抱歉，我现在无法回答您的问题，请稍后再试。"

    def generate_customer_service_reply(
        self,
        conversation_history: List[Dict[str, str]],
        product_info: Optional[str] = None
    ) -> str:
        """
        生成客服回复

        Args:
            conversation_history: 对话历史
            product_info: 商品信息（可选）

        Returns:
            客服回复
        """
        # 客服系统提示词
        system_prompt = """你是一个热情、耐心的闲鱼店铺客服。请遵循以下规则：
1. 使用简洁、友好的语言
2. 回答问题要准确，如果不确定请如实说明
3. 适当使用表情符号让对话更亲切
4. 如果是关于商品的问题，提供准确的商品信息
5. 遇到无法处理的问题，建议买家稍后再联系或联系人工客服
6. 不要做出无法兑现的承诺
"""

        # 如果有商品信息，添加到系统提示中
        if product_info:
            system_prompt += f"\n\n商品信息：{product_info}"

        return self.generate_reply(conversation_history, system_prompt)


# 全局客户端实例
_minimax_client = None


def get_minimax_client() -> MiniMaxClient:
    """获取 MiniMax 客户端实例"""
    global _minimax_client
    if _minimax_client is None:
        _minimax_client = MiniMaxClient()
    return _minimax_client
