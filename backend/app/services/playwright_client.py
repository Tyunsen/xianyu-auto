"""
Playwright 浏览器客户端封装
用于操作咸鱼网页版
"""
import asyncio
import json
import random
from typing import Optional, Dict, List, Any
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page, BrowserContext


class XianyuBrowser:
    """咸鱼浏览器客户端"""

    BASE_URL = "https://www.goofish.com"

    def __init__(self, account_id: int, cookie: str, user_agent: str = ""):
        self.account_id = account_id
        self.cookie = cookie
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        await self.launch()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def launch(self):
        """启动浏览器"""
        playwright = await async_playwright().start()
        # 使用有界面模式（非headless）
        self.browser = await playwright.chromium.launch(
            headless=False,  # 有界面，方便调试
            args=['--disable-blink-features=AutomationControlled']
        )
        # 创建上下文（每个账号独立）
        self.context = await self.browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1280, 'height': 720},
            locale='zh-CN'
        )
        # 设置cookie
        await self._set_cookies()
        # 创建页面
        self.page = await self.context.new_page()

    async def close(self):
        """关闭浏览器"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def _set_cookies(self):
        """设置Cookie"""
        try:
            cookies = json.loads(self.cookie) if isinstance(self.cookie, str) else self.cookie
            if isinstance(cookies, dict):
                # 兼容字典格式
                cookies = [{'name': k, 'value': v} for k, v in cookies.items()]
            await self.context.add_cookies(cookies)
        except Exception as e:
            print(f"设置Cookie失败: {e}")

    async def is_logged_in(self) -> bool:
        """检查是否已登录"""
        if not self.page:
            return False

        try:
            await self.page.goto(self.BASE_URL, wait_until="networkidle", timeout=10000)
            # 检查是否跳转到登录页
            current_url = self.page.url
            if "login" in current_url:
                return False
            # 检查是否有用户头像等登录标识
            await self.page.wait_for_timeout(2000)
            return True
        except Exception:
            return False

    async def get_messages(self) -> List[Dict[str, Any]]:
        """获取消息列表"""
        if not self.page:
            return []

        messages = []
        try:
            await self.page.goto(f"{self.BASE_URL}/im", wait_until="networkidle", timeout=15000)

            # 等待消息列表加载
            await self.page.wait_for_timeout(2000)

            # 获取消息元素（需要根据实际页面结构调整）
            # 这里提供基础逻辑
            msg_items = await self.page.query_selector_all(".message-item, .conversation-item")

            for item in msg_items:
                try:
                    # 提取消息基本信息
                    msg_data = await self._extract_message(item)
                    if msg_data:
                        messages.append(msg_data)
                except Exception:
                    continue

        except Exception as e:
            print(f"获取消息失败: {e}")

        return messages

    async def _extract_message(self, element) -> Optional[Dict]:
        """提取单条消息"""
        try:
            # 实际实现需要根据页面结构调整
            # 这里提供基础框架
            return {
                "message_id": "",
                "from_user": "",
                "content": "",
                "timestamp": datetime.now()
            }
        except Exception:
            return None

    async def send_message(self, user_id: str, content: str) -> bool:
        """发送消息"""
        if not self.page:
            return False

        try:
            # 打开聊天窗口
            await self.page.goto(f"{self.BASE_URL}/im?userId={user_id}", wait_until="networkidle")
            await self.page.wait_for_timeout(1000)

            # 输入消息
            text_area = await self.page.query_selector("textarea, input[type='text']")
            if text_area:
                await text_area.fill(content)

                # 发送
                send_btn = await self.page.query_selector("button.send, .send-btn")
                if send_btn:
                    await send_btn.click()
                    return True

        except Exception as e:
            print(f"发送消息失败: {e}")

        return False

    async def publish_product(self, product_data: Dict) -> bool:
        """发布商品"""
        if not self.page:
            return False

        try:
            # 打开发布页面
            await self.page.goto(f"{self.BASE_URL}/publish", wait_until="networkidle")
            await self.page.wait_for_timeout(2000)

            # 填写商品信息
            # 标题
            title_input = await self.page.query_selector("input[name='title']")
            if title_input:
                await title_input.fill(product_data.get("title", ""))

            # 价格
            price_input = await self.page.query_selector("input[name='price']")
            if price_input:
                await price_input.fill(str(product_data.get("price", "")))

            # 描述
            desc_input = await self.page.query_selector("textarea[name='description']")
            if desc_input:
                await desc_input.fill(product_data.get("description", ""))

            # 提交发布
            submit_btn = await self.page.query_selector("button.submit, .publish-btn")
            if submit_btn:
                await submit_btn.click()
                await self.page.wait_for_timeout(2000)
                return True

        except Exception as e:
            print(f"发布商品失败: {e}")

        return False

    async def refresh_page(self):
        """刷新页面保活"""
        if self.page:
            try:
                await self.page.reload(wait_until="networkidle")
                await self.page.wait_for_timeout(1000)
            except Exception:
                pass


# 浏览器池管理
class BrowserPool:
    """浏览器连接池（每个账号独立浏览器）"""

    def __init__(self):
        self.browsers: Dict[int, XianyuBrowser] = {}

    async def get_browser(self, account_id: int, cookie: str, user_agent: str = "") -> XianyuBrowser:
        """获取或创建浏览器实例"""
        if account_id not in self.browsers:
            self.browsers[account_id] = XianyuBrowser(account_id, cookie, user_agent)
            await self.browsers[account_id].launch()

        return self.browsers[account_id]

    async def close_browser(self, account_id: int):
        """关闭指定浏览器"""
        if account_id in self.browsers:
            await self.browsers[account_id].close()
            del self.browsers[account_id]

    async def close_all(self):
        """关闭所有浏览器"""
        for browser in self.browsers.values():
            await browser.close()
        self.browsers.clear()


# 全局浏览器池
browser_pool = BrowserPool()
