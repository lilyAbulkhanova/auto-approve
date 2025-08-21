from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from paidposts.bot.srcs.utils.owner_validator import OwnerValidator
from paidposts.bot.settings import OWNER_IDS, START_MESSAGE, HELP_MESSAGE
from paidposts.bot.srcs.utils.topic_id import topic

owner_router: Router = Router()
owner_router.message.filter(OwnerValidator(OWNER_IDS))


@owner_router.message(Command("start"))
async def start_cmd(m: Message) -> None:
    await m.answer(START_MESSAGE, direct_messages_topic_id=topic(m))


@owner_router.message(Command("help"))
async def help_cmd(m: Message) -> None:
    await m.answer(HELP_MESSAGE, direct_messages_topic_id=topic(m))


@owner_router.message(Command("id"))
async def id_cmd(m: Message) -> None:
    await m.answer(f"Твой tg_id: {str(m.from_user.id)}", direct_messages_topic_id=topic(m))
