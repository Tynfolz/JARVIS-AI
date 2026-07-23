from ai.search import web_search
from ai.ai_hybrid import ask_ai
from voice.tts import speak
from core.phrases import SEARCH_NOT_FOUND


class SearchService:


    def process(self, text):

        search_words = [

            "найди",
            "поищи",
            "посмотри",
            "узнай",
            "проверь",
            "ищи",

        ]


        if not any(
            text.startswith(x)
            for x in search_words
        ):
            return False


        query = text


        for word in search_words:

            if query.startswith(word):

                query = query.replace(
                    word,
                    "",
                    1
                ).strip()

                break


        print("SEARCH QUERY:", query)


        results = web_search(query)


        if not results:

            speak(
                SEARCH_NOT_FOUND
            )

            return True



        context = ""


        for r in results[:3]:

            context += f"""

Заголовок:
{r['title']}

Описание:
{r['body']}

"""


        prompt = f"""

Ты JARVIS.

Ответь пользователю используя только данные поиска.

Правила:

- коротко
- без ссылок
- без упоминания поиска
- не придумывай


Запрос:

{query}


Данные:

{context}

"""


        answer = ask_ai(prompt)


        speak(answer)


        return True

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------