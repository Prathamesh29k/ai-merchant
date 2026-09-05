import sqlite3

from fastapi import APIRouter, Depends

from agent.chat_agent import respond
from agent.upsell_engine import suggest_upsells
from database import get_db
from models import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat(payload: ChatRequest, db: sqlite3.Connection = Depends(get_db)) -> dict[str, object]:
    reply = respond(payload.message)
    products = [dict(row) for row in db.execute("SELECT * FROM products WHERE stock > 0").fetchall()]
    category = reply["intent"].get("category") if isinstance(reply["intent"], dict) else None
    return {**reply, "upsells": suggest_upsells(str(category or ""), products)}