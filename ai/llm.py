import gc
import os
import threading

import llama_cpp
from llama_cpp import Llama

from core import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "qwen", "Qwen2.5-3B-Instruct-Q4_K_M.gguf")

JARVIS_PROMPT = """Ты JARVIS — персональный голосовой AI-ассистент.
- отвечай только на русском языке, кратко (1–3 предложения)
- называй пользователя «сэр»
- не выдумывай факты; если ответа нет в памяти — скажи, что не знаешь
- не повторяй вопрос и не говори, что ты языковая модель
- без markdown, списков и эмодзи: ответ будет озвучен"""

_llm = None
_loaded_device = None
_lock = threading.Lock()


def gpu_available():
    """True, если llama-cpp-python собран с поддержкой видеокарты (CUDA/Vulkan)."""
    try:
        return bool(llama_cpp.llama_supports_gpu_offload())
    except Exception:
        return False


def _wanted_device():
    dev = str(getattr(config, "LLM_DEVICE", "cpu")).lower()
    if dev in ("gpu", "cuda"):
        if gpu_available():
            return "gpu"
        print("⚠️ llama-cpp-python без поддержки GPU — работаю на CPU")
    return "cpu"


def _get_llm():
    global _llm, _loaded_device
    if _llm is None:
        device = _wanted_device()
        gpu_layers = int(getattr(config, "LLM_GPU_LAYERS", -1)) if device == "gpu" else 0
        threads = int(getattr(config, "LLM_THREADS", 0)) or max(2, (os.cpu_count() or 4) // 2)

        print(f"🧠 Loading LLM on {device.upper()} (gpu_layers={gpu_layers}, threads={threads})...")
        _llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=int(getattr(config, "LLM_CTX", 4096)),
            n_threads=threads,
            n_gpu_layers=gpu_layers,
            verbose=False,
        )
        _loaded_device = device
        print(f"🧠 LLM READY ({device.upper()})")
    return _llm


def current_device():
    """'cpu' / 'gpu' / None (модель ещё не загружена)."""
    return _loaded_device


def unload():
    global _llm, _loaded_device
    with _lock:
        if _llm is not None:
            try:
                _llm.close()
            except Exception:
                pass
            _llm = None
            _loaded_device = None
            gc.collect()
            print("🧠 LLM UNLOADED")


def set_device(device):
    """Переключить устройство. Модель перезагрузится при следующем запросе."""
    device = "gpu" if str(device).lower() in ("gpu", "cuda") else "cpu"
    config.set_config("LLM_DEVICE", device)
    unload()
    return device


def preload():
    try:
        with _lock:
            _get_llm()
    except Exception as e:
        print("LLM LOAD ERROR:", e)


def generate(messages, temperature=0.7, max_tokens=300):
    with _lock:
        resp = _get_llm().create_chat_completion(
            messages=messages, temperature=temperature, max_tokens=max_tokens
        )
    return resp["choices"][0]["message"]["content"].strip()


def complete(prompt, system=JARVIS_PROMPT, temperature=0.3, max_tokens=300):
    try:
        return generate(
            [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as e:
        print("LLAMA ERROR:", e)
        return ""


def ask_ai(text, memory_context="", history=None):
    system = JARVIS_PROMPT
    if memory_context:
        system += f"\n\nПАМЯТЬ О ПОЛЬЗОВАТЕЛЕ:\n{memory_context}"

    messages = [{"role": "system", "content": system}]
    for role, msg in history or []:
        messages.append({"role": "user" if role == "user" else "assistant", "content": msg})
    messages.append({"role": "user", "content": text})

    try:
        return generate(messages)
    except Exception as e:
        print("LLAMA ERROR:", e)
        return "Локальный ИИ недоступен, сэр."