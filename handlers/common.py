from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging


logger = logging.getLogger(__name__)
rt = Router()


@rt.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, command: CommandObject):
    data = await state.get_data()
    if data is None:
        await state.set_data({})
    
    match command.args:
        case None:
            pass
        
        case _:
            logger.info(f"Start is {command}")

    await message.answer(f"Hello! I am an echo bot and just copying your messages to you.")


@rt.message()
async def msg_echo(message: Message):
    await message.copy_to(message.chat.id)
