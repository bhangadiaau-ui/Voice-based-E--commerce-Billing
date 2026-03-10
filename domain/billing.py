from domain.cart import Cart

def generate_bill(cart: Cart) -> dict:
    return {
        "items": cart.items,
        "total": cart.total()
    }