PHRASES = [

    "обнови плагины",
    "перезагрузи плагины",
    "обновить плагины"

]


def run(jarvis, text):

    jarvis.plugins.reload()

    jarvis.say(
        "Плагины обновлены"
    )