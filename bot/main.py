import asyncio
from aiogram import Bot, Dispatcher
from paidposts.bot.settings import BOT_TOKEN
from paidposts.bot.srcs.routers.owner_router import owner_router
from paidposts.bot.srcs.routers.user_router import user_router

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_router(owner_router)
dp.include_router(user_router)


async def main():
    await dp.start_polling(bot, allowed_updates=["message"])


if __name__ == "__main__":
    asyncio.run(main())
