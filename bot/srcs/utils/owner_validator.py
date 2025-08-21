from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import List


class OwnerValidator(BaseFilter):
    def __init__(self, owners: List[int]) -> None:
        self.owners: set[int] = {int(x) for x in owners}

    async def __call__(self, message: Message) -> bool:
        return bool(message.from_user and message.from_user.id in self.owners)
