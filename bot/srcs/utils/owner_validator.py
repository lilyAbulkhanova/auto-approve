# Назначение: фильтр aiogram для проверки, что сообщение пришло от владельца (админа).
# Используется в owner_router, чтобы только OWNER_IDS могли вызывать команды /start, /help, /id.

from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import List


class OwnerValidator(BaseFilter):
    """
    Кастомный фильтр для aiogram.
    Проверяет: id отправителя входит ли в список владельцев.
    """

    def __init__(self, owners: List[int]) -> None:
        # сохраняем список владельцев в виде множества (set) для быстрого поиска
        self.owners: set[int] = {int(x) for x in owners}

    async def __call__(self, message: Message) -> bool:
        """
        Этот метод вызывается при каждом входящем сообщении.
        Если возвращает True → сообщение проходит дальше в обработчик.
        Если False → обработчик не будет вызван.
        """
        # проверяем, что у сообщения есть автор (from_user)
        # и его id входит в список владельцев
        return bool(
            message.from_user and message.from_user.id in self.owners
        )
