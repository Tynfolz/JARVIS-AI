# 🤖 JARVIS — Голосовой ассистент

Локальный голосовой ассистент на Python с плагинной архитектурой. Работает полностью офлайн (кроме веб-поиска, погоды, курсов валют).

---

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
# или для разработки:
pip install -e ".[dev]"
```

### 2. Модели (обязательно)
Скачай и положи в папку `models/`:
- **Vosk** (распознавание речи): `models/vosk/` — [vosk-model-ru-0.22](https://alphacephei.com/vosk/models)
- **Piper** (TTS): `models/piper/piper.exe` + голоса в `models/piper/voices/` — [piper releases](https://github.com/rhasspy/piper/releases)
- **Rustpotter** (wake-word): `models/rustpotter/rustpotter-cli.exe` — [rustpotter releases](https://github.com/Tynfolz/rustpotter/releases)
- **LLM** (опционально): `models/qwen/` — `.gguf` модель (например, Qwen2.5-7B-Instruct-Q4_K_M.gguf)

### 3. Запуск
```bash
python main.py
```

Параметры:
- `--no-tray` — без иконки в трее
- `--no-greet` — без приветствия при старте

---

## 🎯 Возможности

| Категория | Плагины |
|-----------|---------|
| **Система** | Перезагрузка, обновление плагинов, автообновление Jarvis |
| **Голос** | Смена голоса Piper (Дмитрий, Руслан, Ирина) |
| **Мультимедиа** | Spotify (play/pause/next/prev/volume), Spicetify bridge |
| **Инфо** | Погода, время, таймеры, будильники, курсы валют |
| **Веб** | Поиск (DuckDuckGo), открытие сайтов |
| **Память** | Запоминание фактов, контекст диалога, LLM-чат |
| **Мессенджеры** | Telegram, Discord (базовые команды) |

---

## 🗂 Структура проекта

```
jarvis/
├── main.py                 # Точка входа
├── core/
│   ├── config.py           # Настройки (микрофон, голоса, LLM, пороги)
│   ├── jarvis_router.py    # Главный роутер команд
│   ├── plugin_loader.py    # Загрузка плагинов + автоустановка deps
│   ├── jarvis_api.py       # API для плагинов (say, open, notify, etc.)
│   ├── phrases.py          # Фразы-ответы
│   └── apps/               # Индексатор установленных программ
├── plugins/                # 18 плагинов (каждый — отдельный .py файл)
├── speech/
│   ├── vosk_engine.py      # Распознавание речи (Vosk)
│   └── wake_word.py        # Wake-word (Rustpotter)
├── voice/
│   ├── tts.py              # Синтез речи (Piper)
│   └── voice_async.py      # Асинхронный TTS
├── ai/
│   ├── llm.py              # Локальная LLM (llama.cpp)
│   ├── memory_db.py        # SQLite: факты + история
│   └── memory_sorter.py    # Анализ памяти LLM
├── tray/                   # Системный трей
└── models/                 # Большие файлы (в .gitignore)
```

---

## ⚙️ Конфигурация

Основные настройки в `core/config.py`:

```python
MICROPHONE_NAME = "Razer Barracuda X 2.4"  # Твоё имя микрофона
PIPER_VOICE = "ruslan"                      # dmitri / ruslan / irina
LLM_DEVICE = "gpu"                          # "cpu" или "gpu"
LLM_GPU_LAYERS = -1                         # -1 = все слои на GPU
PLUGIN_MATCH_THRESHOLD = 80                 # Порог срабатывания плагина (0-100)
```

Менять можно:
1. Прямо в файле `core/config.py`
2. Через голос: *«Джарвис, настрой [параметр] [значение]»* (если есть плагин)
3. Программно: `from core.config import set_config; set_config("PIPER_VOICE", "dmitri")`

---

## 🔌 Добавление плагина

Создай файл `plugins/my_plugin.py`:

```python
PHRASES = [
    "мой плагин",
    "сделай что-нибудь",
]

def run(jarvis, text):
    jarvis.say("Плагин сработал!")
    return True
```

Плагин загрузится автоматически при следующем старте или команде *«обнови плагины»*.

Доступно в `jarvis`:
- `jarvis.say(text)` / `jarvis.say_async(text)` — озвучка
- `jarvis.open_app("name")` — запуск программы
- `jarvis.open_url("https://...")` — открыть в браузере
- `jarvis.notify(title, text)` — уведомление Windows
- `jarvis.plugins.reload()` — горячая перезагрузка плагинов

---

## 🧠 Память и LLM

- Факты сохраняются в `jarvis_memory.db` (SQLite)
- История диалогов — в той же БД
- Каждые 20 сообщений LLM анализирует память и выделяет важное
- В режиме ИИ (после «давай поболтаем») отвечает локальная модель

---

## 🐳 Docker (опционально)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

> ⚠️ Для работы в Docker нужен проброс аудио (`--device /dev/snd`) и GPU (`--gpus all`).

---

## 📝 Лицензия

MIT — делай что хочешь, но оставь копирайт.

---

## 👤 Автор

**Tynfolz** — [GitHub](https://github.com/Tynfolz)