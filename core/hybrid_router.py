print("HR 1")
from ai.ai_hybrid import ask_ai

print("HR 2")
from voice.tts import speak

print("HR 3")
from ai.memory_db import MemoryDB

print("HR 4")
from voice.voice_async import speak_async

print("HR 5")
from core.skill_engine import SkillEngine

print("HR 6")
from ai.search import web_search

import requests

class HybridRouter:

    def __init__(self):
        print("🔥 INIT START SkillEngine")

        self.db = MemoryDB()
        self.skills = SkillEngine()
        self.listen_mode = "ACTIVE"
        self.ai_mode = False
        self.last_action = None
        self.last_failed_action = None
        self.pending_context = None

        print("🚀 JARVIS FINAL ROUTER READY")

    def process(self, text: str):

        if not text:
            return

        text = text.lower().strip()

        print("ROUTER:", text)

        # -------------------------
        # AI MODE ON
        # -------------------------
        if text in ["режим общения", "поговорим", "включи ии"]:
            self.ai_mode = True

            speak("Режим общения активирован")

            return

        # -------------------------
        # AI MODE OFF
        # -------------------------
        if text in ["режим команд", "выключи ии"]:
            self.ai_mode = False

            speak("Режим команд активирован")

            return

        # -------------------------
        # SLEEP
        # -------------------------
        if text in ["свободен", "спи", "режим ожидания", "оставь"]:
            self.listen_mode = "SLEEP"

            speak_async("Перехожу в режим ожидания")

            return

        # -------------------------
        # IGNORE WHILE SLEEPING
        # -------------------------
        if self.listen_mode == "SLEEP":
            return

        # -------------------------
        # MEMORY
        # -------------------------
        print("1")

        self.db.add_message("user", text)

        print("2")

        self.last_action = text

        print("3")

        # -------------------------
        # INTERNET SEARCH
        # -------------------------
        if any(text.startswith(x) for x in [
            "найди",
            "поищи",
            "посмотри",
            "узнай",
            "проверь",
            "ищи"
        ]):

            search_words = [
                "найди",
                "поищи",
                "посмотри",
                "узнай",
                "проверь",
                "ищи"
            ]

            query = text

            for word in search_words:
                if query.startswith(word):
                    query = query.replace(word, "", 1).strip()
                    break

            print("SEARCH QUERY:", query)

            # -------------------------
            # CURRENCY
            # -------------------------

            currency_map = {

                "доллар": "USD",
                "доллара": "USD",
                "долларов": "USD",

                "евро": "EUR",

                "гривна": "UAH",
                "гривны": "UAH",
                "гривен": "UAH",

                "фунт": "GBP",
                "фунта": "GBP",

                "юань": "CNY",
                "юаня": "CNY",

                "тенге": "KZT",

                "злотый": "PLN",
                "злотых": "PLN",
            }

            if any(word in query for word in currency_map):

                try:

                    base = None

                    for word, code in currency_map.items():

                        if word in query:
                            base = code
                            break

                    print("CURRENCY BASE:", base)

                    data = requests.get(
                        f"https://open.er-api.com/v6/latest/{base}",
                        timeout=10
                    ).json()

                    rate = data["rates"]["RUB"]

                    names = {

                        "USD": "доллар",
                        "EUR": "евро",
                        "UAH": "гривна",
                        "GBP": "фунт",
                        "CNY": "юань",
                        "KZT": "тенге",
                        "PLN": "злотый"
                    }

                    answer = (
                        f"Один {names[base]} стоит "
                        f"{round(rate, 2)} рублей"
                    )

                    print("CURRENCY:", answer)

                    speak(answer)

                    return


                except Exception as e:

                    print("CURRENCY ERROR:", e)

                    speak("Не удалось получить курс валюты")

                    return
                    
            results = web_search(query)

            if not results:
                speak("В поиске нет информации")
                return

            search_context = ""

            for r in results[:3]:
                search_context += f"""
        Заголовок:
        {r['title']}

        Описание:
        {r['body']}
        """

            prompt = f"""
        Ты JARVIS.

        Используя результаты поиска, ответь пользователю.
        
        - только ответ по сути
        - не говори "я нашел информацию"
        - не давай ссылки
        - не объясняй источники
        - если данных нет, скажи "В поиске нет информации"
        - не используй свои знания
        - не меняй числа
        - не добавляй свои расчёты

        Запрос:
        {query}

        Данные:
        {search_context}

        Ответь коротко.
        Не придумывай.
        """

            response = ask_ai(prompt)

            speak(response)

            return

        # -------------------------
        # SKILLS
        # -------------------------

        result = self.skills.process(text)

        print("4")

        if result:
            return


        # -------------------------
        # AI DISABLED
        # -------------------------
        if not self.ai_mode:
            speak("Команда не найдена")

            return

        # -------------------------
        # AI
        # -------------------------
        facts = self.db.get_facts()

        memory_context = "\n".join(
            [f"{k}: {v}" for k, v in facts.items()]
        )

        prompt = f"""
    Ты JARVIS — русский AI ассистент.

    ВАЖНО:
    - отвечай только на русском
    - будь кратким

    ПАМЯТЬ:
    {memory_context}

    Последняя команда:
    {self.last_action}

    Пользователь:
    {text}
    """

        try:

            response = ask_ai(prompt)

        except Exception:

            response = "Ошибка AI"

        print("AI:", response)

        self.db.add_message("jarvis", response)

        speak(response)

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------