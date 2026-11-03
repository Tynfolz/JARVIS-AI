PRIORITY = 20
PREFIXES = ("смени город на", "сменить город на", "поменяй город на")


def match(text):
    return text.startswith(PREFIXES)


def run(jarvis, text):
    city = next((text[len(p):] for p in PREFIXES if text.startswith(p)), "").strip()
    if not city:
        jarvis.say("Не удалось определить город")
        return True

    city = " ".join(w.capitalize() for w in city.split())
    jarvis.config.set("WEATHER_CITY", city)
    jarvis.say(f"Город изменён на {city}")
    return True