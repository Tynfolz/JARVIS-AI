from ddgs import DDGS


def web_search(query: str, max_results=5):
    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "body": r.get("body", ""),
                    "url": r.get("href", "")
                })

    except Exception as e:
        print("SEARCH ERROR:", e)

    return results