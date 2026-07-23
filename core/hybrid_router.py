from ai.ai_hybrid import ask_ai
from voice.tts import speak
from ai.memory_db import MemoryDB
from voice.voice_async import speak_async
from core.skill_engine import SkillEngine
from ai.search import web_search
from core.phrases import MODES, random_phrase
from core.phrases import SEARCH_NOT_FOUND
from core.phrases import COMMAND_NOT_FOUND
from core import config

import requests

class HybridRouter:

    def __init__(self):
        print("🔥 INIT START SkillEngine")
        self.sleep_requested = False
        self.db = MemoryDB()
        self.skills = SkillEngine()
        self.listen_mode = "ACTIVE"
        self.ai_mode = False
        self.last_action = None

        print("🚀 JARVIS FINAL ROUTER READY")

    def process(self, text: str):

        if not text:
            return

        text = text.lower().strip()

        print("ROUTER:", text)

        # -------------------------
        # AI MODE ON
        # -------------------------

        ai_on_phrases = [

            "режим общения",
            "включи ии",
            "включи искусственный интеллект",
            "включи режим ии",
            "активируй ии",
            "активируй искусственный интеллект",
            "давай поговорим",
            "поговорим",
            "пообщаемся",
            "хочу поговорить",
            "общайся со мной",
            "перейди в режим общения",
            "запусти режим общения",
            "джарвис поговорим",
            "джарвис включи ии",
        ]

        if text in ai_on_phrases:
            self.ai_mode = True

            speak(random_phrase(MODES["ai_on"]))

            return

        # -------------------------
        # AI MODE OFF
        # -------------------------

        ai_off_phrases = [

            "режим команд",
            "выключи ии",
            "отключи ии",
            "выключи искусственный интеллект",
            "отключи искусственный интеллект",
            "перейди в режим команд",
            "только команды",
            "режим управления",
            "командный режим",
            "верни режим команд",
            "хватит общения",
            "закончить разговор",
            "прекрати разговор",
            "джарвис только команды",
        ]

        if text in ai_off_phrases:
            self.ai_mode = False

            speak(random_phrase(MODES["ai_off"]))

            return

        # -------------------------
        # SLEEP
        # -------------------------
        if text in ["свободен", "спи", "режим ожидания", "оставь"]:
            self.listen_mode = "SLEEP"

            self.sleep_requested = True

            speak(random_phrase(MODES["sleep"]))

            return True

        # -------------------------
        # PIPER
        # -------------------------

        if text.startswith("смени голос на") or text.startswith("сменить голос на"):

            name = text.replace(
                "смени голос на",
                ""
            ).replace(
                "сменить голос на",
                ""
            ).strip()

            voices = {

                "дмитрий": "dmitri",
                "ирина": "irina",
                "руслан": "ruslan",

            }

            if name in voices:

                config.PIPER_VOICE = voices[name]

                speak("Голос изменён")

            else:

                speak("Такого голоса нет")

            return True


        # -------------------------
        # MEMORY
        # -------------------------
        self.db.add_message("user", text)

        self.last_action = text

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
                speak_async(random_phrase(SEARCH_NOT_FOUND), ),
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

        if result:
            return


        # -------------------------
        # AI DISABLED
        # -------------------------
        if not self.ai_mode:
            speak_async(random_phrase(COMMAND_NOT_FOUND), ),

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