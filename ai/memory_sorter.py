import json
import re

from ai.llm import generate

SORTER_PROMPT = """Ты модуль долговременной памяти. Извлеки из сообщений пользователя
только постоянные факты о нём: имя, любимые игры, музыку, хобби, навыки, стиль, предпочтения, настройки.
НЕ сохраняй вопросы, приветствия, эмоции, планы на сегодня, команды, случайные фразы.

Ответ — ТОЛЬКО JSON-массив, без текста вокруг:
[{"category": "hobby", "key": "favorite_game", "value": "Dota 2", "importance": 9}]
Если фактов нет — верни []"""


class MemorySorter:

    def __init__(self, db):
        self.db = db

    def analyze(self):
        messages = self.db.get_unsorted_messages()
        if not messages:
            return

        ids = [i for i, _, _ in messages]
        user_text = "\n".join(f"- {msg}" for _, role, msg in messages if role == "user")

        try:
            if not user_text.strip():
                return

            raw = generate(
                [
                    {"role": "system", "content": SORTER_PROMPT},
                    {"role": "user", "content": user_text[:3000]},
                ],
                temperature=0.1,
                max_tokens=400,
            )
            found = re.search(r"\[.*\]", raw, re.S)
            facts = json.loads(found.group(0)) if found else []

            for f in facts:
                if isinstance(f, dict) and f.get("key") and f.get("value"):
                    self.db.add_fact(
                        f.get("category", "other"),
                        f["key"],
                        str(f["value"]),
                        int(f.get("importance", 5)),
                    )
            if facts:
                print("🧠 MEMORY UPDATED:", facts)

        except Exception as e:
            print("MEMORY ERROR:", e)

        finally:
            self.db.mark_processed(ids)
            self.db.cleanup_conversations()