from core import config

PRIORITY = 10
TRIGGERS = ("погод", "температур", "градус", "на улице", "дожд", "снег", "ветер", "прогноз")

RULES = (
    "Ответь только про погоду, кратко, используя только данные ниже. Не выдумывай. "
    "Не используй сокращения: вместо '°C' говори 'градусов', "
    "вместо 'мм рт. ст.' говори 'миллиметров ртутного столба'."
)


def match(text):
    return any(t in text for t in TRIGGERS)


def run(jarvis, text):
    city = config.WEATHER_CITY
    print("WEATHER CITY:", city)

    results = jarvis.ai.search(f"погода {city} {text}")
    if not results:
        jarvis.say("Не удалось получить погоду")
        return True

    data = "\n\n".join(f"{r['title']}\n{r['body']}" for r in results[:3])
    answer = jarvis.ai.ask(f"Город: {city}\nЗапрос: {text}\n\nДанные:\n{data}", rules=RULES)

    answer = (
        answer.replace("°C", " градусов")
        .replace("°", " градусов")
        .replace("мм рт. ст.", " миллиметров ртутного столба")
        .replace("мм рт.", " миллиметров ртутного столба")
    )
    print("WEATHER:", answer)
    jarvis.say(answer or "Не удалось получить погоду")
    return True