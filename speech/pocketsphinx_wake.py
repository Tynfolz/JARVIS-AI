"""Wake-word на базе PocketSphinx (CMU). Бесплатный, полностью офлайн."""

import os
import time
import queue
import threading
import sounddevice as sd
from pocketsphinx import LiveSpeech, get_model_path
from core.config import MICROPHONE_NAME


class PocketSphinxWakeWord:
    def __init__(self, keyword="jarvis", threshold=1e-20):
        self._queue = queue.Queue()
        self._stop = False
        self.sample_rate = 16000

        model_root = get_model_path()
        hmm_path = os.path.join(model_root, "en-us", "en-us")
        if not os.path.isfile(os.path.join(hmm_path, "mdef")):
            raise RuntimeError(f"Акустическая модель не найдена: {hmm_path}\\mdef")

        last_err = None
        for idx, hostapi, name in self._device_candidates():
            try:
                sd.check_input_settings(device=idx, samplerate=self.sample_rate,
                                        channels=1, dtype="int16")
            except Exception as e:
                print(f"⏭  [{idx}] {name} ({hostapi}) не поддерживает 16 кГц: {e}")
                last_err = e
                continue

            try:
                self.speech = LiveSpeech(
                    audio_device=idx,
                    sampling_rate=self.sample_rate,
                    hmm=hmm_path,
                    lm=False,
                    keyphrase=keyword,
                    kws_threshold=threshold,
                )
                self.device = idx
                print(f"🎤 Открыт микрофон [{idx}] {name} ({hostapi}) @ 16 кГц")
                break
            except Exception as e:
                print(f"⏭  [{idx}] {name} ({hostapi}) не открылся: {e}")
                last_err = e
                continue
        else:
            raise RuntimeError(f"Не удалось открыть ни один микрофон на 16 кГц. "
                               f"Последняя ошибка: {last_err}")

        threading.Thread(target=self._loop, daemon=True, name="pocketsphinx-wake").start()
        print(f"🟢 PocketSphinx WakeWord запущен (keyword='{keyword}', device={self.device})")

    def _device_candidates(self):
        priority = {"Windows DirectSound": 0, "Windows WASAPI": 1}
        cand = []
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0 and MICROPHONE_NAME.lower() in dev["name"].lower():
                hostapi = sd.query_hostapis(dev["hostapi"])["name"]
                cand.append((i, hostapi, dev["name"]))
        cand.sort(key=lambda c: priority.get(c[1], 99))
        return cand

    def _loop(self):
        for phrase in self.speech:
            if self._stop:
                break
            if phrase.segments():
                self._queue.put(time.monotonic())

    def listen(self, timeout=0.5):
        try:
            self._queue.get(timeout=timeout)
            return True
        except queue.Empty:
            return False

    def stop(self):
        self._stop = True

    def clear(self):
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass

    def block(self, seconds: float):
        time.sleep(seconds)

    POST_SLEEP_BLOCK = 2.0


WakeWord = PocketSphinxWakeWord