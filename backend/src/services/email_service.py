"""
邮件服务
"""
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """邮件服务"""

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = self.smtp_user

    def is_configured(self) -> bool:
        """检查邮件服务是否已配置"""
        return bool(self.smtp_host and self.smtp_user and self.smtp_password)

    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = True
    ) -> bool:
        """
        发送邮件

        Args:
            to: 收件人
            subject: 主题
            body: 内容
            html: 是否为 HTML 格式

        Returns:
            是否发送成功
        """
        if not self.is_configured():
            logger.warning("邮件服务未配置，跳过发送")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to

            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, mime_type, 'utf-8'))

            await aiosmtplib.send(
                msg,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                tls=True
            )

            logger.info(f"邮件发送成功: {to}")
            return True

        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            return False

    async def send_alert_email(
        self,
        to: str,
        alert_type: str,
        content: str
    ) -> bool:
        """
        发送告警邮件

        Args:
            to: 收件人
            alert_type: 告警类型
            content: 告警内容

        Returns:
            是否发送成功
        """
        subject = f"【闲鱼自动化】告警通知 - {alert_type}"
        body = f"""
        <html>
        <body>
            <h2>告警通知</h2>
            <p><strong>类型:</strong> {alert_type}</p>
            <p><strong>内容:</strong> {content}</p>
            <p><strong>时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <p>此邮件由闲鱼自动管理系统发送</p>
        </body>
        </html>
        """
        return await self.send_email(to, subject, body)

    async def send_daily_report(
        self,
        to: str,
        report_data: dict
    ) -> bool:
        """
        发送日报

        Args:
            to: 收件人
            report_data: 报表数据

        Returns:
            是否发送成功
        """
        subject = f"【闲鱼自动化】日报 - {datetime.now().strftime('%Y-%m-%d')}"
        body = f"""
        <html>
        <body>
            <h2>每日运营报表</h2>
            <p>新增订单: {report_data.get('new_orders', 0)}</p>
            <p>销售额: ¥{report_data.get('sales', 0)}</p>
            <p>在线账号: {report_data.get('online_accounts', 0)}</p>
            <p>待处理告警: {report_data.get('pending_alerts', 0)}</p>
            <hr>
            <p>此邮件由闲鱼自动管理系统发送</p>
        </body>
        </html>
        """
        return await self.send_email(to, subject, body)


# 全局服务实例
_email_service = None


def get_email_service() -> EmailService:
    """获取邮件服务实例"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


from datetime import datetime
