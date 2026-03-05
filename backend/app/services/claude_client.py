"""
Claude Code 调用封装
"""
import subprocess
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ClaudeClient:
    """Claude Code 客户端"""

    def __init__(self):
        self.api_key = settings.claude_api_key

    async def call(self, prompt: str, system_prompt: str = "") -> str:
        """
        调用 Claude Code 生成回复

        Args:
            prompt: 用户消息
            system_prompt: 系统提示词

        Returns:
            AI生成的回复内容
        """
        try:
            # 构建完整的prompt
            full_prompt = f"{system_prompt}\n\n用户消息: {prompt}\n\n请生成合适的回复:" if system_prompt else prompt

            # 调用Claude Code CLI
            result = await self._run_claude(full_prompt)

            return result

        except Exception as e:
            logger.error(f"Claude调用失败: {e}")
            return "抱歉，我现在无法回答，请稍后再试。"

    async def _run_claude(self, prompt: str) -> str:
        """执行 Claude Code 命令"""
        # 使用subprocess运行claude命令
        process = await asyncio.create_subprocess_exec(
            "claude",
            "-p",
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.error(f"Claude命令执行失败: {stderr.decode()}")
            return "抱歉，处理失败。"

        return stdout.decode().strip()

    async def generate_reply(
        self,
        message: str,
        context: Dict[str, Any] = None,
        product_info: Dict[str, Any] = None
    ) -> str:
        """
        生成消息回复

        Args:
            message: 用户消息
            context: 对话上下文
            product_info: 商品信息

        Returns:
            生成的回复
        """
        # 构建系统提示词
        system_prompt = self._build_system_prompt(product_info)

        # 添加上下文信息
        if context:
            prompt = f"""商品信息: {json.dumps(product_info, ensure_ascii=False) if product_info else '无'}
商品描述: {product_info.get('description', '') if product_info else ''}
商品价格: {product_info.get('price', '') / 100 if product_info and product_info.get('price') else ''}元

用户消息: {message}

请根据以上信息，以咸鱼卖家的身份回复用户。回复要简洁友好。"""

        else:
            prompt = f"""用户消息: {message}

请以咸鱼卖家的身份回复用户。回复要简洁友好。"""

        return await self.call(prompt, system_prompt)

    def _build_system_prompt(self, product_info: Dict = None) -> str:
        """构建系统提示词"""
        base_prompt = """你是一个咸鱼二手平台的卖家客服。
- 回复要简洁、口语化
- 态度友好但不过分热情
- 如果用户问价，可以适当优惠
- 如果缺货/缺货，要如实告知
- 不要编造信息"""

        if product_info:
            base_prompt += f"""
商品信息:
- 名称: {product_info.get('title', '')}
- 价格: {product_info.get('price', 0) / 100}元
- 描述: {product_info.get('description', '')}
- 库存: {product_info.get('stock', 0)}"""

        return base_prompt


# 全局客户端实例
claude_client = ClaudeClient()
