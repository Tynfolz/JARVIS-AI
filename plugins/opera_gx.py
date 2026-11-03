PHRASES = [

    "открой оперу гх",
    "открой opera gx"

]


def run(jarvis, text):

    if jarvis.apps.open("Opera GX"):

        jarvis.say("Открываю Opera GX")

    else:

        jarvis.say("Не удалось найти Opera GX")