import whisper
import sounddevice as sd
import numpy as np

class WakeListener:

    def __init__(self):

        print("Loading Whisper...")

        self.model = whisper.load_model("base")

        print("Whisper READY")

        self.samplerate = 48000

    def record(self, seconds=2):

        audio = sd.rec(
            int(seconds * self.samplerate),
            samplerate=self.samplerate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        return np.squeeze(audio)

    def listen_for_wake_word(self):

        audio = self.record(2)

        level = np.max(np.abs(audio))
        print("AUDIO LEVEL:", level)

        if level < 0.01:
            return False

        result = self.model.transcribe(
            audio,
            language="ru",
            temperature=0
        )

        text = result["text"].lower().strip()

        print("WAKE HEARD:", text)

        # 🔥 WAKE WORD
        return "джарвис" in text

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------