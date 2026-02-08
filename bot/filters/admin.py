import aiohttp
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiohttp import InvalidUrlClientError

from core import logger
from core.config import NGROK_INTERFACE_HOST, NGROK_INTERFACE_PORT, ADMIN_LIST
from schemas.payment import Payment


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in ADMIN_LIST