import json
from ai.ai_hybrid import ask_ai


class MemorySorter:


    def __init__(self, db):

        self.db = db



    def analyze(self):

        messages = self.db.get_unsorted_messages()


        if not messages:
            return



        text = ""


        ids = []

        for i, role, msg in messages:

            ids.append(i)

            if role != "user":
                continue

            text += f"""
        user:
        {msg}

        """

        prompt = f"""

        Ты модуль долговременной памяти JARVIS.

        Твоя задача:
        найти только важные постоянные факты о пользователе.


        Сохраняй ТОЛЬКО:

        - любимые игры
        - любимую музыку
        - хобби
        - навыки
        - стиль одежды
        - предпочтения
        - имя
        - постоянные настройки


        НЕ сохраняй:

        - обычные ответы
        - вопросы
        - приветствия
        - эмоции
        - планы на сегодня
        - случайные сообщения
        - ответы JARVIS
        - информацию о текущем разговоре


        Примеры хороших фактов:

        "Я люблю Dota 2"

        результат:

        [
        {
        "category":"hobby",
        "key":"favorite_game",
        "value":"Dota 2",
        "importance":9
        }
        ]


        "Мне нравится чёрная одежда"

        результат:

        [
        {
        "category":"style",
        "key":"clothing",
        "value":"чёрная одежда",
        "importance":7
        }
        ]


        Если фактов нет:

        []

        Верни ТОЛЬКО JSON.


        Разговор:

        {text}

        """


        try:

            result = ask_ai(prompt)


            facts = json.loads(result)


            for fact in facts:

                self.db.add_fact(

                    fact["category"],

                    fact["key"],

                    fact["value"],

                    fact["importance"]

                )


            self.db.mark_processed(ids)
            self.db.cleanup_conversations()


            print(
                "🧠 MEMORY UPDATED:",
                facts
            )


        except Exception as e:

            print(
                "MEMORY ERROR:",
                e
            )