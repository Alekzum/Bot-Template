from aiogram.fsm.state import State, StatesGroup


class CommonStates(StatesGroup):
    START = State()
    ECHO_INFO = State()
    ECHO = State()