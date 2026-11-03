PRIORITY = 20
PREFIXES = ("смени голос на", "сменить голос на", "поменяй голос на")
VOICES = {"дмитрий": "dmitri", "ирина": "irina", "руслан": "ruslan"}


def match(text):
    return text.startswith(PREFIXES)


def run(jarvis, text):
    name = next((text[len(p):] for p in PREFIXES if text.startswith(p)), "").strip()
    voice = VOICES.get(name)

    if not voice:
        jarvis.say("Такого голоса нет. Доступны: " + ", ".join(VOICES))
        return True

    jarvis.config.set("PIPER_VOICE", voice)
    jarvis.say(f"Голос изменён на {name}")
    return True