import json
import sqlite3

from fastapi import APIRouter, Depends

from database import get_db
from database import get_db

router = APIRouter()


@router.get("")
def list_audit_logs(db: sqlite3.Connection = Depends(get_db)) -> list[dict[str, object]]:
    events = db.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 100").fetchall()
    return [
        {**dict(event), "rules_checked": json.loads(event["rules_checked"])} for event in events
    ]


@router.get("/metrics")
def revenue_metrics(db: sqlite3.Connection = Depends(get_db)) -> dict[str, int]:
    row = db.execute("SELECT COUNT(*) AS orders, COALESCE(SUM(amount_paise), 0) AS revenue "
                     "FROM orders WHERE status = 'paid'").fetchone()
    return {"paid_orders": row["orders"], "revenue_paise": row["revenue"]}
