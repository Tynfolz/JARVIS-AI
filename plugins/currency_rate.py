from api.currency import get_currency, get_currency_code

PRIORITY = 5


def match(text):
    return get_currency_code(text) is not None


def run(jarvis, text):
    answer = get_currency(text)
    print("CURRENCY:", answer)
    jarvis.say(answer or "Не удалось получить курс валюты")
    return True