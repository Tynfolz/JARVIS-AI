"""Фабрика для выбора движка wake-word.

Выбор движка настраивается в core/config.py:
    WAKE_ENGINE = "porcupine"  # "porcupine" | "vosk" | "rustpotter"
    PORCUPINE_ACCESS_KEY = "ваш_ключ"
    PORCUPINE_SENSITIVITY = 0.6
    VOSK_WAKE_KEYWORDS = ("джарвис",)
    VOSK_WAKE_THRESHOLD = 0.5
"""

from core import config


def create_wake_engine():
    """Создаёт экземпляр wake-word движка согласно настройкам."""
    engine = getattr(config, "WAKE_ENGINE", "rustpotter").lower()

    if engine == "porcupine":
        return _create_porcupine()
    elif engine == "vosk":
        return _create_vosk()
    elif engine == "rustpotter":
        return _create_rustpotter()
    elif engine == "pocketsphinx":
        return _create_pocketsphinx()
    else:
        raise ValueError(
            f"Неизвестный WAKE_ENGINE: {engine}. Доступные: porcupine, vosk, rustpotter, precise, pocketsphinx"
        )


def _create_porcupine():
    from speech.porcupine_wake import PorcupineWakeWord

    access_key = getattr(config, "PORCUPINE_ACCESS_KEY", "")
    sensitivity = getattr(config, "PORCUPINE_SENSITIVITY", 0.6)
    keywords = getattr(config, "PORCUPINE_KEYWORDS", ("jarvis",))

    return PorcupineWakeWord(
        access_key=access_key,
        keywords=keywords,
        sensitivities=(sensitivity,) * len(keywords)
    )


def _create_vosk():
    from speech.vosk_wake import VoskWakeWord

    keywords = getattr(config, "VOSK_WAKE_KEYWORDS", ("джарвис",))
    threshold = getattr(config, "VOSK_WAKE_THRESHOLD", 0.5)

    return VoskWakeWord(keywords=keywords, threshold=threshold)


def _create_rustpotter():
    from speech.wake_word import WakeWord as RustpotterWakeWord

    return RustpotterWakeWord()


def _create_pocketsphinx():
    from speech.pocketsphinx_wake import PocketSphinxWakeWord
    keyword = getattr(config, "POCKETSPHINX_KEYWORD", "jarvis")
    threshold = getattr(config, "POCKETSPHINX_THRESHOLD", 1e-20)
    return PocketSphinxWakeWord(keyword=keyword, threshold=threshold)


# Обратная совместимость: WakeWord = текущий движок
WakeWord = create_wake_engine