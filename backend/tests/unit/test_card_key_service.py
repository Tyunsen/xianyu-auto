"""
卡密服务单元测试
"""
import pytest
from unittest.mock import MagicMock
from datetime import datetime


class TestCardKeyService:
    """卡密服务测试"""

    def test_allocate_card_key_success(self):
        """测试分配卡密成功"""
        from src.services.order_service import OrderService

        # Mock order
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.product_id = 1

        # Mock card key
        mock_card_key = MagicMock()
        mock_card_key.id = 1

        mock_db = MagicMock()

        # First call returns order, second call returns card key
        mock_db.query.return_value.filter.return_value.first.side_effect = [mock_order, mock_card_key]

        service = OrderService(mock_db)
        result = service.allocate_card_key(1)

        assert result is not None
        mock_db.commit.assert_called()

    def test_allocate_card_key_no_available(self):
        """测试没有可用卡密"""
        from src.services.order_service import OrderService

        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.product_id = 1

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.side_effect = [mock_order, None]

        service = OrderService(mock_db)
        result = service.allocate_card_key(1)

        assert result is None

    def test_ship_order_success(self):
        """测试发货成功"""
        from src.services.order_service import OrderService

        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.status = "paid"

        mock_card_key = MagicMock()
        mock_card_key.id = 1

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.side_effect = [mock_order, mock_card_key]

        service = OrderService(mock_db)
        result = service.ship_order(1)

        assert result is True

    def test_ship_order_failure(self):
        """测试发货失败（订单不存在）"""
        from src.services.order_service import OrderService

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        service = OrderService(mock_db)
        result = service.ship_order(999)

        assert result is False


class TestOrderService:
    """订单服务测试"""

    def test_get_pending_orders(self):
        """测试获取待发货订单"""
        from src.services.order_service import OrderService
        from src.models.order import OrderStatus

        mock_order = MagicMock()
        mock_order.id = 1

        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.all.return_value = [mock_order]

        service = OrderService(mock_db)
        orders = service.get_pending_orders()

        assert len(orders) == 1

    def test_create_ship_failed_alert(self):
        """测试创建发货失败告警"""
        from src.services.order_service import OrderService

        mock_db = MagicMock()

        service = OrderService(mock_db)
        alert = service.create_ship_failed_alert(1, "测试失败原因")

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
