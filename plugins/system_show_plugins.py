PHRASES = [

    "покажи плагины",
    "какие плагины есть",
    "список плагинов"

]


def run(jarvis, text):

    plugins = jarvis.plugins.list()


    if not plugins:

        jarvis.say(
            "Нет загруженных плагинов"
        )

        return


    result = "Загружены плагины: "

    result += ", ".join(plugins)


    jarvis.say(result)