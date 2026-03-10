from domain.product_catalog import get_price


class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, name: str, qty: int):
        if not name or qty <= 0:
            return
        if get_price(name) == 0:
            return
        self.items[name] = self.items.get(name, 0) + qty

    def total(self) -> int:
        return sum(qty * get_price(item) for item, qty in self.items.items())

    def is_empty(self) -> bool:
        return len(self.items) == 0