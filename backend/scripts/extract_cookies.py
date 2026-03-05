#!/usr/bin/env python
"""
闲鱼Cookie提取脚本 - 支持多账号

使用方法:
    python scripts/extract_cookies.py [账号名称]

示例:
    python scripts/extract_cookies.py          # 交互式选择账号
    python scripts/extract_cookies.py 账号1   # 为指定账号提取Cookie

功能:
    1. 启动浏览器打开闲鱼登录页面
    2. 等待用户扫码登录
    3. 登录成功后自动提取Cookie
    4. 保存到对应账号的 cookies_{账号名}.json 文件
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright


# 闲鱼域名
XIANYU_DOMAINS = [
    "goofish.com",
    "2.taobao.com",
    "taobao.com",
    "alicdn.com",
]


async def extract_cookies(account_name: str = "default"):
    """提取Cookie主函数"""
    print("=" * 50)
    print(f"闲鱼Cookie提取工具 - 账号: {account_name}")
    print("=" * 50)
    print()
    print("将执行以下操作:")
    print("1. 启动浏览器打开闲鱼首页")
    print("2. 点击登录按钮，等待扫码")
    print("3. 登录成功后，Cookie自动提取并保存")
    print()

    async with async_playwright() as p:
        # 启动浏览器（非headless模式）
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ]
        )

        # 创建上下文
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            locale='zh-CN',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # 创建页面
        page = await context.new_page()

        # 打开闲鱼首页
        print("正在打开闲鱼首页...")
        await page.goto("https://www.goofish.com/", wait_until="networkidle")

        # 等待页面加载
        print("等待页面加载...")
        await page.wait_for_timeout(2000)

        # 尝试点击登录按钮
        try:
            login_btn = page.get_by_text("登录").first()
            await login_btn.click()
            print("已点击登录按钮")
            await page.wait_for_timeout(2000)
        except Exception as e:
            print(f"自动点击登录按钮失败: {e}")
            print("请手动点击登录按钮")

        print()
        print("=" * 50)
        print("请在浏览器中完成登录（支付宝扫码）...")
        print("登录成功后，程序会自动检测并提取Cookie")
        print("=" * 50)
        print()

        # 等待用户登录，检测登录成功
        max_wait_seconds = 300  # 最多等待5分钟
        check_interval = 3

        logged_in = False
        for i in range(max_wait_seconds // check_interval):
            await page.wait_for_timeout(check_interval * 1000)

            current_url = page.url

            # 检查是否跳转到闲鱼首页（登录成功）
            if "goofish.com" in current_url and "login" not in current_url.lower():
                logged_in = True
                print(f"检测到登录成功! 当前URL: {current_url}")
                break

            # 显示等待状态
            if (i + 1) % 10 == 0:
                print(f"等待登录中... ({ (i + 1) * check_interval }秒)")

        if not logged_in:
            print()
            print("-" * 50)
            print("未检测到登录成功，请重试")
            input("按回车键退出...")
        else:
            # 等待确保Cookie完全加载
            await page.wait_for_timeout(2000)

            # 提取Cookie
            cookies = await context.cookies()

            # 过滤闲鱼相关的Cookie
            xianyu_cookies = [
                cookie for cookie in cookies
                if any(domain in cookie.get('domain', '') for domain in XIANYU_DOMAINS)
            ]

            print()
            print("=" * 50)
            print(f"提取到 {len(xianyu_cookies)} 个Cookie")
            print("=" * 50)

            # 生成安全的文件名
            safe_name = "".join(c for c in account_name if c.isalnum() or c in ('-', '_'))

            # 保存到文件
            output_file = project_root / "cookies" / f"cookies_{safe_name}.json"
            output_file.parent.mkdir(exist_ok=True)

            cookie_data = {
                "account_name": account_name,
                "cookies": xianyu_cookies,
                "extracted_at": str(Path(__file__).stat().st_mtime) if False else None,
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cookie_data, f, indent=2, ensure_ascii=False)

            print()
            print(f"Cookie已保存到: {output_file}")

            # 打印JSON格式
            print()
            print("=" * 50)
            print("JSON格式 (可用于代码):")
            print("=" * 50)
            print(json.dumps(xianyu_cookies, indent=2, ensure_ascii=False)[:500] + "...")

            print()
            print("提取完成!")
            input("按回车键关闭浏览器...")

        await browser.close()


if __name__ == "__main__":
    # 获取账号名称
    account_name = sys.argv[1] if len(sys.argv) > 1 else "default"

    try:
        asyncio.run(extract_cookies(account_name))
    except KeyboardInterrupt:
        print("\n\n已取消操作")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
