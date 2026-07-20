import requests


def detect_intent(text: str) -> str:
    text = text.lower()

    if any(w in text for w in ["открой", "запусти", "включи", "старт", "открыть"]):
        return "skill"

    return "chat"


def ask_ai(text: str, memory_context: str = ""):

    system_prompt = f"""
Ты JARVIS — персональный AI ассистент.

Ты используешь память о пользователе и историю диалога.

ВАЖНО:
- не выдумывай факты
- не называй пользователя по имени без памяти
- будь кратким и естественным
- ОТВЕЧАЙ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ
- НИКОГДА НЕ ИСПОЛЬЗУЙ АНГЛИЙСКИЙ
- НЕ ПЕРЕКЛЮЧАЙСЯ НА ДРУГИЕ ЯЗЫКИ
- НЕ ДОБАВЛЯЙ ФРАЗЫ ВРОДЕ "You're welcome"
- не добавляй в каждом предложение слово саратов
- называй пользователя "сэр"


ПАМЯТЬ:
{memory_context}
"""

    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": system_prompt + "\n\nUser: " + text + "\nJarvis:",
                "stream": False
            },
            timeout=60
        )

        return r.json()["response"].strip()

    except:
        return "Локальный ИИ недоступен."

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------