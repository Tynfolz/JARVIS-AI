from core import config
from ai.search import web_search
from ai.ai_hybrid import ask_ai
from voice.tts import speak


class WeatherRouter:

    def process(self, text):

        weather_words = [

            "погода",
            "температура",
            "градусов",
            "на улице",
            "дождь",
            "снег",
            "ветер",
            "завтра",
            "сегодня",

        ]

        if not any(word in text for word in weather_words):
            return False

        city = config.WEATHER_CITY

        print("WEATHER SEARCH CITY:", city)

        results = web_search(
            f"погода {city} {text}"
        )

        if not results:

            speak("Не удалось получить погоду")

            return True

        context = ""

        for r in results[:3]:

            context += f"""

Заголовок:
{r['title']}

Описание:
{r['body']}

"""

        prompt = f"""
Ты JARVIS.

Ответь только про погоду.

Город:
{city}

Запрос:
{text}

Данные:
{context}

Отвечай естественно.

Не используй сокращения.

Вместо:

°C

говори

градусов.

Вместо

мм рт.

говори

миллиметров ртутного столба.

Не выдумывай.
"""

        answer = ask_ai(prompt)

        answer = (
            answer
            .replace("°C", " градусов")
            .replace("°", " градусов")
            .replace("мм рт.", " миллиметров ртутного столба")
            .replace("мм рт", " миллиметров ртутного столба")
        )

        print("WEATHER:", answer)

        speak(answer)

        return True

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------