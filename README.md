# Secure Chatbot PoC (AI Security Mini-Project)

A FastAPI microservice that demonstrates prompt-injection defenses, output sanitization, logging, and resilience (retry/fallback/mock).

## Features
- Guarded `/chat` endpoint
- Output redaction + input blocking
- Security logging to `security.log`
- `/health` endpoint for uptime
- Works offline in mock mode
- Dockerized + pytest coverage

## Quickstart
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
...
EOF

yaml
Copy code

---

## 🔒 Step 5 — Create `THREAT_MODEL.md`

```bash
cat > THREAT_MODEL.md << 'EOF'
# Threat Model — Secure Chatbot PoC
...
EOF