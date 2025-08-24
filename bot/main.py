# Назначение: точка входа для запуска бота.
# Здесь создаются Bot и Dispatcher, подключаются роутеры и запускается polling.

import asyncio
from aiogram import Bot, Dispatcher

# Импорт токена бота (должен быть прописан в settings.py)
from paidposts.bot.settings import BOT_TOKEN

# Импорт роутеров:
#  - owner_router  — команды /start, /help, /id (только для владельцев)
#  - user_router   — обработка предложенных постов из лички канала
from paidposts.bot.srcs.routers.owner_router import owner_router
from paidposts.bot.srcs.routers.user_router import user_router


# Создаём экземпляр бота, указываем токен
bot = Bot(BOT_TOKEN)

# Создаём диспетчер (центральный объект, через который проходят апдейты)
dp = Dispatcher()

# Подключаем роутеры
# Теперь все хендлеры из этих файлов будут работать
dp.include_router(owner_router)
dp.include_router(user_router)


async def main():
    """
    Главная асинхронная функция.
    Запускает polling — бот будет опрашивать Telegram на новые апдейты.
    allowed_updates=["message"] → мы явно говорим, что нас интересуют только апдейты типа "message".
    Это ускоряет работу, так как игнорируются лишние события (callback_query, edited_message и т.д.).
    """
    await dp.start_polling(bot, allowed_updates=["message"])


# Точка входа при запуске файла как скрипта
if __name__ == "__main__":
    # asyncio.run() запускает асинхронную функцию main() в событийном цикле
    asyncio.run(main())
