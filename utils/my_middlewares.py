from typing import Callable, Dict, Any, Awaitable, TypedDict, override, Optional
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject, User, Chat
from math import floor
import time


class Translation(TypedDict):
    seconds_to_str: dict[int | str, str]
    """Dict for converting seconds to string"""
    error_too_fast: str
    """Message which need to be used with `.format(remain_time=..., unit_string=...)`"""


translations: dict[str, Translation] = dict(
    ru=Translation(
        seconds_to_str={
            1: "секунду",
            2: "секунды",
            3: "секунды",
            4: "секунды",
            "default": "секунд",
        },
        error_too_fast="слишком быстро, подожди чут-чут 🤏, вот прям {remain_time:.1f} {unit_string}",
    ),
    en=Translation(
        seconds_to_str={1: "second", "default": "seconds"},
        error_too_fast="Too fast, wait just {remain_time:.1f} {unit_string}",
    ),
)
"""Get translation_table by language code. 

In that table there is two fields: seconds_to_str and error_too_fast.

Usage:

```python
unit_string = seconds_to_str.get(last_digit, seconds_to_str['default'])
too_fast_message = error_too_fast.format(remain_time=remain_time, unit_string=unit_string)
```
"""


class CooldownMiddleware(BaseMiddleware):
    """If from previous update from user didn't pass *cooldown* seconds, then update will not invoked"""

    def __init__(self, cooldown: float = 0.5):
        self.cooldown = cooldown
        self.times: dict[int, float] = dict()

    @override
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        from_user: Optional[User] = getattr(event, "from_user", None)
        sender_chat: Optional[Chat] = getattr(event, "sender_chat", None)
        if from_user is not None:
            uid = from_user.id  # type: ignore[union-attr]
            language_code = from_user.language_code or "en"

        elif sender_chat is not None:
            uid = sender_chat.id
            language_code = "en"

        else:
            return await handler(event, data)

        translation_table = translations.get(language_code, translations["en"])

        cur_time = time.time()
        delta_time = cur_time - self.times.get(uid, 0)

        is_too_fast = delta_time < self.cooldown

        if isinstance(event, CallbackQuery) and is_too_fast:
            fast_msg_template = translation_table["error_too_fast"]
            unit_strings = translation_table["seconds_to_str"]

            remain_time = self.cooldown - delta_time
            remain_last_d = floor(remain_time) % 10

            too_fast_message = fast_msg_template.format(
                remain_time=remain_time,
                unit_string=unit_strings.get(remain_last_d, unit_strings["default"]),
            )
            await event.answer(too_fast_message)
            return

        elif is_too_fast:
            return

        self.times[uid] = cur_time
        return await handler(event, data)
