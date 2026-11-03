import re
import threading
import time
from datetime import datetime, timedelta

PRIORITY = 50

TIME_PHRASES = (
    "сколько времени", "который час", "сколько время",
    "время скажи", "скажи время", "сколько сейчас времени",
)
KEYWORDS = ("таймер", "секундомер", "будильник")

NUMBERS = {
    "ноль": 0, "один": 1, "одна": 1, "одну": 1, "два": 2, "две": 2, "три": 3,
    "четыре": 4, "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9,
    "десять": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13,
    "четырнадцать": 14, "пятнадцать": 15, "шестнадцать": 16, "семнадцать": 17,
    "восемнадцать": 18, "девятнадцать": 19, "двадцать": 20, "тридцать": 30,
    "сорок": 40, "пятьдесят": 50,
}
TENS = {20, 30, 40, 50}

_state = {"stopwatch": None, "awaiting_alarm": False}


def reset():
    _state["awaiting_alarm"] = False


def match(text):
    if _state["awaiting_alarm"]:
        return 100
    return any(p in text for p in TIME_PHRASES) or any(k in text for k in KEYWORDS)


def extract_numbers(text):
    words = re.sub(r"[:.,]", " ", text).split()
    nums, i = [], 0
    while i < len(words):
        w = words[i]
        if w.isdigit():
            nums.append(int(w))
        elif w in NUMBERS:
            value = NUMBERS[w]
            nxt = words[i + 1] if i + 1 < len(words) else ""
            if value in TENS and 0 < NUMBERS.get(nxt, 0) < 10:
                value += NUMBERS[nxt]
                i += 1
            nums.append(value)
        i += 1
    return nums


def plural(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def duration_text(seconds):
    h, rest = divmod(int(seconds), 3600)
    m, s = divmod(rest, 60)
    parts = []
    if h:
        parts.append(f"{h} {plural(h, 'час', 'часа', 'часов')}")
    if m:
        parts.append(f"{m} {plural(m, 'минута', 'минуты', 'минут')}")
    if s or not parts:
        parts.append(f"{s} {plural(s, 'секунда', 'секунды', 'секунд')}")
    return " ".join(parts)


def parse_duration(text):
    nums = extract_numbers(text)
    value = nums[0] if nums else 1
    if "мин" in text:
        return value * 60
    if "сек" in text:
        return value
    if "час" in text:
        return value * 3600
    return 0


def start_timer(jarvis, seconds):
    def worker():
        time.sleep(seconds)
        jarvis.say("Сэр, время вышло.")

    threading.Thread(target=worker, daemon=True).start()
    jarvis.say(f"Таймер запущен: {duration_text(seconds)}")


def set_alarm(jarvis, hour, minute):
    if not (0 <= hour < 24 and 0 <= minute < 60):
        jarvis.say("Некорректное время")
        return

    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)

    def worker():
        while datetime.now() < target:
            time.sleep(5)
        jarvis.say("Сэр, сработал будильник.")

    threading.Thread(target=worker, daemon=True).start()
    jarvis.say(f"Будильник установлен на {hour:02d}:{minute:02d}")


def run(jarvis, text):
    if _state["awaiting_alarm"]:
        _state["awaiting_alarm"] = False
        nums = extract_numbers(text)
        if not nums:
            return False
        set_alarm(jarvis, nums[0], nums[1] if len(nums) > 1 else 0)
        return True

    if any(p in text for p in TIME_PHRASES):
        jarvis.say(f"Сейчас {datetime.now():%H:%M}")
        return True

    if "будильник" in text:
        nums = extract_numbers(text)
        if nums:
            set_alarm(jarvis, nums[0], nums[1] if len(nums) > 1 else 0)
        else:
            _state["awaiting_alarm"] = True
            jarvis.say("На какое время, сэр?")
        return True

    if "секундомер" in text:
        if any(w in text for w in ("стоп", "останов", "выключ", "сколько")):
            start = _state["stopwatch"]
            if not start:
                jarvis.say("Секундомер не запущен")
            else:
                _state["stopwatch"] = None
                jarvis.say(f"Прошло {duration_text(time.time() - start)}")
        else:
            _state["stopwatch"] = time.time()
            jarvis.say("Секундомер запущен")
        return True

    if "таймер" in text:
        seconds = parse_duration(text)
        if not seconds:
            jarvis.say("Не понял время таймера")
            return True
        start_timer(jarvis, seconds)
        return True

    return False