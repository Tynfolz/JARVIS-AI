"""Wake-word на базе Vosk (keyword spotting).

Использует уже установленную модель Vosk. Менее точен для wake-word,
чем Porcupine, но не требует внешнего ключа.
"""

import os
import json
import queue
import threading
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from core.config import MICROPHONE_NAME


class VoskWakeWord:
    def __init__(self, keywords=("джарвис",), threshold=0.5):
        self._keywords = set(k.lower() for k in keywords)
        self._threshold = threshold
        self._queue = queue.Queue()
        self._stop = False

        # Загрузка модели Vosk
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "vosk")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель Vosk не найдена: {model_path}")

        self.model = Model(model_path)

        # Аудиострим
        self.device = self._find_device()
        device_info = sd.query_devices(self.device, "input")
        self.sample_rate = int(device_info["default_samplerate"])

        self.rec = KaldiRecognizer(self.model, self.sample_rate)
        # Включаем частичные результаты для быстрого реагирования
        self.rec.SetWords(True)

        self.stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            device=self.device,
            channels=1,
            dtype="int16",
            callback=self._callback
        )
        self.stream.start()

        # Инициализируем очередь ДО запуска потока
        self._audio_queue = queue.Queue()

        # Фоновый поток обработки
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

        print(f"🟢 Vosk WakeWord запущен: keywords={self._keywords}, threshold={self._threshold}")

    def _find_device(self):
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0 and MICROPHONE_NAME.lower() in dev["name"].lower():
                return i
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:
                print(f"⚠️ Микрофон '{MICROPHONE_NAME}' не найден, использую: {dev['name']}")
                return i
        raise Exception("Нет доступных микрофонов")

    def _callback(self, indata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")
        data = bytes(indata)
        self._audio_queue.put(data)

    def _loop(self):
        while not self._stop:
            try:
                data = self._audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get("text", "").lower()
                self._check_keywords(text)
            else:
                # Частичный результат — быстрее, но менее точно
                partial = json.loads(self.rec.PartialResult())
                text = partial.get("partial", "").lower()
                self._check_keywords(text, partial=True)

    def _check_keywords(self, text, partial=False):
        for kw in self._keywords:
            if kw in text:
                # Для частичных результатов требуем более высокий порог уверенности
                if partial:
                    # В частичных результатах нет confidence, используем эвристику
                    if len(text) >= len(kw) * 0.8:
                        self._queue.put(time.monotonic())
                        return
                else:
                    self._queue.put(time.monotonic())
                    return

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


# Алиас для совместимости
WakeWord = VoskWakeWord