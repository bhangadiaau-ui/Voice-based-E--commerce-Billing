import json
from config import PRODUCT_FILE

with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

def get_price(item: str) -> int:
    return PRODUCTS.get(item, 0)