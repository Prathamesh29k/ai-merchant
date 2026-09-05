# Architecture

The backend owns products, orders, AI orchestration, payment-order creation, and audit events. The frontend consumes the API and renders merchant and checkout workflows.

```text
Next.js UI -> FastAPI routes -> SQLite
                    |-> Groq API (optional)
                    |-> Razorpay Test API (optional)
```

External services are optional during local development. The app remains usable with seeded local products and deterministic fallback responses when credentials are absent.
