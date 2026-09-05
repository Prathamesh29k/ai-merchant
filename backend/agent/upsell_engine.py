ACCESSORY_RULES = {
    "laptop": ["mouse", "bag"],
    "phone": ["case", "charger"],
}


def suggest_upsells(category: str, products: list[dict[str, object]]) -> list[dict[str, object]]:
    desired = ACCESSORY_RULES.get(category.lower(), [])
    return [
        product for product in products
        if product["stock"] and any(word in str(product["category"]).lower() or word in str(product["name"]).lower()
                                     for word in desired)
    ]
