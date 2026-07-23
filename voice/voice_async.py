import threading
from voice.tts import speak


def speak_async(text):

    threading.Thread(
        target=speak,
        args=(text,),
        daemon=True
    ).start()

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------
