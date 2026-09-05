# Agent-Ready Merchant OS

## Problem

NPCI's Unified Agent Protocol (UAP) points toward commerce where AI agents can discover products and act for buyers. Merchants need more than a payment button: they need machine-readable catalogs, conversational checkout, explainable recommendations, spending controls, and an audit trail that makes every agent action accountable.

## Solution

Agent-Ready Merchant OS is a zero-cost prototype for that merchant control plane. It exposes an agent-readable catalog, parses buyer intent, suggests category-aware accessories, creates Razorpay Test Mode orders, verifies payment signatures, rejects purchases over an agent's daily budget, and records the decision context in `audit_logs`.

## Architecture

```text
AI buyer chat / merchant dashboard (Next.js 14 + Tailwind)
                         |
                         v
              FastAPI REST API + CORS
       _________|____________|____________
      v                      v            v
   SQLite              Groq Llama 3   Razorpay Test Mode
 products/orders/       intent JSON     order.create()
 audit_logs
```

## Tech stack

- Python FastAPI, SQLite, Pydantic, pytest
- Next.js 14, React 18, TypeScript, Tailwind CSS
- Razorpay public Test Mode API
- Groq Cloud free tier with Llama 3.1, plus deterministic local fallback
- GitHub for public source hosting

## Setup

From the repository root:

```bash
git init
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
python backend/seed_data.py
```

Add the keys described below to `.env`. The API still runs without them using local test order IDs and local intent parsing.

Run the backend:

```bash
cd backend
uvicorn main:app --reload
```

In a second terminal, run the frontend:

```bash
cd frontend
npm install
npm run dev
```

On Windows PowerShell with script execution restricted, use `npm.cmd install` and `npm.cmd run dev`.

Open [http://localhost:3000](http://localhost:3000), then try `/dashboard` and `/checkout`.

## API endpoints

- `GET /health` - service health check.
- `GET /api/products` - agent-readable catalog.
- `POST /api/products` - create a product; price is in paise.
- `PUT /api/products/{id}` and `DELETE /api/products/{id}` - product CRUD.
- `POST /api/agent/chat` - parse natural-language buyer intent and return upsells.
- `POST /api/orders` - check stock and daily limit, log the decision, and create a Razorpay Test Mode order.
- `POST /api/orders/verify` - verify the Razorpay HMAC-SHA256 signature.
- `GET /api/audit` - audit events with agent, amount, rules, decision, and explanation.
- `GET /api/audit/metrics` - paid-order and revenue metrics.

The default daily limit is `5000` paise (`₹50`) per agent. An over-limit response is HTTP 400 with `error_code: daily_limit_exceeded`, today's total, and the configured limit. The rejection is logged before the response is returned.

## API keys

1. Razorpay: create Test Mode keys at https://dashboard.razorpay.com/app/keys. Put `rzp_test_...` in `RAZORPAY_KEY_ID` and the test secret in `RAZORPAY_KEY_SECRET`.
2. Groq: create a free API key at https://console.groq.com. Put it in `GROQ_API_KEY`.
3. Copy `.env.example` to `.env`; never commit `.env` or live credentials.

## Tests

```bash
python -m pytest tests/test_payment_flow.py -q
```

The tests cover health, product listing, an approved order, and a repeated agent purchase rejected by the daily limit.

## GitHub push

Create an empty public repository on GitHub, then run:

```bash
git add .
git commit -m "Build Agent-Ready Merchant OS"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agent-ready-merchant.git
git push -u origin main
```

## Demo video placeholder

`[Add your 5-minute unlisted YouTube/Loom link here]`

See [docs/pitch_script.md](docs/pitch_script.md) for the timed pitch flow.
