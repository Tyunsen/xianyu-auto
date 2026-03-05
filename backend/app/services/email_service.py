"""
邮件通知服务
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmailService:
    """邮件服务"""

    def __init__(self):
        self.smtp_host = getattr(settings, 'smtp_host', '')
        self.smtp_port = getattr(settings, 'smtp_port', 587)
        self.smtp_user = getattr(settings, 'smtp_user', '')
        self.smtp_password = getattr(settings, 'smtp_password', '')
        self.from_email = getattr(settings, 'from_email', self.smtp_user)
        self.to_emails = getattr(settings, 'to_emails', '').split(',')

    def is_configured(self) -> bool:
        """检查是否配置了邮件"""
        return bool(self.smtp_host and self.smtp_user and self.smtp_password)

    async def send_email(
        self,
        subject: str,
        content: str,
        to_emails: Optional[List[str]] = None
    ) -> bool:
        """
        发送邮件

        Args:
            subject: 邮件主题
            content: 邮件内容（支持HTML）
            to_emails: 收件人列表，默认使用配置中的收件人

        Returns:
            是否发送成功
        """
        if not self.is_configured():
            logger.warning("邮件未配置，跳过发送")
            return False

        if not to_emails:
            to_emails = [e.strip() for e in self.to_emails if e.strip()]

        if not to_emails:
            logger.warning("没有配置收件人")
            return False

        try:
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"咸鱼自动管理系统 <{self.from_email}>"
            msg['To'] = ', '.join(to_emails)

            # 添加HTML内容
            html_part = MIMEText(content, 'html', 'utf-8')
            msg.attach(html_part)

            # 发送邮件
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, to_emails, msg.as_string())

            logger.info(f"邮件发送成功: {subject}")
            return True

        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            return False

    async def send_alert(self, alert_type: str, title: str, content: str) -> bool:
        """发送告警邮件"""
        html_content = f"""
        <html>
        <body>
            <h2 style="color: #ff4d4f;">⚠️ 咸鱼系统告警</h2>
            <h3>{title}</h3>
            <p><strong>类型：</strong>{alert_type}</p>
            <p><strong>内容：</strong>{content}</p>
            <p><strong>时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <p style="color: #888; font-size: 12px;">此邮件由咸鱼自动管理系统发送</p>
        </body>
        </html>
        """
        from datetime import datetime
        return await self.send_email(f"【告警】{title}", html_content)

    async def send_stock_warning(self, product_title: str, stock: int) -> bool:
        """发送库存预警邮件"""
        html_content = f"""
        <html>
        <body>
            <h2 style="color: #faad14;">📦 库存预警</h2>
            <p>商品 <strong>{product_title}</strong> 库存不足！</p>
            <p>当前库存：<strong style="color: #ff4d4f;">{stock}</strong></p>
            <p>请及时补充库存！</p>
            <hr>
            <p style="color: #888; font-size: 12px;">此邮件由咸鱼自动管理系统发送</p>
        </body>
        </html>
        """
        return await self.send_email(f"【库存预警】{product_title}", html_content)

    async def send_login_expired(self, account_name: str) -> bool:
        """发送登录过期邮件"""
        html_content = f"""
        <html>
        <body>
            <h2 style="color: #ff4d4f;">🔐 账号登录过期</h2>
            <p>账号 <strong>{account_name}</strong> 的登录状态已过期！</p>
            <p>请及时更新Cookie！</p>
            <hr>
            <p style="color: #888; font-size: 12px;">此邮件由咸鱼自动管理系统发送</p>
        </body>
        </html>
        """
        return await self.send_email(f"【登录过期】{account_name}", html_content)


# 全局邮件服务
email_service = EmailService()
