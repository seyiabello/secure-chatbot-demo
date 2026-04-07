<!-- ======================= -->
<!-- 🔥 HERO SECTION -->
<!-- ======================= -->

<h1 align="center">🛡️ Secure AI Chatbot (PoC)</h1>

<p align="center">
  <b>Secure LLM Backend · FastAPI · Guardrails · Resilience Engineering</b>
</p>

<p align="center">
  A production-style AI chatbot demonstrating prompt injection defense, output sanitisation, and secure deployment patterns
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Security-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Docker-Deployable-blue?style=for-the-badge"/>
</p>

<p align="center">
  🌐 <a href="https://secure-chatbot-demo.onrender.com"><b>Live Demo</b></a> ·
  📘 <a href="https://secure-chatbot-demo.onrender.com/docs"><b>API Docs</b></a>
</p>

---

# 🧠 Overview

This project is a **secure AI chatbot backend** built with FastAPI, designed to demonstrate:

- Prompt injection defence  
- Output sanitisation (guardrails)  
- Secure logging practices  
- Resilient LLM interaction (fallback + retries + mock mode)  

👉 Focus: **building safe, deployable AI systems — not just models**

---

# 🧠 System Architecture


User → /chat (FastAPI)
↓
Input Guard (Prompt Injection Filtering)
↓
LLM (OpenAI API or Mock Mode)
↓
Output Guard (Sanitisation / Redaction)
↓
Response to User
↓
Security Log (metadata only)


### 🔐 Design Principles

- Never trust user input  
- Never expose raw model output  
- Never log sensitive data  
- Always support graceful failure  

---

# 🚀 Features

### 🛡️ Security
- Prompt injection detection and filtering  
- Output guardrails (sensitive data redaction)  
- UTF-8 safe logging (`security.log`)  
- No secrets stored or logged  

### ⚙️ Resilience
- Automatic retries on failure  
- Model fallback support  
- Mock mode (works without API key)  

### 🧪 Testing
- Pytest suite for:
  - Guardrails  
  - Mock mode  
  - Core functionality  

### 🌐 API & UI
- FastAPI backend (`/chat`, `/health`)  
- Interactive Swagger docs (`/docs`)  
- Minimal HTML chat interface  

### 🐳 Deployment
- Dockerised for portability  
- Deployed on Render  

---

# ⚙️ Local Setup

## 1️⃣ Clone the repo

```bash
git clone https://github.com/seyiabello/secure-chatbot-demo.git
cd secure-chatbot-demo
```
## 2️⃣ Create virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
# or
source .venv/bin/activate       # macOS/Linux
## 3️⃣ Install dependencies
pip install -r requirements.txt

## 4️⃣ Configure environment variables

Create a .env file:

OPENAI_API_KEY=sk-xxxx
MODEL_NAME=gpt-3.5-turbo
## 5️⃣ Run the app
uvicorn app.main:app --reload --port 8000
Access:
Chat UI → http://127.0.0.1:8000
Docs → http://127.0.0.1:8000/docs
Health → http://127.0.0.1:8000/health
## 🧪 Tests

Run all tests:

pytest -q
## 🐳 Docker Usage
Build image
docker build -t secure-chatbot-demo .
Run (mock mode)
docker run -p 8000:8000 secure-chatbot-demo
Run (with API key)
docker run -e OPENAI_API_KEY="sk-xxx" -e MODEL_NAME="gpt-3.5-turbo" -p 8000:8000 secure-chatbot-demo
## 🌐 Deployment (Render)

The app is deployed using Docker on Render.

Environment variables:
OPENAI_API_KEY (optional for mock mode)
MODEL_NAME (e.g. gpt-3.5-turbo)
## 🔍 Security Practices
.env excluded via .gitignore
Secrets injected via environment variables only
Logs store metadata only (no user content)
Guardrails enforce safe interaction

👉 Production-ready extensions:

Rate limiting (SlowAPI)
Authentication (JWT / API key)
PII detection layer
## 🧱 Project Structure
secure-chatbot-demo/
├── app/
│   ├── main.py
│   ├── guardrails.py
│   ├── settings.py
│   ├── prompts.py
│   └── tests/
├── security.log
├── requirements.txt
├── Dockerfile
├── THREAT_MODEL.md
└── README.md
## 🧠 Threat Model (Summary)
Covered threats:
Prompt injection / jailbreak attempts
Sensitive data leakage
API key exposure
Logging vulnerabilities
DoS / quota exhaustion
Controls implemented:
Input/output guards
Logging redaction
Retry + fallback + mock modes
Environment-based secret management

👉 See THREAT_MODEL.md for full details

## 🧰 Tech Stack
Component	Technology
Backend	FastAPI (Python 3.11)
LLM	OpenAI API / Mock
Deployment	Render (Docker)
Testing	Pytest
Logging	Local UTF-8 file
Frontend	HTML + Fetch API
## 💡 Future Enhancements
Authentication (JWT / API keys)
Rate limiting (SlowAPI)
ML-based input classification
Observability dashboards
Extended LLM fallback logic
## 👤 Author

Oluwaseyi Bello
🎓 MSc Human-Centred AI (Data Science) — University of Exeter
💻 AI Engineer focused on secure, deployable AI systems

📧 seyiabello@gmail.com

🔗 https://www.linkedin.com/in/oluwaseyi-bello-2653a2215/

## 🪪 License

Educational and research use.
Feel free to fork and extend with credit.
