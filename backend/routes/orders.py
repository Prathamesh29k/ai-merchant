import hashlib
import hmac
import sqlite3
import uuid

from fastapi import APIRouter, Depends, HTTPException

from config import settings
from database import get_db
from middleware.audit_logger import log_money_action
from models import OrderCreate, OrderResponse, PaymentVerifyRequest

router = APIRouter()


def _daily_total(db: sqlite3.Connection, agent_id: str) -> int:
    row = db.execute(
        "SELECT COALESCE(SUM(amount_paise), 0) AS total FROM orders "
        "WHERE agent_id = ? AND date(created_at) = date('now') AND status != 'rejected'",
        (agent_id,),
    ).fetchone()
    return int(row["total"])


def _razorpay_order(amount_paise: int, receipt: str) -> str:
    if settings.razorpay_key_id and settings.razorpay_key_secret:
        import razorpay

        client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
        created = client.order.create({"amount": amount_paise, "currency": "INR", "receipt": receipt})
        return str(created["id"])
    return f"order_test_{uuid.uuid4().hex[:16]}"


@router.post("", response_model=OrderResponse)
def create_order(payload: OrderCreate, db: sqlite3.Connection = Depends(get_db)) -> OrderResponse:
    product = db.execute("SELECT * FROM products WHERE id = ?", (payload.product_id,)).fetchone()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if payload.quantity > product["stock"]:
        raise HTTPException(status_code=400, detail="Requested quantity is unavailable")

    amount_paise = product["price_paise"] * payload.quantity
    daily_total = _daily_total(db, payload.agent_id)
    rules = ["product_exists", "stock_available", "daily_spending_limit"]
    if daily_total + amount_paise > settings.daily_limit_paise:
        explanation = (
            f"Rejected: today's spend is {daily_total} paise; adding {amount_paise} paise "
            f"would exceed the {settings.daily_limit_paise} paise agent limit."
        )
        log_money_action(db, agent_id=payload.agent_id, action="order.create", amount_paise=amount_paise,
                         rules_checked=rules, decision="rejected", explanation=explanation)
        db.commit()
        raise HTTPException(status_code=400, detail={
            "error_code": "daily_limit_exceeded", "today_total_paise": daily_total,
            "limit_paise": settings.daily_limit_paise, "message": explanation,
        })

    razorpay_order_id = _razorpay_order(amount_paise, f"agent-{payload.agent_id}")
    cursor = db.execute(
        "INSERT INTO orders (agent_id, product_id, quantity, amount_paise, status, razorpay_order_id) "
        "VALUES (?, ?, ?, ?, 'created', ?)",
        (payload.agent_id, payload.product_id, payload.quantity, amount_paise, razorpay_order_id),
    )
    db.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (payload.quantity, payload.product_id))
    log_money_action(db, agent_id=payload.agent_id, action="order.create", amount_paise=amount_paise,
                     rules_checked=rules, decision="approved",
                     explanation="Order passed product, stock, and daily spending checks.")
    db.commit()
    return OrderResponse(id=cursor.lastrowid, agent_id=payload.agent_id, product_id=payload.product_id,
                         quantity=payload.quantity, amount_paise=amount_paise, amount_inr=amount_paise / 100,
                         status="created", razorpay_order_id=razorpay_order_id,
                         daily_total_paise=daily_total + amount_paise,
                         daily_limit_paise=settings.daily_limit_paise)


@router.post("/verify")
def verify_payment(payload: PaymentVerifyRequest, db: sqlite3.Connection = Depends(get_db)) -> dict[str, str]:
    order = db.execute("SELECT * FROM orders WHERE id = ?", (payload.order_id,)).fetchone()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    message = f"{payload.razorpay_order_id}|{payload.razorpay_payment_id}"
    expected = hmac.new(settings.razorpay_key_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    if not settings.razorpay_key_secret or not hmac.compare_digest(expected, payload.razorpay_signature):
        log_money_action(db, agent_id=order["agent_id"], action="payment.verify",
                         amount_paise=order["amount_paise"],
                         rules_checked=["order_exists", "hmac_sha256_signature"], decision="rejected",
                         explanation="Payment signature verification failed.")
        db.commit()
        raise HTTPException(status_code=400, detail={"error_code": "invalid_signature"})
    db.execute("UPDATE orders SET status = 'paid' WHERE id = ?", (payload.order_id,))
    log_money_action(db, agent_id=order["agent_id"], action="payment.verify",
                     amount_paise=order["amount_paise"],
                     rules_checked=["order_exists", "hmac_sha256_signature"], decision="approved",
                     explanation="Razorpay payment signature verified successfully.")
    db.commit()
    return {"status": "paid", "message": "Payment verified"}
