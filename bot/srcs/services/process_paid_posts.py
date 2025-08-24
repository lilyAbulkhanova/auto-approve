# Назначение: бизнес-логика проверки предложенного поста.
# Проверяем:
#  - сообщение из лички канала?
#  - автор в whitelist?
#  - цена поста >= минимальной?
# Возвращаем решение в виде dict.

from aiogram.types import Message
from typing import Dict, Any, Optional

# Импорт настроек и текстов из settings.py
from paidposts.bot.settings import (
    USER_ID_WHITELIST,   # список id пользователей, которым можно авто-одобрять посты
    MODERATION_MESSAGE,  # текст "пост проходит модерацию"
    MIN_PRICE_MESSAGE,   # текст "слишком дёшево"
    MIN_POST_PRICE,      # минимальная цена поста (в XTR)
    APPROVED_MESSAGE     # текст "пост одобрен"
)


def gen_dict(ans: bool, msg: str, is_valid: bool = True, decline_post: bool = False) -> Dict[str, Any]:
    """
    Вспомогательная функция: формируем словарь-результат.
    ans       — True = approve, False = decline/ничего
    msg       — текст сообщения пользователю
    is_valid  — валидно ли сообщение (если False, обработка останавливается)
    decline_post — нужно ли явно вызвать decline_suggested_post
    """
    return {
        "ans": ans,
        "msg": msg,
        "valid": is_valid,
        "decline": decline_post
    }


async def process_paid_posts(message: Message) -> Dict[str, Any]:
    """
    Основная бизнес-логика:
    - Проверяет источник и автора
    - Проверяет цену поста
    - Возвращает dict с решением для user_router
    """

    # 1) Проверка: сообщение должно быть в "личке канала"
    # (у таких чатов chat.is_direct_messages == True)
    if not (message.chat and getattr(message.chat, 'is_direct_messages', False)):
        # если нет — сообщение невалидное, возвращаем пустой ответ
        return gen_dict(False, "", False)

    # 2) Проверка: автор должен быть в whitelist
    if message.from_user.id not in USER_ID_WHITELIST:
        # если автора нет в белом списке → пост "на модерацию"
        return gen_dict(False, MODERATION_MESSAGE)

    # 3) Проверка: автор вообще существует
    author_id: int = message.from_user.id if message.from_user else None
    if author_id is None:
        # если по какой-то причине нет from_user → невалидно
        return gen_dict(False, "", False)

    # 4) Проверка цены поста (если в suggested_post_info есть price)
    price_amount: Optional[int] = None
    price_currency: Optional[str] = None
    if message.suggested_post_info and getattr(message.suggested_post_info, 'price', None):
        # достаём объект цены
        p = message.suggested_post_info.price
        # amount = числовое значение
        price_amount = getattr(p, 'amount', None)
        # currency = строка с кодом валюты (например, 'XTR')
        price_currency = getattr(p, 'currency', None)

    # 5) Проверка: если валюта XTR и сумма меньше минимальной → отклоняем пост
    if price_currency == 'XTR' and price_amount is not None:
        if price_amount < MIN_POST_PRICE:
            return gen_dict(
                False,             # ans = False → не approve
                MIN_PRICE_MESSAGE, # текст "минимальная цена..."
                True,              # valid = True (мы знаем, что это валидный пост, просто не прошёл по цене)
                True               # decline_post = True → нужно вызвать decline
            )

    # 6) Если все проверки пройдены → авто-одобряем пост
    return gen_dict(
        True,               # ans = True → approve
        APPROVED_MESSAGE    # сообщение "пост одобрен"
    )
