import sounddevice as sd
import numpy as np

class WakeWord:

    def __init__(self):

        self.device = 9   # 🔥 стабильный ME6S
        self.samplerate = 44100

    def listen(self):

        audio = sd.rec(
            int(1.5 * self.samplerate),
            samplerate=self.samplerate,
            channels=1,
            dtype="float32",
            device=self.device
        )

        sd.wait()

        audio = np.squeeze(audio)

        level = np.max(np.abs(audio))

        print("WAKE LEVEL:", level)

        return level > 0.03
