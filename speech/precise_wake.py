"""Wake‑word на базе Mycroft Precise (open‑source, полностью локальный).

Требуется пакет `precise-runner`. Установить:
    pip install precise-runner==0.3.1

Если хотите обучить собственную модель, см. гайд в конце.
"""

import os
import time
import queue
import threading
import sounddevice as sd
from precise_runner import PreciseRunner
from core.config import MICROPHONE_NAME


class PreciseWakeWord:
    def __init__(self, model_path="models/precise/jarvis.tflite"):
        self._queue = queue.Queue()
        self._stop = False

        # Находим микрофон
        self.device = self._find_device()
        device_info = sd.query_devices(self.device, "input")
        self.sample_rate = int(device_info["default_samplerate"])

        # Precise требует 16 kHz — если микрофон другой частоты, нужен ресэмплинг.
        # PreciseRunner умеет делать это сам, если указать sample_rate=16000.
        target_sample_rate = 16000

        trigger_level = getattr(__import__("core.config", fromlist=["PRECISE_TRIGGER_LEVEL"]), "PRECISE_TRIGGER_LEVEL", 0.5)

        # PreciseRunner запускает свой поток и сам читает с микрофона.
        # Колбэк on_activation вызывается при срабатывании.
        from precise_runner import PreciseEngine

        # Инициализация движка
        self.engine = PreciseEngine(
            exe_file=["precise-engine"],  # имя файла без расширения
            model_file=model_path,
        )

        # Запуск PreciseRunner с колбэками
        self.runner = PreciseRunner(
            engine=self.engine,
            trigger_level=trigger_level,
            on_activation=self._on_activation,
        )
        self.runner.start()
        print(f"🟢 Precise WakeWord запущен (model={model_path}, level={trigger_level}, device={self.device})")

    def _find_device(self):
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0 and MICROPHONE_NAME.lower() in dev["name"].lower():
                return i
        raise Exception(f"Микрофон '{MICROPHONE_NAME}' не найден")

    def _on_activation(self):
        """Вызывается PreciseRunner'ом, когда детектор уверенно услышал слово."""
        self._queue.put(time.monotonic())

    def _on_prediction(self, confidence):
        """Вызывается на каждом чанке (можно использовать для отладки)."""
        # print(f"  Precise confidence: {confidence:.3f}")
        pass

    # API, совместимый с rustpotter
    def listen(self, timeout=0.5):
        try:
            self._queue.get(timeout=timeout)
            return True
        except queue.Empty:
            return False

    def stop(self):
        self._stop = True
        try:
            self.runner.stop()
        except Exception:
            pass

    # Совместимость с rustpotter
    def clear(self):
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass

    def block(self, seconds: float):
        time.sleep(seconds)

    POST_SLEEP_BLOCK = 2.0

# Алиас для совместимости
WakeWord = PreciseWakeWord