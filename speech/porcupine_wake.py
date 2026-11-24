"""Wake-word на базе Picovoice Porcupine.

Точный, быстрый, промышленный стандарт. Бесплатен для личного использования.
Получите AccessKey: https://console.picovoice.ai/
"""

import pvporcupine
import sounddevice as sd
import numpy as np
import threading
import queue
import time
from core.config import MICROPHONE_NAME


class PorcupineWakeWord:
    def __init__(self, access_key: str, keywords=("jarvis",), sensitivities=(0.6,)):
        if not access_key:
            raise ValueError("Porcupine AccessKey не задан. Получите на https://console.picovoice.ai/")

        self._access_key = access_key
        self._keywords = list(keywords)
        self._sensitivities = list(sensitivities)
        self._queue = queue.Queue()
        self._stop = False

        # Инициализация Porcupine
        self.handle = pvporcupine.create(
            access_key=access_key,
            keywords=self._keywords,
            sensitivities=self._sensitivities
        )

        # Аудиострим
        self.device = self._find_device()
        device_info = sd.query_devices(self.device, "input")
        self.sample_rate = int(device_info["default_samplerate"])

        # Проверка совместимости sample rate
        if self.sample_rate != self.handle.sample_rate:
            print(f"⚠️ Sample rate микрофона ({self.sample_rate}) ≠ Porcupine ({self.handle.sample_rate}), будет ресэмплинг")

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            device=self.device,
            channels=1,
            dtype="int16",
            blocksize=self.handle.frame_length,
            callback=self._callback
        )
        self.stream.start()

        print(f"🟢 Porcupine запущен: keywords={self._keywords}, sensitivity={self._sensitivities}")

    def _find_device(self):
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0 and MICROPHONE_NAME.lower() in dev["name"].lower():
                return i
        # Fallback: первый доступный вход
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:
                print(f"⚠️ Микрофон '{MICROPHONE_NAME}' не найден, использую: {dev['name']}")
                return i
        raise Exception("Нет доступных микрофонов")

    def _callback(self, indata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")
        # Porcupine ожидает int16 mono
        pcm = indata[:, 0].astype(np.int16)
        keyword_index = self.handle.process(pcm)
        if keyword_index >= 0:
            self._queue.put(time.monotonic())

    def listen(self, timeout=0.5):
        """True, если только что прозвучало wake-word."""
        try:
            self._queue.get(timeout=timeout)
            return True
        except queue.Empty:
            return False

    def stop(self):
        self._stop = True
        try:
            self.stream.stop()
            self.stream.close()
        except Exception:
            pass
        try:
            self.handle.delete()
        except Exception:
            pass

    # Совместимость с API rustpotter
    def clear(self):
        """Выбросить накопленные события."""
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass

    def block(self, seconds: float):
        """Заблокировать срабатывание на N секунд (просто ждём)."""
        time.sleep(seconds)

    # Атрибут для совместимости
    POST_SLEEP_BLOCK = 2.0


# Алиас для совместимости со старым API
WakeWord = PorcupineWakeWord