from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .settings import settings
from .guardrails import apply_input_guard, apply_output_guard
from datetime import datetime

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
    reraise=True
)
async def call_openai(prompt: str, api_key: str, model: str):
    """Call OpenAI API with retry logic for transient failures."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30.0
        )

        if resp.status_code in (429, 500, 502, 503):
            raise Exception(f"Transient API error: {resp.status_code}")

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
        # 1️⃣ Input Guard
        if apply_input_guard(req.message):
            log_event("BLOCKED_INPUT", req.message)
            return {"response": "I'm sorry — I cannot comply with that request."}

        # 2️⃣ Try primary model
        primary_model = settings.model_name or "gpt-4o-mini"
        try:
            j = await call_openai(req.message, settings.openai_api_key, primary_model)
        except Exception as e:
            # 3️⃣ Try fallback model
            if "429" in str(e) or "503" in str(e):
                fallback_model = "gpt-3.5-turbo"
                log_event(
                    "FALLBACK_TRIGGERED",
                    f"Switching from {primary_model} -> {fallback_model} due to {e}"
                )
                try:
                    j = await call_openai(req.message, settings.openai_api_key, fallback_model)
                except Exception as inner_e:
                    # 4️⃣ Enter mock LLM mode
                    log_event("MOCK_MODE", f"Using local mock response due to {inner_e}")
                    mock_response = f"[MOCK RESPONSE] Hi! I’m your local AI assistant (offline mode). You said: '{req.message}'"
                    clean_text = apply_output_guard(mock_response)
                    return {"response": clean_text}
            else:
                raise e

        # 5️⃣ Extract and sanitize response
        text = j.get("choices", [{}])[0].get("message", {}).get("content", "")
        clean_text = apply_output_guard(text)

        if clean_text != text:
            log_event("REDACTED_OUTPUT", text)

        return {"response": clean_text}

    except Exception as e:
        log_event("API_EXCEPTION", str(e))
        print(f"[DEBUG] API Exception: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {e}")

from datetime import datetime

@app.get("/health")
async def health():
    """Simple health check endpoint"""
    return {
        "status": "ok",
        "model": getattr(settings, "model_name", "mock"),
        "time": f"{datetime.now():%Y-%m-%d %H:%M:%S}"
    }

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the simple chat UI."""
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()
