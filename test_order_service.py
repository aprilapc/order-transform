import unittest
import json
from app import app


class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_successful_order(self):
        order = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "2000",
            "currency": "TWD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Order received", response.get_data(as_text=True))

    def test_successful_order_with_usd(self):
        order = {
            "id": "A0000002",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "50",
            "currency": "USD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Order received", response.get_data(as_text=True))
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data["order"]["currency"], "TWD")
        self.assertEqual(response_data["order"]["price"], str(int(50 * 31)))

    def test_order_with_usd_exceeding_2000(self):
        order = {
            "id": "A0000003",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "100",
            "currency": "USD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price is over 2000", response.get_data(as_text=True))

    def test_missing_order_id(self):
        order = {
            "id": "",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "2000",
            "currency": "TWD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Order ID is required", response.get_data(as_text=True))

    def test_non_english_name(self):
        order = {
            "id": "A0000001",
            "name": "Melody 旅館",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "2000",
            "currency": "TWD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Name contains non-English characters", response.get_data(as_text=True)
        )

    def test_name_not_capitalized(self):
        order = {
            "id": "A0000001",
            "name": "melody holiday inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "2000",
            "currency": "TWD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Name is not capitalized", response.get_data(as_text=True))

    def test_price_not_a_number(self):
        order = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "twenty",
            "currency": "TWD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price must be a number", response.get_data(as_text=True))

    def test_price_over_2000(self):
        order = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "3000",
            "currency": "TWD",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price is over 2000", response.get_data(as_text=True))

    def test_invalid_currency(self):
        order = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road",
            },
            "price": "2000",
            "currency": "EUR",
        }
        response = self.app.post(
            "/api/orders", data=json.dumps(order), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Currency format is wrong", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
