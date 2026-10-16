import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# ==============================================================
# CẤP ĐỘ 1: Bộ test cơ bản có sẵn
# ==============================================================
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""
    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ==============================================================
# CẤP ĐỘ 2: Bổ sung 7 kịch bản Mocking & Edge Cases
# ==============================================================
class TestMediumLevel(unittest.TestCase):
    """Kiểm thử áp dụng mã khuyến mãi (apply_promo_code)"""

    def test_promo_online_valid(self):
        """Kịch bản 1: Online hợp lệ áp dụng mã GIAM10"""
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000, "GIAM10")
        self.assertEqual(result, 90000.0)

    def test_promo_offline_raises_connection_error(self):
        """Kịch bản 2: Thiết bị Offline ném ngoại lệ ConnectionError"""
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_promo_special_valid_on_os_15(self):
        """Kịch bản 3: Mã NEW_OS_ONLY áp dụng thành công trên OS 15"""
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000, "NEW_OS_ONLY")
        self.assertEqual(result, 80000.0)

    def test_promo_special_invalid_on_os_14_raises_value_error(self):
        """Kịch bản 4: Mã NEW_OS_ONLY ném ValueError khi chạy trên OS 14"""
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """Kiểm thử chức năng GPS lân cận sử dụng unittest.mock.patch"""

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_in_range(self, mock_location):
        """Kịch bản 5: Mock GPS trả về tọa độ trong vùng có nhà hàng (10.0, 105.0)"""
        mock_location.return_value = (10.0, 105.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(
            restaurants,
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"]
        )

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_out_of_range(self, mock_location):
        """Kịch bản 6: Mock GPS trả về tọa độ ngoài vùng hỗ trợ (20.0, 110.0)"""
        mock_location.return_value = (20.0, 110.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(restaurants, [])

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_signal_lost(self, mock_location):
        """Kịch bản 7: Mock GPS ném GPSSignalLostError khi mất sóng định vị"""
        mock_location.side_effect = gps_service.GPSSignalLostError()
        app = YummyApp()
        result = app.get_nearby_restaurants()
        self.assertEqual(result, "Khong the xac dinh vi tri.")


if __name__ == "__main__":
    unittest.main()