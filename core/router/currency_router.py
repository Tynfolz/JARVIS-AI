from api.currency import get_currency
from voice.tts import speak


class CurrencyRouter:

    def __init__(self):
        self.words = [

            "доллар",
            "евро",
            "гривна",
            "фунт",
            "юань",
            "тенге",
            "рубль",
            "злотый",

        ]

    def process(self, query):

        if not any(word in query for word in self.words):
            return False

        try:

            answer = get_currency(query)

            print("CURRENCY:", answer)

            speak(answer)

        except Exception as e:

            print("CURRENCY ERROR:", e)

            speak("Не удалось получить курс валюты")

        return True

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------