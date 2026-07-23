import os
import sounddevice as sd
import queue
import json
import threading
from core.config import MICROPHONE_NAME
from vosk import Model, KaldiRecognizer
print("USING VOSK FILE:")
print(__file__)


class VoskEngine:

    def __init__(self):

        print("Loading Vosk...")
        print("MY VOSK VERSION")
        

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "vosk")

        print("BASE =", base_dir)
        print("MODEL PATH =", model_path)
        print("EXISTS =", os.path.exists(model_path))

        self.model = Model(model_path)

        self.device = None

        devices = sd.query_devices()

        for i, dev in enumerate(devices):

            if dev["max_input_channels"] > 0:

                print(i, dev["name"])

                if MICROPHONE_NAME.lower() in dev["name"].lower():
                    self.device = i
                    break

        if self.device is None:
            raise Exception(
                f'Микрофон "{MICROPHONE_NAME}" не найден'
            )

        device_info = sd.query_devices(self.device, "input")
        self.samplerate = int(device_info["default_samplerate"])

        print("MIC =", device_info["name"])

        self.q = queue.Queue()
        self.text_q = queue.Queue()

        self.rec = KaldiRecognizer(self.model, self.samplerate)

        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            device=self.device,
            channels=1,
            dtype="int16",
            callback=self.callback
        )

        self.stream.start()

        threading.Thread(target=self._loop, daemon=True).start()

        print("Vosk READY")

    def reset(self):

        print("🔄 VOSK RESET")

        self.rec = KaldiRecognizer(
            self.model,
            self.samplerate
        )

        # чистим старые распознанные фразы
        while not self.text_q.empty():
            try:
                self.text_q.get_nowait()
            except:
                break

        # чистим аудио-буфер
        while not self.q.empty():
            try:
                self.q.get_nowait()
            except:
                break

    def callback(self, indata, frames, time, status):

        data = bytes(indata)

        # тут будет Rustpotter
        # если услышал Jarvis:
        # self.wake_detected = True

        self.q.put(data)

    def _loop(self):

        while True:

            data = self.q.get()

            if self.rec.AcceptWaveform(data):

                result = json.loads(
                    self.rec.Result()
                )

                text = result.get("text", "")

                if text:
                    self.text_q.put(text)

    def get_text(self):
        try:
            return self.text_q.get_nowait()
        except:
            return None

    def stop(self):

        try:
            self.stream.stop()
            self.stream.close()
        except:
            pass
# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------