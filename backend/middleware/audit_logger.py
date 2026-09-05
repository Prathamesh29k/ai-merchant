import json
import sqlite3
from collections.abc import Callable

from fastapi import FastAPI, Request

from database import get_connection


def log_money_action(
    connection: sqlite3.Connection,
    *,
    agent_id: str,
    action: str,
    amount_paise: int,
    rules_checked: list[str],
    decision: str,
    explanation: str,
) -> None:
    connection.execute(
        """
        INSERT INTO audit_logs
        (agent_id, action, amount_paise, rules_checked, decision, explanation)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (agent_id, action, amount_paise, json.dumps(rules_checked), decision, explanation),
    )


def register_audit_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def audit_request(request: Request, call_next: Callable):
        response = await call_next(request)
        response.headers["X-Agent-Audit"] = "money-actions-logged-at-route-boundary"
        return response