from flask import Flask, request, jsonify
from order import Order, Address
from order_service import OrderService
from order_validator import OrderValidator

app = Flask(__name__)

order_service = OrderService(OrderValidator())


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.json
    address = Address(
        data["address"]["city"], data["address"]["district"], data["address"]["street"]
    )
    order = Order(data["id"], data["name"], address, data["price"], data["currency"])
    try:
        created_order = order_service.create_order(order)
        response_data = {
            "id": created_order.id,
            "name": created_order.name,
            "address": {
                "city": created_order.address.city,
                "district": created_order.address.district,
                "street": created_order.address.street,
            },
            "price": created_order.price,
            "currency": created_order.currency,
        }
        return jsonify({"message": "Order received", "order": response_data}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
