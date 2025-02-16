from importlib import import_module
from aiogram import Dispatcher
import pathlib


def include_routers(dp: Dispatcher, root="handlers"):
    files = pathlib.Path(root).glob("*.py")
    for file in files:
        module = import_module(".".join((root, file.with_suffix("").name)))
        dp.include_router(module.rt)
