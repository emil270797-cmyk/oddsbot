import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from .handlers import router
from .providers.base import Providers
from .providers.stub import StubMatches, StubOdds, StubMoneyFlow
from .storage import DB


async def main():
    load_dotenv()
    bot = Bot(os.environ["BOT_TOKEN"])
    # Здесь подменяются источники: реальные адаптеры вместо заглушек.
    providers = Providers(matches=StubMatches(), odds=StubOdds(), moneyflow=StubMoneyFlow())
    dp = Dispatcher(providers=providers, db=DB(os.getenv("DB_PATH", "footbot.sqlite3")))
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
