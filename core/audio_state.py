# core/audio_state.py
# Общий «пульс» микрофона для фильтрации wake-word без поднятия порога.
#
# VoskEngine кормит сюда каждый блок PCM (int16) из своего callback.
# Здесь считается RMS (громкость) и хранится кольцо последних значений.
# WakeWord использует это, чтобы отклонять детекции Rustpotter, которые
# пришлись на постоянный шум/музыку (нет ни одной «тихой» точки в окне),
# а не на человеческую речь (тишина → всплеск «джарвис»).

import array
import math
import threading
import time
from collections import deque

_RING = deque(maxlen=1200)   # ~ 1200 блоков × ~42 мс ≈ 50 с
_LOCK = threading.Lock()


def feed(indata) -> None:
    """Скормить блок PCM int16 (байты или numpy-массив int16)."""
    try:
        if hasattr(indata, "tobytes"):
            raw = indata.tobytes()
        else:
            raw = bytes(indata)
        a = array.array("h")
        a.frombytes(raw)
        n = len(a)
        if not n:
            return
        s = 0
        for v in a:
            s += v * v
        rms = math.sqrt(s / n) / 32768.0
    except Exception:
        return

    now = time.monotonic()
    with _LOCK:
        _RING.append((now, rms))


def current_rms() -> float:
    with _LOCK:
        if not _RING:
            return 0.0
        return _RING[-1][1]


def recent_silence(window: float, silence_thr: float) -> bool:
    """Была ли хотя бы одна «тихая» точка (RMS < silence_thr) за последние `window` сек.

    Устойчивый громкий фон (музыка, ТВ, вентиляторы) таких точек не даёт —
    значит детекция Rustpotter скорее всего ложная.
    """
    now = time.monotonic()
    with _LOCK:
        for ts, rms in _RING:
            if now - ts > window:
                continue
            if rms < silence_thr:
                return True
    return False


def loud_fraction(window: float, loud_thr: float) -> float:
    """Доля «громких» блоков микрофона за последние `window` сек.

    >0.5 в комбинации с «тихой точкой» — признак музыки/ТВ с паузами:
    Rustpotter попал в паузу трека, а не в человеческую речь. Реальная
    «джарвис» произносится на фоне тихого помещения, где громких блоков почти нет.
    """
    now = time.monotonic()
    total = 0
    loud = 0
    with _LOCK:
        for ts, rms in _RING:
            if now - ts > window:
                continue
            total += 1
            if rms >= loud_thr:
                loud += 1
    if not total:
        return 0.0
    return loud / total