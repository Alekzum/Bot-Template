from utils.config import get_token
from utils.my_routers import include_routers
from utils.my_middlewares import CooldownMiddleware
from utils.my_aiosqlitestore import AioSQLStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import pathlib


def make_bot():
    return Bot(token=get_token(), default=DefaultBotProperties(parse_mode="html"))


def make_dispatcher():
    dp = Dispatcher(storage=AioSQLStorage(str(pathlib.Path("data", "fsm_storage.db"))))

    dp.message.middleware(CooldownMiddleware(1))
    dp.callback_query.middleware(CooldownMiddleware(1))
    include_routers(dp)

    return dp
