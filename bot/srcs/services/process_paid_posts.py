from aiogram.types import Message
from typing import Dict, Any, Optional

from paidposts.bot.settings import (
    USER_ID_WHITELIST,
    MODERATION_MESSAGE,
    MIN_PRICE_MESSAGE,
    MIN_POST_PRICE,
    APPROVED_MESSAGE
)


def gen_dict(ans: bool, msg: str, is_valid: bool = True, decline_post: bool = False) -> Dict[str, Any]:
    return {
        "ans": ans,
        "msg": msg,
        "valid": is_valid,
        "decline": decline_post
    }


async def process_paid_posts(message: Message) -> Dict[str, Any]:
    if not (message.chat and getattr(message.chat, 'is_direct_messages', False)):
        return gen_dict(False, "", False)

    if message.from_user.id not in USER_ID_WHITELIST:
        return gen_dict(False, MODERATION_MESSAGE)

    author_id: int = message.from_user.id if message.from_user else None
    if author_id is None:
        return gen_dict(False, "", False)

    price_amount: Optional[int] = None
    price_currency: Optional[str] = None
    if message.suggested_post_info and getattr(message.suggested_post_info, 'price', None):
        p = message.suggested_post_info.price
        price_amount = getattr(p, 'amount', None)
        price_currency = getattr(p, 'currency', None)

    if price_currency == 'XTR' and price_amount is not None:
        if price_amount < MIN_POST_PRICE:
            return gen_dict(False, MIN_PRICE_MESSAGE, True, True)

    return gen_dict(True, APPROVED_MESSAGE)


