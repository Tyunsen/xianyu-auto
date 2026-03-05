#!/usr/bin/env python
"""
闲鱼登录状态检测脚本 - 支持多账号

使用方法:
    python scripts/check_login_status.py [账号名称]

示例:
    python scripts/check_login_status.py          # 检测所有账号
    python scripts/check_login_status.py 账号1   # 检测指定账号

功能:
    1. 加载指定账号的Cookie
    2. 使用Playwright打开闲鱼
    3. 检测是否仍保持登录状态
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright


async def check_login_status(account_name: str = None):
    """检测登录状态"""
    print("=" * 50)
    print("闲鱼登录状态检测")
    print("=" * 50)
    print()

    cookies_dir = project_root / "cookies"
    if not cookies_dir.exists():
        print("错误: cookies 目录不存在")
        print("请先运行 extract_cookies.py 提取Cookie")
        return

    # 获取所有Cookie文件
    cookie_files = list(cookies_dir.glob("cookies_*.json"))

    if not cookie_files:
        print("错误: 没有找到任何Cookie文件")
        print("请先运行 extract_cookies.py 提取Cookie")
        return

    # 过滤指定账号
    if account_name:
        safe_name = "".join(c for c in account_name if c.isalnum() or c in ('-', '_'))
        cookie_files = [f for f in cookie_files if safe_name in f.name]

    print(f"找到 {len(cookie_files)} 个账号的Cookie")
    print()

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ]
        )

        for cookie_file in cookie_files:
            account_name = cookie_file.stem.replace("cookies_", "")
            print(f"{'='*50}")
            print(f"检测账号: {account_name}")
            print(f"{'='*50}")

            # 读取Cookie
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookie_data = json.load(f)

            cookies = cookie_data.get('cookies', [])
            if not cookies:
                print(f"  ❌ 没有Cookie")
                continue

            # 创建上下文
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                locale='zh-CN',
            )

            # 添加Cookie
            await context.add_cookies(cookies)

            # 打开闲鱼首页
            page = await context.new_page()
            await page.goto("https://www.goofish.com/", wait_until="networkidle", timeout=15000)
            await page.wait_for_timeout(2000)

            # 检测状态
            current_url = page.url

            if "login" in current_url.lower():
                print(f"  ❌ 登录状态: 已失效")
            elif "goofish.com" in current_url:
                print(f"  ✅ 登录状态: 正常")
            else:
                print(f"  ⚠️  状态: 未知 ({current_url})")

            await page.close()
            await context.close()

        print()
        print("=" * 50)
        print("检测完成")
        print("=" * 50)

        input("按回车键关闭浏览器...")
        await browser.close()


if __name__ == "__main__":
    account_name = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        asyncio.run(check_login_status(account_name))
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
