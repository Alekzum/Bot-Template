from utils.my_makers import make_bot, make_dispatcher
from utils.my_wraps import wrap_loggers
import asyncio


async def main():
    wrap_loggers()
    bot = make_bot()
    dp = make_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
