from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Next, Back, Row
from aiogram_dialog.widgets.input import MessageInput

from aiogram_dialog.api.exceptions import NoContextError
from utils.fsm_states import CommonStates
import logging
import json


logger = logging.getLogger(__name__)
rt = Router()


async def echo_actions(msg: Message, _, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.EDIT
    await msg.copy_to(msg.chat.id)


common_dialog = Dialog(
    Window(
        Const("Hello! I am an echo bot and just copying your messages to you."),
        Next(Const("Ok and?")),
        state=CommonStates.START,
    ),
    Window(
        Const("Just type something to me and I send same message"),
        Row(
            Back(Const("repeat pls")),
            Next(Const("ok")),
        ),
        state=CommonStates.ECHO_INFO,
    ),
    Window(
        Const("Now write. I will wait..."),
        Back(Const("I changed my mind")),
        MessageInput(echo_actions),
        state=CommonStates.ECHO,
    ),
)


@rt.message(StateFilter(None), Command("start"))
async def cmd_start(_: Message, dialog_manager: DialogManager):
    try:
        dialog_manager.current_context()
    except NoContextError:
        await dialog_manager.start(
            CommonStates.START,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.AUTO,
        )


@rt.message(Command("cancel"))
async def cancel_state(_: Message, dialog_manager: DialogManager):
    await dialog_manager.reset_stack()


rt.include_router(common_dialog)
