from utils.my_makers import make_bot, make_dispatcher
import asyncio


async def main():
    bot = make_bot()
    dp = make_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
