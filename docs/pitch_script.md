# Five-minute Razorpay AI Buildathon Pitch

## 0:00-1:00: Problem slide

"AI buyers are moving from search to action. NPCI's Unified Agent Protocol makes that direction concrete, but a merchant cannot safely expose only a checkout button. The merchant also needs structured product context, agent identity, spending policy, explainable recommendations, and a full record of what happened. Today, those controls are fragmented."

Show the problem slide with three labels: discoverability, trust, and control.

## 1:00-3:00: Live demo

1. Open the Agent-Ready Merchant OS landing page and state that the prototype uses FastAPI, SQLite, Next.js, Razorpay Test Mode, and Groq's free tier.
2. Open `/dashboard`. Point out the agent-readable catalog, prices in paise, stock, revenue metric, and audit table.
3. Open `/checkout`. Ask: `Show me laptops under 50000`.
4. Explain the structured intent: category `laptop`, max price `5000000` paise, and keywords. Point out the laptop upsell rule and accessories.
5. Create a test order from the dashboard. Show the generated `order_test_...` ID when no Razorpay credentials are configured, or the real Razorpay Test Mode order ID when keys are present.
6. Return to the dashboard and show the approved `order.create` event with agent ID, amount, rules checked, decision, and explanation.

## 3:00-4:00: Failure handling

1. Explain the demo default: `DAILY_LIMIT_PER_AGENT=5000` paise, or ₹50.
2. Use a low-priced test product and place one order for the same agent.
3. Place the second order for that agent. The API returns HTTP 400 with `daily_limit_exceeded`, today's total, and the limit.
4. Refresh the audit table. Show that the rejected attempt is still logged with `decision: rejected`, the checked rules, amount, and a human-readable explanation.
5. Emphasize that the guardrail runs before Razorpay order creation, so an unsafe transaction never reaches the payment provider.

## 4:00-5:00: Why Razorpay and closing

"Razorpay can be the payment execution layer for agentic commerce, but merchants need a policy and observability layer around payment creation. This project demonstrates that layer with standard public Test Mode APIs, HMAC-SHA256 verification, and no special hackathon access. It is cheap to prototype, explicit about failure, and ready to evolve toward UAP-compatible agent identity and consent flows."

Close on the GitHub repository URL and show the final dashboard audit trail. Mention that real keys are never committed, the free Groq integration has a deterministic fallback, and the demo can run at zero rupees.

## Recording checklist

- Capture the problem slide before opening the app.
- Keep the backend terminal visible briefly when starting `uvicorn`.
- Use a clean browser window at `localhost:3000`.
- Zoom the dashboard enough for the audit columns to be readable.
- Pause after the rejection response so `daily_limit_exceeded` is legible.
- End with the public GitHub URL and the architecture diagram from the README.
