import subprocess
import tempfile
import os

import sounddevice as sd
import soundfile as sf

from core import config


BASE = os.path.dirname(
    os.path.dirname(__file__)
)


PIPER = os.path.join(
    BASE,
    "models",
    "piper",
    "piper.exe"
)


VOICES = {

    "dmitri":
        "ru_RU-dmitri-medium.onnx",

    "ruslan":
        "ru_RU-ruslan-medium.onnx",

    "irina":
        "ru_RU-irina-medium.onnx",
}


def get_voice_path():

    voice_name = config.PIPER_VOICE

    if voice_name not in VOICES:
        voice_name = "ruslan"

    return os.path.join(
        BASE,
        "models",
        "piper",
        "voices",
        VOICES[voice_name]
    )



def speak(text):

    if not text:
        return


    text = str(text).strip()


    if not text:
        return


    try:

        fd, wav = tempfile.mkstemp(
            suffix=".wav"
        )

        os.close(fd)


        process = subprocess.Popen(
            [
                PIPER,

                "--model",
                get_voice_path(),

                "--output_file",
                wav,


                "--length_scale",
                str(config.PIPER_LENGTH_SCALE),


                "--noise_scale",
                str(config.PIPER_NOISE_SCALE),


                "--noise_w",
                str(config.PIPER_NOISE_W),
            ],

            stdin=subprocess.PIPE,

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL,

            text=True,

            encoding="utf-8"
        )


        process.communicate(text)



        audio, sr = sf.read(
            wav,
            dtype="float32"
        )


        sd.stop()

        sd.play(
            audio,
            sr
        )

        sd.wait()


        os.remove(wav)


    except Exception as e:

        print(
            "PIPER ERROR:",
            e
        )


# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------