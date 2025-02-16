from utils.config import get_token
from utils.my_routers import include_routers
from utils.my_middlewares import CooldownMiddleware
from utils.my_aiosqlitestore import AioSQLStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import asyncio
import pathlib


async def main():
    bot = Bot(token=get_token(), default=DefaultBotProperties(parse_mode="html"))
    dp = Dispatcher(storage=AioSQLStorage(str(pathlib.Path("data", "fsm_storage.db"))))

    dp.message.middleware(CooldownMiddleware(1))
    dp.callback_query.middleware(CooldownMiddleware(1))
    include_routers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
