# Назначение: обработчик предложенных постов, которые приходят в личку канала.
# Логика: принять/отклонить/ответить в зависимости от правил (см. process_paid_posts).

from aiogram import Router, F, Bot
from aiogram.types import Message
from typing import Dict, Any

# Импорт бизнес-логики проверки постов
from paidposts.bot.srcs.services.process_paid_posts import process_paid_posts
# Утилита: достаёт id треда (direct_messages_topic_id), чтобы ответить в тот же тред
from paidposts.bot.srcs.utils.topic_id import topic


# Создаём роутер для пользователей (сюда приходят "предложенные посты")
user_router: Router = Router()


# Хендлер: ловим сообщения только если:
#  1) сообщение пришло из "лички канала" (chat.is_direct_messages == True)
#  2) в сообщении есть suggested_post_info (значит, это реально предложенный пост)
@user_router.message(F.chat.is_direct_messages == True, F.suggested_post_info)
async def on_suggested_post(message: Message, bot: Bot) -> None:
    """
    Основной обработчик предложенных постов.
    Вызывает process_paid_posts(), получает решение и действует:
      - decline (отклонить пост)
      - approve (одобрить пост)
      - либо просто отправить ответ пользователю.
    """

    # Передаём сообщение в сервисную функцию,
    # она возвращает dict с ключами "ans", "msg", "valid", "decline".
    post: Dict[str, Any] = await process_paid_posts(message)

    # 1) Если флаг decline=True → отклоняем пост через API Telegram
    if post.get("decline"):
        await bot.decline_suggested_post(
            chat_id=message.chat.id,       # id чата (это личка канала)
            message_id=message.message_id, # id исходного сообщения
            comment=post.get("msg"),       # комментарий для отклонения
        )
        return None

    # 2) Если сообщение оказалось невалидным (valid=False) → ничего не делаем
    if not post.get("valid"):
        return None

    # 3) Если ans=True → нужно одобрить пост
    if post.get("ans"):
        # Одобряем предложенный пост через API Telegram
        await bot.approve_suggested_post(
            chat_id=message.chat.id,
            message_id=message.message_id,
        )
        # Отправляем сообщение-пояснение в тот же тред лички канала
        await message.answer(
            post.get("msg"),
            direct_messages_topic_id=topic(message),
        )
        return None

    # 4) Иначе (ans=False) → просто отвечаем текстом (без approve/decline)
    else:
        await message.answer(
            post.get("msg"),
            direct_messages_topic_id=topic(message),
        )
        return None
