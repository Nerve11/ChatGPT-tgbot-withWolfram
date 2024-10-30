import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def get_chatgpt_response(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты ассистент, помогающий пользователям решать их задачи."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка при работе с ChatGPT: {e}"
