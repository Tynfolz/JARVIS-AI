PHRASES = [

    "открой дискорд",
    "запусти дискорд",
    "открой дискорд"

]


def run(jarvis, text):


    if jarvis.apps.open(
        "discord"
    ):

        jarvis.say(
            "Открываю дискорд"
        )


    else:

        jarvis.say(
            "дискорд не найден"
        )