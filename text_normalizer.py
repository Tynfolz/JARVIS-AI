import re
import num2words


def number_to_words(match):
    num = int(match.group())
    return num2words.num2words(num, lang="ru")


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()

    # -------------------------
    # 1. ЧИСЛА → СЛОВА
    # -------------------------
    text = re.sub(r"\b\d+\b", number_to_words, text)

    # -------------------------
    # 2. МАТЕМАТИЧЕСКИЕ СИМВОЛЫ
    # -------------------------
    symbols = {
        "+": " плюс ",
        "-": " минус ",
        "=": " равно ",
        "*": " умножить на ",
        "/": " делить на ",
        "%": " процентов ",
        "°": " градусов ",
        "℃": " градусов цельсия ",
        "℉": " градусов фаренгейта "
    }

    for sym, word in symbols.items():
        text = text.replace(sym, word)

    # -------------------------
    # 3. СОКРАЩЕНИЯ
    # -------------------------
    replacements = {
        "м/с": "метров в секунду",
        "ai": "эй ай",
        "api": "эй пи ай",
        "cpu": "си пи ю",
        "gpu": "джи пи ю",
        "ram": "рам",
        "wifi": "вай фай",
        "ok": "окей",
        "lol": "лол",
        "jarvis": "джарвис",
        "pc": "пи си"
    }

    for k, v in replacements.items():
        text = re.sub(rf"\b{k}\b", v, text)

    # -------------------------
    # 4. ЧИСТКА СТРОКИ
    # -------------------------
    text = re.sub(r"[^\w\sа-яА-ЯёЁ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text