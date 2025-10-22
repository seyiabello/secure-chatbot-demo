# Secure Chatbot PoC (AI Security Mini-Project)

A tiny FastAPI chatbot that **demonstrates prompt-injection attacks** and **defenses** with input/output guardrails and a minimal **security audit log**.

## What this shows
- Input guard to flag likely prompt-injection attempts
- Output guard to redact sensitive strings (e.g., “system prompt”, key-like blobs)
- Simple security logging to `security.log`
- Unit tests verifying guards

## Stack
FastAPI · Python · Pytest · (optional) OpenAI API · Docker (optional)

## Quickstart (local)
```bash
python -m venv .venv
source .venv/Scripts/activate           # (Git Bash on Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload