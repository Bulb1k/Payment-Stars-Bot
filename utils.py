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


async def send_callback(url: str, payment: Payment):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            logger.info(f"Sending callback for invoice_id {payment.invoice_id} to {url} data {payment.model_dump()}")
            async with session.post(url, json=payment.model_dump()) as response:
                response.raise_for_status()
                logger.info(f"Callback for invoice_id {payment.invoice_id} sent successfully to {url}")
        except (aiohttp.ClientResponseError, aiohttp.ClientError, InvalidUrlClientError) as e:
            logger.error(f"Failed to send callback for invoice_id {payment.invoice_id} to {url}: {e}")


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in ADMIN_LIST
