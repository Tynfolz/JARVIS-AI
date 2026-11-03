from core.phrases import SEARCH_NOT_FOUND, random_phrase

PREFIXES = ("найди", "поищи", "посмотри", "узнай", "проверь", "ищи")
EXCLUDE = ("песн", "трек", "плейлист", "обновлен")

RULES = (
    "Ответь на запрос, используя только данные поиска ниже. "
    "Коротко, без ссылок, не упоминай поиск, не выдумывай."
)


def match(text):
    if not text.startswith(PREFIXES) or any(x in text for x in EXCLUDE):
        return 0
    return 85


def run(jarvis, text):
    query = text
    for p in PREFIXES:
        if query.startswith(p):
            query = query[len(p):].strip()
            break

    if not query:
        return False

    print("SEARCH QUERY:", query)
    results = jarvis.ai.search(query)
    if not results:
        jarvis.say(random_phrase(SEARCH_NOT_FOUND))
        return True

    data = "\n\n".join(f"{r['title']}\n{r['body']}" for r in results[:3])
    answer = jarvis.ai.ask(f"Запрос: {query}\n\nДанные:\n{data}", rules=RULES)
    jarvis.say(answer or random_phrase(SEARCH_NOT_FOUND))
    return True