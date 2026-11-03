PHRASES = [

    "открой корзину",
    "покажи корзину"

]


def run(jarvis, text):

    jarvis.open.program(
        "explorer.exe shell:RecycleBinFolder"
    )

    jarvis.say(
        "Открываю корзину"
    )