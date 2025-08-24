# Назначение: утилита для извлечения id треда в личке канала (direct messages).
# Используется в owner_router и user_router, чтобы бот отвечал в нужный топик.

from aiogram.types import Message


def topic(m: Message) -> int:
    """
    Возвращает идентификатор треда (topic_id) из лички канала.
    Это нужно для параметра direct_messages_topic_id в методах answer().
    Без него ответ может не попасть в правильный тред.
    
    Пример:
        await m.answer("Привет!", direct_messages_topic_id=topic(m))
    """
    return m.direct_messages_topic.topic_id
