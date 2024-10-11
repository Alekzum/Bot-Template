from utils.runtime_platform import check_platform
check_platform()

from utils.config import TOKEN
from utils.my_routers import include_routers
from utils.middleware import CooldownMiddleware
from aiogram_sqlite_storage.sqlitestore import SQLStorage  # type: ignore
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
import asyncio


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="html"))
    dp = Dispatcher(storage=SQLStorage())
    include_routers(dp)

    dp.message.middleware(CooldownMiddleware(1))
    dp.callback_query.middleware(CooldownMiddleware(10))

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        pass

asyncio.run(main())
