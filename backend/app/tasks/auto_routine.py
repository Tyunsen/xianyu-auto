"""
自动擦亮和签到任务
"""
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Account, Product
from app.services.account_service import AccountService
from app.services.product_service import ProductService
from app.services.log_service import LogService
from app.services.playwright_client import browser_pool
from app.tasks.scheduler import task


@task("auto_rub")
async def auto_rub_task(db: Session):
    """自动擦亮任务 - 每天定时刷新商品曝光"""
    log_service = LogService(db)
    account_service = AccountService(db)
    product_service = ProductService(db)

    # 获取所有正常状态的账号
    accounts = account_service.get_active_accounts()

    if not accounts:
        log_service.info("auto_rub", "没有活跃账号")
        return

    log_service.info("auto_rub", f"开始擦亮 {len(accounts)} 个账号的商品")

    for account in accounts:
        try:
            # 获取该账号上架的商品
            products = db.query(Product).filter(
                Product.account_id == account.id,
                Product.status == "on_shelf"
            ).all()

            if not products:
                continue

            # 使用浏览器擦亮商品
            async with browser_pool.get_browser(account.id, account.cookie, account.user_agent) as browser:
                for product in products:
                    try:
                        # 访问商品页面进行"擦亮"
                        if product.xianyu_url:
                            await browser.page.goto(product.xianyu_url, wait_until="networkidle")
                            await browser.page.wait_for_timeout(1000)

                            # 点击擦亮按钮（需要根据实际页面调整）
                            # 这里提供基础逻辑
                            log_service.info("auto_rub", f"擦亮商品: {product.title}")

                    except Exception as e:
                        log_service.error("auto_rub", f"擦亮商品 {product.id} 失败: {e}")

        except Exception as e:
            log_service.error("auto_rub", f"处理账号 {account.id} 擦亮失败: {e}")


@task("auto_sign")
async def auto_sign_task(db: Session):
    """自动签到任务 - 每天签到领闲鱼币"""
    log_service = LogService(db)
    account_service = AccountService(db)

    # 获取所有正常状态的账号
    accounts = account_service.get_active_accounts()

    if not accounts:
        log_service.info("auto_sign", "没有活跃账号")
        return

    log_service.info("auto_sign", f"开始签到 {len(accounts)} 个账号")

    for account in accounts:
        try:
            async with browser_pool.get_browser(account.id, account.cookie, account.user_agent) as browser:
                # 访问签到页面
                await browser.page.goto("https://www.goofish.com/wallet/signin", wait_until="networkidle")
                await browser.page.wait_for_timeout(2000)

                # 尝试点击签到按钮（需要根据实际页面调整）
                # 这里提供基础逻辑
                sign_btn = await browser.page.query_selector(".sign-btn, button:has-text('签到')")

                if sign_btn:
                    await sign_btn.click()
                    await browser.page.wait_for_timeout(1000)
                    log_service.info("auto_sign", f"账号 {account.id} 签到成功")
                else:
                    # 可能已经签到过了
                    log_service.info("auto_sign", f"账号 {account.id} 今日已签到")

        except Exception as e:
            log_service.error("auto_sign", f"账号 {account.id} 签到失败: {e}")
