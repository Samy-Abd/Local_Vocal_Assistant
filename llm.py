import requests
from config import OLLAMA_URL, OLLAMA_MODEL, SYSTEM_PROMPT

def ask_ollama(user_text: str, history: list | None = None) -> str:
    """
    history: optional list of {"role": "user"/"assistant", "content": "..."}
    For MVP we keep it simple: prepend system prompt + short history.
    """
    prompt_parts = [f"System: {SYSTEM_PROMPT}"]

    if history:
        for m in history[-6:]:
            role = m.get("role", "user")
            content = m.get("content", "")
            prompt_parts.append(f"{role.capitalize()}: {content}")

    prompt_parts.append(f"User: {user_text}")
    prompt_parts.append("Assistant:")

    prompt = "\n".join(prompt_parts)

    r = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip()