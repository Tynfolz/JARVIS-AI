import requests


CURRENCY_NAMES = {

    "доллар": "USD",
    "доллара": "USD",
    "долларов": "USD",

    "евро": "EUR",

    "гривна": "UAH",
    "гривны": "UAH",
    "гривен": "UAH",

    "фунт": "GBP",
    "фунта": "GBP",

    "юань": "CNY",
    "юаня": "CNY",

    "тенге": "KZT",

    "злотый": "PLN",
    "злотых": "PLN",
}


DISPLAY_NAMES = {

    "USD": "доллар",
    "EUR": "евро",
    "UAH": "гривна",
    "GBP": "фунт",
    "CNY": "юань",
    "KZT": "тенге",
    "PLN": "злотый"

}


def get_currency_code(text):

    for word, code in CURRENCY_NAMES.items():

        if word in text:
            return code

    return None



def get_currency(text):

    code = get_currency_code(text)

    if not code:
        return None


    try:

        data = requests.get(
            f"https://open.er-api.com/v6/latest/{code}",
            timeout=10
        ).json()


        rub = data["rates"]["RUB"]


        return (
            f"Один {DISPLAY_NAMES[code]} "
            f"стоит {round(rub,2)} рублей"
        )


    except Exception as e:

        print("CURRENCY ERROR:",e)

        return "Не удалось получить курс валют"

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------