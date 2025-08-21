from aiogram import Router, F, Bot
from aiogram.types import Message

from paidposts.bot.srcs.services.process_paid_posts import process_paid_posts
from paidposts.bot.srcs.utils.topic_id import topic

from typing import Dict, Any

user_router: Router = Router()


@user_router.message(F.chat.is_direct_messages == True, F.suggested_post_info)
async def on_suggested_post(message: Message, bot: Bot) -> None:
    post: Dict[str, Any] = await process_paid_posts(message)

    if post.get("decline"):
        await bot.decline_suggested_post(
            chat_id=message.chat.id,
            message_id=message.message_id,
            comment=post.get("msg"),
        )
        return None

    if not post.get("valid"):
        return None

    if post.get("ans"):
        await bot.approve_suggested_post(
            chat_id=message.chat.id,
            message_id=message.message_id,
        )
        await message.answer(post.get("msg"), direct_messages_topic_id=topic(message))
        return None
    else:
        await message.answer(post.get("msg"), direct_messages_topic_id=topic(message))
        return None
