from aiogram import Bot, Dispatcher
import asyncio
import logging
import os
from dotenv import load_dotenv
from utils.handlers import router, send_message_to_user


async def main():
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
