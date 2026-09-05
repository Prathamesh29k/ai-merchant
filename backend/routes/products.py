import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import ProductCreate, ProductResponse

router = APIRouter()


@router.get("", response_model=list[ProductResponse])
def list_products(db: sqlite3.Connection = Depends(get_db)) -> list[ProductResponse]:
    rows = db.execute("SELECT * FROM products ORDER BY id").fetchall()
    return [ProductResponse(**dict(row)) for row in rows]


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(payload: ProductCreate, db: sqlite3.Connection = Depends(get_db)) -> ProductResponse:
    cursor = db.execute(
        "INSERT INTO products (name, category, description, price_paise, stock) VALUES (?, ?, ?, ?, ?)",
        (payload.name, payload.category, payload.description, payload.price_paise, payload.stock),
    )
    db.commit()
    row = db.execute("SELECT * FROM products WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return ProductResponse(**dict(row))


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductCreate, db: sqlite3.Connection = Depends(get_db)) -> ProductResponse:
    cursor = db.execute(
        "UPDATE products SET name=?, category=?, description=?, price_paise=?, stock=? WHERE id=?",
        (payload.name, payload.category, payload.description, payload.price_paise, payload.stock, product_id),
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    db.commit()
    row = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return ProductResponse(**dict(row))


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: sqlite3.Connection = Depends(get_db)) -> None:
    cursor = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    db.commit()
