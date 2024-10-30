import asyncio
from aiogram import Bot, Dispatcher, types
from config import TELEGRAM_TOKEN
from gpt_handler import get_chatgpt_response
from wolfram_handler import calculate_with_wolfram
from internet_handler import search_bing
from database import init_db, add_user, update_request_count, get_user_profile
from i18n_handler import translate

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

def get_user_language(message: types.Message) -> str:
    language_code = message.from_user.language_code
    if language_code not in ["ru", "ar", "en"]:
        language_code = "en"
    return language_code

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    language = get_user_language(message)

    add_user(user_id)
    await message.reply(translate("welcome", language))

@dp.message_handler(commands=['profile'])
async def profile_command(message: types.Message):
    user_id = message.from_user.id
    language = get_user_language(message)

    add_user(user_id)
    profile = get_user_profile(user_id)
    if not profile:
        await message.reply(translate("profile_not_found", language))
        return

    response = (
        f"ID: {user_id}\n"
        f"{translate('requests_used', language)}: {profile['requests_today']} / {profile['request_limit']}\n"
        f"{translate('requests_remaining', language)}: {profile['remaining_requests']}"
    )
    await message.reply(response)

@dp.message_handler(commands=['calculate'])
async def calculate_command(message: types.Message):
    user_id = message.from_user.id
    user_query = message.text[len("/calculate "):]
    language = get_user_language(message)

    if not update_request_count(user_id):
        result = await get_chatgpt_response(f"[Облегчённый режим]: {user_query}")
        await message.reply(f"{translate('lite_mode_result', language)}\n{result}")
        return

    plan = await get_chatgpt_response(f"Составь пошаговый план для запроса: {user_query}")
    await message.reply(f"{translate('plan_solution', language)} {plan}")

    result = await calculate_with_wolfram(user_query)
    await message.reply(f"{translate('calculation_result', language)} {result}")

@dp.message_handler(commands=['internet'])
async def internet_command(message: types.Message):
    user_id = message.from_user.id
    user_query = message.text[len("/internet "):]
    language = get_user_language(message)

    result = await search_bing(user_query)
    await message.reply(f"{translate('internet_result', language)}\n{result}")

    update_request_count(user_id)

if __name__ == '__main__':
    init_db()
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
