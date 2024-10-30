import requests
from config import BING_API_KEY

async def search_bing(query: str) -> str:
    headers = {
        'Ocp-Apim-Subscription-Key': BING_API_KEY
    }
    params = {
        'q': query,
        'textDecorations': True,
        'textFormat': 'HTML',
        'count': 3
    }
    try:
        response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json().get('webPages', {}).get('value', [])

        result = ""
        for item in search_results:
            result += f"Title: {item['name']}\nURL: {item['url']}\nSnippet: {item['snippet']}\n\n"
        return result or "Нет доступной информации по вашему запросу."
    except Exception as e:
        return f"Ошибка при выполнении интернет-запроса: {e}"
