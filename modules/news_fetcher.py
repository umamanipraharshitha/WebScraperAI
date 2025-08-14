import requests

# Free news via Hacker News Algolia (no API key)
def get_latest_news(query="AI", hits=5):
    url = "https://hn.algolia.com/api/v1/search"
    params = {"query": query, "tags": "story", "hitsPerPage": hits}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        items = r.json().get("hits", [])
        return [{"title": it.get("title"), "url": it.get("url") or f"https://news.ycombinator.com/item?id={it.get('objectID')}"} for it in items]
    except Exception:
        return []
