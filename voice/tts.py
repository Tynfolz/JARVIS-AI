import subprocess
import tempfile
import os
import threading
import time

import numpy as np
import sounddevice as sd
import soundfile as sf

from core import config
from core.audio_state import feed as audio_state_feed


BASE = os.path.dirname(
    os.path.dirname(__file__)
)


# ---------------------------------------------------------------
# Время окончания последнего воспроизведения TTS.
# WakeWord не срабатывает, пока идёт или только что дошла речь Джарвиса:
# иначе он «будит сам себя» своим же приветствием/ответом.
# ---------------------------------------------------------------
_tts_finish_lock = threading.Lock()
_tts_finished_at = 0.0


def note_tts_finished():
    global _tts_finished_at
    with _tts_finish_lock:
        _tts_finished_at = time.monotonic()


def tts_quiet_since() -> float:
    with _tts_finish_lock:
        return _tts_finished_at


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


        # Подавляем собственный голос: пока играет TTS, wake-word не будит.
        sd.stop()

        sd.play(
            audio,
            sr
        )

        # Подмешиваем копию PCM в rms-пульс (тоже «тихая» зона на время речи).
        try:
            pcm = (np.clip(audio, -1.0, 1.0) * 32767.0).astype(np.int16)
            audio_state_feed(pcm.tobytes())
        except Exception:
            pass

        sd.wait()


        os.remove(wav)

        note_tts_finished()


    except Exception as e:

        print(
            "PIPER ERROR:",
            e
        )


# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------