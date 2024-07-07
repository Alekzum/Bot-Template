from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging


logger = logging.getLogger(__name__)
rt = Router()


@rt.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, command: list[str]):
    data = await state.get_data()
    if data is None:
        await state.set_data({})
    
    match command:
        case ['start']:
            pass
        
        case _:
            logger.info(f"Args for start are {command}")

    await message.answer(f"Hello!")  