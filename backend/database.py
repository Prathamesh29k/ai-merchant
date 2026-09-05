import sqlite3
from collections.abc import Generator

from config import settings


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(settings.database_path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                price_paise INTEGER NOT NULL CHECK(price_paise >= 0),
                stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0)
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                amount_paise INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'created',
                razorpay_order_id TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id) REFERENCES products(id)
            );
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                action TEXT NOT NULL,
                amount_paise INTEGER NOT NULL DEFAULT 0,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                rules_checked TEXT NOT NULL,
                decision TEXT NOT NULL,
                explanation TEXT NOT NULL
            );
            """
        )


def get_db() -> Generator[sqlite3.Connection, None, None]:
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()
