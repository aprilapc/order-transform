class Order:
    def __init__(self, id, name, address, price, currency):
        self.id = id
        self.name = name
        self.address = address
        self.price = price
        self.currency = currency


class Address:
    def __init__(self, city, district, street):
        self.city = city
        self.district = district
        self.street = street
