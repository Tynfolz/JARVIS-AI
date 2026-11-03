PHRASES = [

    "открой телеграм",
    "запусти телеграм",
    "открой telegram"

]


def run(jarvis, text):

    jarvis.open.program(
        "telegram"
    )

    jarvis.say(
        "Открываю Telegram"
    )