from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from middleware.audit_logger import register_audit_middleware
from routes import agent, audit, orders, products

init_db()

app = FastAPI(title="Agent-Ready Merchant OS", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_audit_middleware(app)

app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "agent-ready-merchant"}
