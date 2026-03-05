"""
账号服务单元测试
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime


class TestAccountService:
    """账号服务测试"""

    def test_check_login_status_not_found(self):
        """测试账号不存在的情况"""
        from src.services.account_service import AccountService

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        service = AccountService(mock_db)
        result = service.check_login_status(999)

        assert result["status"] == "not_found"

    def test_check_login_status_no_cookies(self):
        """测试未设置 cookies 的情况"""
        from src.services.account_service import AccountService

        mock_account = MagicMock()
        mock_account.cookies = ""
        mock_account.status = "offline"

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_account

        service = AccountService(mock_db)
        result = service.check_login_status(1)

        assert result["status"] == "no_cookies"

    def test_refresh_cookies_success(self):
        """测试刷新 cookies 成功"""
        from src.services.account_service import AccountService

        mock_account = MagicMock()
        mock_account.id = 1

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_account

        with patch("src.services.account_service.get_encryptor") as mock_encrypt:
            mock_encrypt.return_value.encrypt.return_value = "encrypted_cookies"

            service = AccountService(mock_db)
            result = service.refresh_cookies(1, "test_cookies")

            assert result is True
            mock_db.commit.assert_called_once()

    def test_refresh_cookies_failure(self):
        """测试刷新 cookies 失败（账号不存在）"""
        from src.services.account_service import AccountService

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        service = AccountService(mock_db)
        result = service.refresh_cookies(999, "test_cookies")

        assert result is False

    def test_detect_expired_accounts(self):
        """测试检测失效账号"""
        from src.services.account_service import AccountService

        mock_account1 = MagicMock()
        mock_account1.id = 1
        mock_account1.status = "offline"

        mock_account2 = MagicMock()
        mock_account2.id = 2
        mock_account2.status = "error"

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.all.return_value = [mock_account1, mock_account2]

        service = AccountService(mock_db)
        expired = service.detect_expired_accounts()

        assert len(expired) == 2

    def test_update_status(self):
        """测试更新账号状态"""
        from src.services.account_service import AccountService

        mock_account = MagicMock()
        mock_account.id = 1

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_account

        service = AccountService(mock_db)
        result = service.update_status(1, "online")

        assert result is True
        assert mock_account.status == "online"
        mock_db.commit.assert_called_once()
