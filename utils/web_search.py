from utils.logger import get_logger

logger = get_logger(__name__)


def should_search_web(query):
    try:
        triggers = [
            "latest", "today", "current", "news", "this week", "this month",
            "breaking", "score", "weather", "stock", "price", "update"
        ]
        lowered = query.lower()
        return any(trigger in lowered for trigger in triggers)
    except Exception as exc:
        logger.exception("Failed to run search heuristic")
        raise RuntimeError(f"Failed to run search heuristic: {exc}")


def search_web(query, settings):
    try:
        provider = settings.search_provider
        if provider == "tavily" and settings.tavily_api_key:
            return _search_tavily(query, settings)

        if provider == "serper" and settings.serper_api_key:
            return _search_serper(query, settings)

        return _search_duckduckgo(query, settings)
    except Exception as exc:
        logger.exception("Failed to search the web")
        raise RuntimeError(f"Failed to search the web: {exc}")


def _search_tavily(query, settings):
    try:
        import requests
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": settings.tavily_api_key,
                "query": query,
                "max_results": settings.search_results
            },
            timeout=20
        )
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("content", ""),
                "url": item.get("url", "")
            })
        return results
    except Exception as exc:
        logger.exception("Tavily search failed")
        raise RuntimeError(f"Tavily search failed: {exc}")


def _search_serper(query, settings):
    try:
        import requests
        response = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": settings.serper_api_key},
            json={"q": query},
            timeout=20
        )
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("organic", [])[: settings.search_results]:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "url": item.get("link", "")
            })
        return results
    except Exception as exc:
        logger.exception("Serper search failed")
        raise RuntimeError(f"Serper search failed: {exc}")


def _search_duckduckgo(query, settings):
    try:
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=settings.search_results):
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("body", ""),
                    "url": item.get("href", "")
                })
        return results
    except Exception as exc:
        logger.exception("DuckDuckGo search failed")
        raise RuntimeError(f"DuckDuckGo search failed: {exc}")
