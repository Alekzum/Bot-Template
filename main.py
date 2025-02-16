from utils.config import get_token
from utils.my_routers import include_routers
from utils.my_middlewares import CooldownMiddleware
from utils.my_aiosqlitestore import AioSQLStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs
import asyncio
import pathlib


def make_bot():
    return Bot(token=get_token(), default=DefaultBotProperties(parse_mode="html"))


def make_dispatcher():
    dp = Dispatcher(storage=AioSQLStorage(str(pathlib.Path("data", "fsm_storage.db"))))

    dp.message.middleware(CooldownMiddleware(1))
    dp.callback_query.middleware(CooldownMiddleware(1))
    include_routers(dp)
    setup_dialogs(dp)

    return dp


async def main():
    bot = make_bot()
    dp = make_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
