import wolframalpha
from config import WOLFRAM_APP_ID

client = wolframalpha.Client(WOLFRAM_APP_ID)

async def calculate_with_wolfram(query: str) -> str:
    try:
        res = client.query(query)
        answer = next(res.results).text
        return answer
    except Exception as e:
        return f"Ошибка при выполнении расчета с Wolfram Alpha: {e}"
