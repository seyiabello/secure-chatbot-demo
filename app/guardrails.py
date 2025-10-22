import re
from datetime import datetime

# 🚧 Patterns that indicate prompt-injection or sensitive data
FORBIDDEN_PATTERNS = [
    r"system prompt",
    r"ignore previous",
    r"developer instructions",
    r"reveal",
    r"bypass",
    r"confidential",
    r"secret key",
]

# 📜 Simple audit logger
def log_event(event_type: str, message: str):
    """
    Append a timestamped security event to security.log.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open("security.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {event_type}: {message}\n")


def apply_input_guard(text: str) -> bool:
    """
    Return True if the input looks suspicious or malicious.
    Example triggers: 'ignore previous', 'reveal system prompt', etc.
    """
    if not text:
        return False

    lower = text.lower()
    for pat in FORBIDDEN_PATTERNS:
        if pat in lower:
            log_event("BLOCKED_INPUT", text)
            return True
    return False


def apply_output_guard(output: str) -> str:
    """
    Sanitise model output to remove or redact sensitive information.
    - Redacts forbidden keywords like 'system prompt'
    - Removes long suspicious strings (e.g. leaked API keys)
    """
    if not output:
        return output

    redacted = output
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, redacted, flags=re.IGNORECASE):
            log_event("REDACTED_OUTPUT", redacted)
            redacted = re.sub(pat, "[REDACTED]", redacted, flags=re.IGNORECASE)

    # Remove base64-like or key-like long strings
    redacted = re.sub(r"([A-Za-z0-9+/]{40,}=*)", "[REDACTED]", redacted)

    return redacted
