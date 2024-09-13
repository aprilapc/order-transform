from order_validator import OrderValidator
from order import Order


class OrderService:
    def __init__(self, validator: OrderValidator):
        self.validator = validator

    def create_order(self, order: Order):
        # 驗證訂單資料
        self.validator.validate(order)

        # 檢查 name 是否包含非英文字符
        if not order.name.isascii():
            raise ValueError("Name contains non-English characters")

        # 檢查 name 是否每個單字首字母大寫
        if not all(word.istitle() for word in order.name.split()):
            raise ValueError("Name is not capitalized")

        # 檢查 currency 是否為 TWD 或 USD
        if order.currency not in ["TWD", "USD"]:
            raise ValueError("Currency format is wrong")

        # 如果 currency 是 USD，將 price 轉換為 TWD
        if order.currency == "USD":
            order.price = str(int(float(order.price) * 31))
            order.currency = "TWD"

        # 檢查 price 是否超過 2000
        if float(order.price) > 2000:
            raise ValueError("Price is over 2000")

        # 這裡省略具體實現
        return order
