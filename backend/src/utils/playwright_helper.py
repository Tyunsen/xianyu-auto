"""
Playwright 浏览器自动化辅助工具
用于闲鱼登录和登录状态检测（二维码登录方案）
"""
import asyncio
import json
import base64
import logging
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright

logger = logging.getLogger(__name__)

# 闲鱼登录URL（二维码登录）
XIANYU_LOGIN_URL = "https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fseller2.xianyu.com%2F"
XIANYU_HOME_URL = "https://seller2.xianyu.com"


class PlaywrightHelper:
    """Playwright 浏览器辅助类"""

    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.contexts: Dict[int, BrowserContext] = {}  # account_id -> context
        self.login_pages: Dict[int, Page] = {}  # account_id -> page

    async def initialize(self):
        """初始化 Playwright（无头模式）"""
        if self.playwright is None:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,  # 无头模式，服务器不需要显示器
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                ]
            )
            logger.info("Playwright 浏览器已启动（无头模式）")

    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Playwright 浏览器已关闭")

    async def start_qr_login(self, account_id: int) -> Dict[str, Any]:
        """
        开始二维码登录流程

        Returns:
            包含二维码图片base64的字典
        """
        if not self.browser:
            await self.initialize()

        # 关闭之前的上下文（如果存在）
        if account_id in self.contexts:
            await self.contexts[account_id].close()
        if account_id in self.login_pages:
            await self.login_pages[account_id].close()

        # 创建新的浏览器上下文
        context = await self.browser.new_context(
            viewport={'width': 400, 'height': 500},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.contexts[account_id] = context

        # 打开登录页面
        page = await context.new_page()
        self.login_pages[account_id] = page

        # 导航到登录页面
        await page.goto(XIANYU_LOGIN_URL)

        # 等待二维码加载
        await page.wait_for_timeout(2000)

        # 查找二维码图片
        qr_code_data = None

        # 方法1: 查找二维码图片元素
        try:
            qr_img = page.locator('img.qrcode, #qrcode img, .login-qrcode img, img[alt*="QR"]').first
            if await qr_img.count() > 0:
                qr_code_data = await qr_img.get_attribute('src')
                if qr_code_data and qr_code_data.startswith('data:image'):
                    logger.info(f"找到二维码图片（base64）")
        except Exception as e:
            logger.debug(f"方法1查找二维码失败: {e}")

        # 方法2: 查找canvas元素
        if not qr_code_data:
            try:
                canvas = page.locator('canvas#qrcode, canvas.login-qrcode').first
                if await canvas.count() > 0:
                    qr_code_data = await canvas.evaluate('(el) => el.toDataURL()')
                    logger.info(f"找到二维码canvas")
            except Exception as e:
                logger.debug(f"方法2查找canvas失败: {e}")

        # 方法3: 截取整个登录页面
        if not qr_code_data:
            try:
                # 等待页面稳定
                await page.wait_for_timeout(1000)
                # 截图
                screenshot = await page.screenshot()
                qr_code_data = f"data:image/png;base64,{base64.b64encode(screenshot).decode()}"
                logger.info(f"使用页面截图作为二维码")
            except Exception as e:
                logger.error(f"截图失败: {e}")

        if not qr_code_data:
            return {
                "success": False,
                "message": "无法获取二维码，请重试"
            }

        logger.info(f"为账号 {account_id} 生成了二维码")

        return {
            "success": True,
            "qr_code": qr_code_data,
            "message": "请使用闲鱼APP扫码登录"
        }

    async def check_qr_login_status(self, account_id: int) -> Dict[str, Any]:
        """
        检查二维码登录状态

        Returns:
            登录状态信息
        """
        if account_id not in self.login_pages:
            return {
                "status": "error",
                "message": "没有登录会话",
                "cookies": None
            }

        page = self.login_pages[account_id]

        try:
            # 检查是否跳转到登录后的页面
            current_url = page.url
            logger.debug(f"当前URL: {current_url}")

            # 如果URL包含seller2.xianyu.com或者不包含login，说明登录成功
            if 'seller2.xianyu.com' in current_url or ('login' not in current_url.lower()):
                # 获取Cookie
                context = self.contexts[account_id]
                cookies = await context.cookies()
                cookie_json = json.dumps(cookies, ensure_ascii=False)

                logger.info(f"账号 {account_id} 扫码登录成功")
                return {
                    "status": "success",
                    "message": "登录成功",
                    "cookies": cookie_json
                }

            # 检查页面是否有用户信息（另一种登录成功的标志）
            try:
                await page.wait_for_selector('.user-nick, .nick-name, [class*="user"]', timeout=1000)
                context = self.contexts[account_id]
                cookies = await context.cookies()
                cookie_json = json.dumps(cookies, ensure_ascii=False)

                logger.info(f"账号 {account_id} 扫码登录成功（检测到用户信息）")
                return {
                    "status": "success",
                    "message": "登录成功",
                    "cookies": cookie_json
                }
            except Exception:
                pass

            # 等待后继续轮询
            return {
                "status": "waiting",
                "message": "等待扫码中...",
                "cookies": None
            }

        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            return {
                "status": "error",
                "message": str(e),
                "cookies": None
            }

    async def close_login(self, account_id: int):
        """关闭登录会话"""
        if account_id in self.login_pages:
            await self.login_pages[account_id].close()
            del self.login_pages[account_id]
        if account_id in self.contexts:
            await self.contexts[account_id].close()
            del self.contexts[account_id]
        logger.info(f"关闭了账号 {account_id} 的登录会话")

    async def get_cookies(self, account_id: int) -> Optional[str]:
        """获取指定账号的Cookie"""
        if account_id not in self.contexts:
            logger.warning(f"账号 {account_id} 没有浏览器上下文")
            return None

        context = self.contexts[account_id]
        cookies = await context.cookies()
        cookie_json = json.dumps(cookies, ensure_ascii=False)
        logger.info(f"获取到账号 {account_id} 的 {len(cookies)} 个 Cookie")

        return cookie_json

    async def close_context(self, account_id: int):
        """关闭指定账号的浏览器上下文"""
        await self.close_login(account_id)

    async def check_login_status(self, cookies_str: str) -> Dict[str, Any]:
        """检查登录状态（通过Cookie）"""
        if not self.browser:
            await self.initialize()

        try:
            context = await self.browser.new_context()
            cookies = json.loads(cookies_str)
            await context.add_cookies(cookies)

            page = await context.new_page()
            await page.goto(XIANYU_HOME_URL)
            await page.wait_for_load_state("networkidle")

            current_url = page.url

            if "login" in current_url.lower():
                await context.close()
                return {"status": "expired", "message": "登录已过期"}

            try:
                await page.wait_for_selector(".user-nick", timeout=3000)
                await context.close()
                return {"status": "online", "message": "账号在线"}
            except Exception:
                pass

            await context.close()
            return {"status": "unknown", "message": "无法确定登录状态"}

        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            return {"status": "error", "message": str(e)}


# 全局实例
_playwright_helper: Optional[PlaywrightHelper] = None


def get_playwright_helper() -> PlaywrightHelper:
    """获取 Playwright 辅助实例"""
    global _playwright_helper
    if _playwright_helper is None:
        _playwright_helper = PlaywrightHelper()
    return _playwright_helper


async def cleanup_playwright():
    """清理 Playwright 资源"""
    global _playwright_helper
    if _playwright_helper:
        await _playwright_helper.close()
        _playwright_helper = None
