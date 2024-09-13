from order import Order


class OrderValidator:
    def validate(self, order: Order):
        if not order.id:
            raise ValueError("Order ID is required")
        if not order.name:
            raise ValueError("Name is required")
        if not order.address:
            raise ValueError("Address is required")
        if not order.address.city:
            raise ValueError("City is required")
        if not order.address.district:
            raise ValueError("District is required")
        if not order.address.street:
            raise ValueError("Street is required")
        if not order.price:
            raise ValueError("Price is required")
        if not order.currency:
            raise ValueError("Currency is required")

        try:
            float(order.price)
        except ValueError:
            raise ValueError("Price must be a number")
