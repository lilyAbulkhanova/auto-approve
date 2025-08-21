from aiogram.types import Message


def topic(m: Message) -> int:
    return m.direct_messages_topic.topic_id
