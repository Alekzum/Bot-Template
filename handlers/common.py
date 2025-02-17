from aiogram import Bot, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, Chat
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.fsm_states import CommonStates
from utils.my_keyboard import make_row, make_button
from typing import Callable, TypedDict, NotRequired
import logging


class ContextData(TypedDict):
    msg_id: NotRequired[int]


logger = logging.getLogger(__name__)
rt = Router()

state2func: dict[State | StatesGroup, Callable] = dict()


@rt.message(~StateFilter(None), Command("cancel"))
async def cmd_cancel(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    msg_id = data["msg_id"]
    chat_id = data["chat_id"]
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_id)
    await state.clear()


@rt.callback_query(F.data == "__next__")
async def callback_next(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    cur_state = await state.get_state()
    states = [state for state in CommonStates]

    index = [state.state for state in states].index(cur_state)
    if index + 1 >= len(states):
        logger.warning("how?")
        return
    next_state = states[index + 1]

    next_function = state2func[next_state]
    await state.set_state(next_state)
    await next_function(callback, bot, state)


@rt.callback_query(F.data == "__prev__")
async def callback_prev(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    cur_state = await state.get_state()
    states = [state for state in CommonStates]

    index = [state.state for state in states].index(cur_state)
    if index - 1 >= len(states):
        logger.warning("how?")
        return
    prev_state = states[index - 1]

    prev_function = state2func[prev_state]
    await state.set_state(prev_state)
    await prev_function(callback, bot, state)


@rt.message(StateFilter(None), Command("start"))
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    assert message.from_user

    data = await state.get_data()
    if not data:
        data = dict(chat_id=message.from_user.id)
        await state.set_data(data)

    chat_id = data["chat_id"]
    text = "Hello! I am an echo bot and just copying your messages to you."
    keyboard = make_button("Ok and?", "__next__")

    await state.set_state(CommonStates.START)
    if (msg_id := data.get("msg_id")) is None:
        msg = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
        await state.update_data({"msg_id": msg.message_id})
        return

    await bot.edit_message_text(
        chat_id=chat_id, text=text, reply_markup=keyboard, message_id=msg_id
    )


async def echo_info(_: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    msg_id = data["msg_id"]

    keyboard = make_row(("repeat pls", "__prev__"), ("ok", "__next__"))
    await bot.edit_message_text(
        text="Just type something to me and I send same message",
        chat_id=chat_id,
        message_id=msg_id,
        reply_markup=keyboard,
    )
    await state.set_state(CommonStates.ECHO_INFO)


async def echo_wait(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    msg_id = data["msg_id"]

    keyboard = make_button("I changed my mind", "__prev__")
    await bot.edit_message_text(
        text="Now write. I will wait...",
        chat_id=chat_id,
        message_id=msg_id,
        reply_markup=keyboard,
    )
    await state.set_state(CommonStates.ECHO)


state2func.update(
    {
        CommonStates.START: cmd_start,
        CommonStates.ECHO_INFO: echo_info,
        CommonStates.ECHO: echo_wait,
    }
)


@rt.message(StateFilter(CommonStates.ECHO))
async def msg_echo(message: Message):
    await message.copy_to(message.chat.id)
