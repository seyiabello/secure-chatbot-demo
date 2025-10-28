# 🛡️ Secure Chatbot PoC (AI Security Mini-Project)

A lightweight **FastAPI-based chatbot service** that demonstrates **prompt-injection defenses**, **output sanitization**, **security logging**, and **resilience mechanisms** such as retries, model fallback, and mock local responses.

🌐 **Live Demo:** [https://secure-chatbot-demo.onrender.com](https://secure-chatbot-demo.onrender.com)  
📘 **API Docs:** [https://secure-chatbot-demo.onrender.com/docs](https://secure-chatbot-demo.onrender.com/docs)

---

## 🚀 Features

✅ **Prompt Injection Defense** – input filtering for unsafe patterns  
✅ **Output Guardrails** – redacts sensitive or forbidden text  
✅ **Secure Logging** – UTF-8 safe `security.log` events only (no secrets)  
✅ **Resilience** – automatic retries, fallback models, mock mode when API unavailable  
✅ **Dockerized** – portable and production-ready container  
✅ **/health Endpoint** – uptime and model info for monitoring  
✅ **Pytest Suite** – automated tests for guards and mock mode  
✅ **Web UI** – minimal HTML chat interface for quick demos  

---

## 🧠 Architecture Overview

User → /chat (FastAPI)
↓
Input Guard → LLM (OpenAI API or Mock)
↓
Output Guard → Response
↓
Security Log (security.log)

yaml
Copy code

- Input & output guards protect against **prompt injection** and **data leakage**
- Uses `.env` for secret management (`OPENAI_API_KEY`, `MODEL_NAME`)
- Logs only event metadata — not sensitive content

---

## ⚙️ Setup & Local Run

### 1️⃣ Clone & enter the project
```bash
git clone https://github.com/seyiabello/secure-chatbot-demo.git
cd secure-chatbot-demo
2️⃣ Create & activate virtual environment
bash
Copy code
python -m venv .venv
source .venv/Scripts/activate   # On Windows (Git Bash)
# or
source .venv/bin/activate       # On macOS/Linux
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Add environment variables
Create a .env file (not committed):

ini
Copy code
OPENAI_API_KEY=sk-xxxx
MODEL_NAME=gpt-3.5-turbo
5️⃣ Run the app
bash
Copy code
uvicorn app.main:app --reload --port 8000
Visit:

Chat UI → http://127.0.0.1:8000

Docs → http://127.0.0.1:8000/docs

Health check → http://127.0.0.1:8000/health

🧪 Tests
Run all tests:

bash
Copy code
pytest -q
🐳 Docker Usage
Build the image
bash
Copy code
docker build -t secure-chatbot-demo .
Run the container
Mock mode (no API key):

bash
Copy code
docker run -p 8000:8000 secure-chatbot-demo
Live LLM mode:

bash
Copy code
docker run -e OPENAI_API_KEY="sk-xxx" -e MODEL_NAME="gpt-3.5-turbo" -p 8000:8000 secure-chatbot-demo
🌐 Deployment (Render)
The service is automatically deployed on Render using the Dockerfile.

Environment Variables on Render
OPENAI_API_KEY → your API key (optional for mock mode)

MODEL_NAME → e.g., gpt-3.5-turbo

🔍 Security Practices
.env excluded from Git via .gitignore

Secrets injected via environment variables only

Logs only events, not content

Rate limits, auth, or PII scanning can be added for production

🧱 Project Structure
bash
Copy code
secure-chatbot-demo/
├── app/
│   ├── main.py           # FastAPI app (core routes + guards)
│   ├── guardrails.py     # Input/output sanitization rules
│   ├── settings.py       # Env variable loading (pydantic)
│   ├── prompts.py        # (Optional) prompt templates
│   └── tests/
│       ├── test_security.py
│       └── test_mock_mode.py
├── security.log          # Security event log
├── requirements.txt
├── README.md
├── Dockerfile
└── THREAT_MODEL.md
🧠 Threat Model Summary
See THREAT_MODEL.md for full analysis.

Threats covered:

Prompt injection / jailbreak attempts

Sensitive data leakage

Logging & API key exposure

DoS or quota exhaustion

Controls implemented:

Input & output guards

Logging redaction

Retry + fallback + mock modes

Environment-based secret management

🧰 Tech Stack
Component	Technology
Backend	FastAPI (Python 3.11)
LLM Interface	OpenAI API / Mock
Deployment	Render (Docker)
Tests	Pytest
Logging	Local UTF-8 log file
Frontend	Minimal HTML + Fetch API

🧾 Status & Badges





💡 Future Enhancements
Add authentication (API key or JWT)

Integrate rate limiting (SlowAPI)

Add advanced ML-based input classifiers

Expand test coverage (LLM mock & fallback)

Add small web dashboard for logs

👤 Author
Oluwaseyi Bello
📧 seyiabello@gmail.com https://www.linkedin.com/in/oluwaseyi-bello-2653a2215/
🎓 MSc Human-Centred AI with proficiency in Data Science, University of Exeter
💻 Passionate about secure AI systems and trustworthy LLM development.

🪪 License
This project is provided for educational and research use.
Feel free to fork and extend with credit.

✨ Secure, testable, and deployable AI guardrail demo — built for learning and trustworthiness in LLM applications.