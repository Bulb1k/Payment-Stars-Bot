import aiohttp
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiohttp import InvalidUrlClientError

from core import logger
from core.config import NGROK_INTERFACE_HOST, NGROK_INTERFACE_PORT, ADMIN_LIST
from schemas.payment import Payment


async def get_ngrok_url() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{NGROK_INTERFACE_HOST}:{NGROK_INTERFACE_PORT}/api/tunnels") as resp:
            data = await resp.json()
    for t in data.get("tunnels", []):
        if t.get("proto") == "https":
            return t["public_url"]
    raise RuntimeError("ngrok HTTPS tunnel not found")