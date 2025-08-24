# Назначение: роутер с командами, доступными только владельцам (админам).
# Команды: /start, /help, /id
# Ответы отправляются в тред лички канала (direct messages).

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

# Кастомный фильтр, который пропускает только сообщения от владельцев
from paidposts.bot.srcs.utils.owner_validator import OwnerValidator

# Константы и тексты из настроек:
#  - OWNER_IDS        — список id владельцев (админов), которым доступен этот роутер
#  - START_MESSAGE    — текст ответа на /start
#  - HELP_MESSAGE     — текст ответа на /help
from paidposts.bot.settings import OWNER_IDS, START_MESSAGE, HELP_MESSAGE

# Утилита получения id треда лички канала,
# чтобы ответ пришёл именно в нужный топик в Direct Messages канала.
from paidposts.bot.srcs.utils.topic_id import topic


# Создаём отдельный роутер для владельца.
# Это удобно, чтобы подключать/отключать логические блоки маршрутизации раздельно.
owner_router: Router = Router()

# На все сообщения этого роутера навешиваем фильтр:
# только пользователи, чей id входит в OWNER_IDS, смогут пройти дальше.
owner_router.message.filter(OwnerValidator(OWNER_IDS))


@owner_router.message(Command("start"))
async def start_cmd(m: Message) -> None:
    """
    Обработчик команды /start для владельца.
    Отправляет START_MESSAGE в тред лички канала (direct messages topic).
    """
    # direct_messages_topic_id=topic(m) — указываем, в какой тред лички канала отвечать.
    # ВАЖНО: команду нужно вызывать в личке канала, чтобы у сообщения был direct_messages_topic.
    await m.answer(START_MESSAGE, direct_messages_topic_id=topic(m))


@owner_router.message(Command("help"))
async def help_cmd(m: Message) -> None:
    """
    Обработчик команды /help для владельца.
    Отправляет HELP_MESSAGE в тред лички канала.
    """
    await m.answer(HELP_MESSAGE, direct_messages_topic_id=topic(m))


@owner_router.message(Command("id"))
async def id_cmd(m: Message) -> None:
    """
    Обработчик команды /id для владельца.
    Возвращает Telegram id отправителя (удобно, чтобы добавлять админов/белый список).
    """
    # m.from_user.id — числовой tg_id автора сообщения.
    # Переводим в строку для конкатенации в f-string (хотя можно и без str()).
    await m.answer(
        f"Твой tg_id: {str(m.from_user.id)}",
        direct_messages_topic_id=topic(m),
    )
