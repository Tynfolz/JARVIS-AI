import re
print("TTS 1")
import numpy as np
print("TTS 2")
import sounddevice as sd
print("TTS 3")
import torch
print("TTS 4")
from num2words import num2words
print("TTS 5")
import os
print("TTS FILE =", __file__)


# -------------------------
# LOAD MODEL
# -------------------------
try:
    print("TTS 6")

    model, _ = torch.hub.load(
        "snakers4/silero-models",
        "silero_tts",
        language="ru",
        speaker="v4_ru",
        trust_repo=True
    )

    print("TTS 7")

except Exception:
    import traceback
    traceback.print_exc()
    input("Ошибка загрузки Silero...")
    raise

SAMPLE_RATE = 48000
SPEAKER = "aidar"

# уменьшение лагов
sd.default.latency = ("low", "low")


# -------------------------
# NUMBERS -> WORDS
# -------------------------
def numbers_to_words(text):

    def repl(match):
        try:
            num = int(match.group())
            return num2words(num, lang="ru")
        except:
            return match.group()

    return re.sub(r"\d+", repl, text)


# -------------------------
# CLEAN TEXT
# -------------------------
def clean_text(text: str):

    if not text:
        return ""

    text = str(text).lower()

    # -------------------------
    # markdown / мусор
    # -------------------------
    text = text.replace("*", " ")
    text = text.replace("_", " ")
    text = text.replace("#", " ")
    text = text.replace("•", " ")

    # -------------------------
    # тире между словами
    # -------------------------
    text = re.sub(r"\s-\s", " ", text)

    # -------------------------
    # отрицательные числа
    # -------------------------
    text = re.sub(r"-(\d+)", r"минус \1", text)

    # -------------------------
    # символы
    # -------------------------
    text = text.replace("+", " плюс ")
    text = text.replace("=", " равно ")
    text = text.replace("%", " процентов ")
    text = text.replace("°", " градусов ")

    # -------------------------
    # числа словами
    # -------------------------
    text = numbers_to_words(text)

    # -------------------------
    # убрать английский
    # -------------------------
    text = re.sub(r"[a-zA-Z]", " ", text)

    # -------------------------
    # оставить только русские символы
    # -------------------------
    text = re.sub(r"[^0-9а-яё\s\.\,\!\?]", " ", text)

    # -------------------------
    # пробелы
    # -------------------------
    text = re.sub(r"\s+", " ", text).strip()

    # -------------------------
    # убрать пробелы перед знаками
    # -------------------------
    text = text.replace(" .", ".")
    text = text.replace(" ,", ",")
    text = text.replace(" !", "!")
    text = text.replace(" ?", "?")

    return text


# -------------------------
# SPEAK
# -------------------------
def speak(text: str):

    try:

        text = clean_text(text)

        if not text or len(text) < 2:
            return

        print("JARVIS TTS:", text)

        # -------------------------
        # TTS
        # -------------------------
        audio = model.apply_tts(
            text=text,
            speaker=SPEAKER,
            sample_rate=SAMPLE_RATE
        )

        # -------------------------
        # SPEED UP
        # -------------------------
        speed = 1.12

        indices = np.round(
            np.arange(0, len(audio), speed)
        ).astype(int)

        indices = indices[indices < len(audio)]

        audio = audio[indices]

        # -------------------------
        # PLAY AUDIO
        # -------------------------
        sd.stop()

        sd.play(audio, SAMPLE_RATE)

        sd.wait()

        sd.stop()

    except Exception as e:
        print("TTS ERROR:", e)