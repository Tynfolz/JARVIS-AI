import subprocess


PHRASES = [

    "иди поспи",
    "иди спать",
    "я спать",
    "я пошел спать",
    "я пошёл спать",
    "пойду спать",
    "отправь компьютер спать",
    "уложи компьютер спать",
    "компьютер спать"

]


def run(jarvis, text):

    jarvis.say(
        "Хорошо. Спокойной ночи."
    )

    subprocess.Popen(
        ["shutdown", "/h"],
        shell=False
    )