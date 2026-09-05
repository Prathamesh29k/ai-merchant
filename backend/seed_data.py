import json
from pathlib import Path

from database import get_connection, init_db


def seed() -> None:
    init_db()
    products = json.loads((Path(__file__).parent.parent / "sample_data" / "products.json").read_text())
    with get_connection() as db:
        db.execute("DELETE FROM products")
        db.executemany(
            "INSERT INTO products (name, category, description, price_paise, stock) VALUES (?, ?, ?, ?, ?)",
            [(p["name"], p["category"], p["description"], p["price_paise"], p["stock"]) for p in products],
        )
        db.commit()
    print(f"Seeded {len(products)} products")


if __name__ == "__main__":
    seed()