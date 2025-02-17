from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    SwitchInlineQueryChosenChat,
)
from aiogram.utils import keyboard
from typing import Sequence, Literal, Callable


INPUT_KEYS = Literal[
    "url",
    "callback",
    "switch_inline_query",
    "switch_inline_query_current_chat",
    # "switch_inline_query_chosen_chat",
]
INPUT_FIELDS = dict[
    INPUT_KEYS,
    str,
]
INPUT_FIELDS2 = tuple[
    INPUT_KEYS,
    str,
]


def convert_(to_fill: INPUT_KEYS, text: str, fill_value: str) -> InlineKeyboardButton:
    match to_fill:
        case "url":
            return InlineKeyboardButton(text=text, url=fill_value)
        case "callback":
            return InlineKeyboardButton(text=text, callback=fill_value)
        case "switch_inline_query":
            return InlineKeyboardButton(text=text, switch_inline_query=fill_value)
        case "switch_inline_query_current_chat":
            return InlineKeyboardButton(
                text=text, switch_inline_query_current_chat=fill_value
            )
        case "switch_inline_query_chosen_chat":
            return InlineKeyboardButton(
                text=text, switch_inline_query_chosen_chat=fill_value
            )
        case _:
            raise KeyError(f"Except one of {INPUT_KEYS.__args__}, not {to_fill!r}!")


def make_button_url(text: str, url: str) -> InlineKeyboardMarkup:
    """Make a single button with text and callback data"""
    button = InlineKeyboardButton(text=text, url=url)
    result = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return result


def make_button(text: str, data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=data)]]
    )


def make_row(*items: tuple[str, str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data=data)
                for (text, data) in items
            ]
        ]
    )


def make_column(*items: tuple[str, str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=data)]
            for (text, data) in items
        ]
    )


def make_keyboard(*items: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data=data)
                for (text, data) in pair
            ]
            for pair in items
        ]
    )


def convert(text: str, data: INPUT_FIELDS2 | INPUT_FIELDS) -> InlineKeyboardButton:
    if isinstance(data, dict):
        data_ = tuple(data.items())[0]
    else:
        data_ = data
    return convert_(data_[0], text, data_[1])


def make_button_thing(
    text: str, data: INPUT_FIELDS2 | INPUT_FIELDS
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[convert(text, data)]])


def make_row_thing(
    *items: tuple[str, INPUT_FIELDS2 | INPUT_FIELDS]
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[convert(*pair) for pair in items]])


def make_column_thing(
    *items: tuple[str, INPUT_FIELDS2 | INPUT_FIELDS]
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[convert(*pair)] for pair in items])


def make_keyboard_thing(
    *items: list[tuple[str, INPUT_FIELDS2]]
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[convert(*pair) for pair in pairs] for pairs in items]
    )
