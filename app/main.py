# app/main.py
from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .settings import settings
from .guardrails import apply_input_guard, apply_output_guard


app = FastAPI()


# ---------- Logging Helper ----------
def log_event(event_type: str, message: str):
    """Append event details to security.log with timestamps (UTF-8 safe)."""
    with open("security.log", "a", encoding="utf-8", errors="replace") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {event_type}: {message}\n")


# ---------- Retry Logic for OpenAI API ----------
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def call_openai(prompt: str, api_key: str, model: str):
    """Call OpenAI API with retry logic for transient failures."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30.0,
        )

        # Retry on transient codes
        if resp.status_code in (429, 500, 502, 503):
            raise Exception(f"Transient API error: {resp.status_code}")

        # Surface non-OK errors
        if resp.status_code != 200:
            log_event("API_ERROR", resp.text)
            raise HTTPException(status_code=resp.status_code, detail="LLM API error")

        return resp.json()


# ---------- Request Schema ----------
class ChatRequest(BaseModel):
    message: str


# ---------- Chat Endpoint ----------
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        # 1) Input Guard
        if apply_input_guard(req.message):
            log_event("BLOCKED_INPUT", req.message)
            return {"response": "I'm sorry — I cannot comply with that request."}

        # 2) Missing API key? Use mock mode immediately
        api_key = getattr(settings, "openai_api_key", "") or os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            log_event("MOCK_MODE", "OPENAI_API_KEY not set — serving mock response.")
            mock_response = f"[MOCK RESPONSE] Hi! I’m your local AI assistant (offline mode). You said: '{req.message}'"
            clean_text = apply_output_guard(mock_response)
            return {"response": clean_text}

        # 3) Try primary model
        primary_model = getattr(settings, "model_name", "") or os.getenv("MODEL_NAME", "") or "gpt-4o-mini"
        try:
            j = await call_openai(req.message, api_key, primary_model)
        except Exception as e:
            # 4) Try fallback model on typical transient errors
            if any(code in str(e) for code in ("429", "503", "502", "500")):
                fallback_model = "gpt-3.5-turbo"
                log_event("FALLBACK_TRIGGERED", f"Switching {primary_model} -> {fallback_model} due to: {e}")
                try:
                    j = await call_openai(req.message, api_key, fallback_model)
                except Exception as inner_e:
                    # 5) Enter mock LLM mode
                    log_event("MOCK_MODE", f"Using local mock response due to fallback failure: {inner_e}")
                    mock_response = f"[MOCK RESPONSE] Hi! I’m your local AI assistant (offline mode). You said: '{req.message}'"
                    clean_text = apply_output_guard(mock_response)
                    return {"response": clean_text}
            else:
                raise e

        # 6) Extract and sanitize response
        text = j.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
        clean_text = apply_output_guard(text)
        if clean_text != text:
            log_event("REDACTED_OUTPUT", text)

        return {"response": clean_text}

    except HTTPException:
        # Already logged above for API_ERROR
        raise
    except Exception as e:
        log_event("API_EXCEPTION", str(e))
        # Avoid non-ASCII in detail to prevent codec issues on some terminals
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")


# ---------- Health & Root (GET + HEAD) ----------
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Response
from pathlib import Path

STATIC_DIR = Path("app/static")
INDEX_HTML = STATIC_DIR / "index.html"

# Health (GET + HEAD)
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "primary_model": getattr(settings, "model_name", "mock"),
        "time": f"{datetime.now():%Y-%m-%d %H:%M:%S}",
    }

@app.head("/health")
async def health_head():
    return Response(status_code=200)

# Serve /static if the directory exists (safe to call even if missing)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Root (GET): prefer the HTML UI if present; otherwise return a tiny HTML page
@app.get("/", response_class=HTMLResponse)
async def root_ui():
    if INDEX_HTML.exists():
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            return f.read()
    # HTML fallback (not JSON)
    return """<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>Secure Chatbot</title>
<body style="font-family:system-ui; max-width:720px; margin:3rem auto;">
  <h1>Secure Chatbot is running 🟢</h1>
  <p>Use the <a href="/docs">Swagger UI</a> or <a href="/health">/health</a>.</p>
  <p>If you expected a full web UI, make sure <code>app/static/index.html</code> exists and is committed.</p>
</body></html>"""

# Root (HEAD): return 200 for uptime checkers
@app.head("/")
async def root_head():
    return Response(status_code=200)



# ---------- Static UI (optional) ----------
# Serve / (HTML UI) if app/static/index.html exists; else keep JSON root above.
STATIC_DIR = Path("app/static")
INDEX_HTML = STATIC_DIR / "index.html"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    if INDEX_HTML.exists():
        @app.get("/", response_class=HTMLResponse)
        async def home():
            with open(INDEX_HTML, "r", encoding="utf-8") as f:
                return f.read()
