import aiohttp
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiohttp import InvalidUrlClientError

from core import logger
from core.config import CALLBACK_WEBHOOK_SECRET
from schemas.payment import Payment

import hmac
import hashlib
import json

def generation_callback_signature(secret: str, data: dict):
    return hmac.new(
        secret.encode(),
        msg=json.dumps(data).encode(),
        digestmod=hashlib.sha256
    ).hexdigest()


async def send_callback(url: str, payment: Payment):
    timeout = aiohttp.ClientTimeout(total=10)
    signature = generation_callback_signature(CALLBACK_WEBHOOK_SECRET, payment.model_dump())

    headers = {
        "X-Webhook-Signature": signature,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            logger.info(f"Sending callback for invoice_id {payment.invoice_id} to {url} data {payment.model_dump()}")
            async with session.post(url, json=payment.model_dump(), headers=headers) as response:
                response.raise_for_status()
                logger.info(f"Callback for invoice_id {payment.invoice_id} sent successfully to {url}")
        except (aiohttp.ClientResponseError, aiohttp.ClientError, InvalidUrlClientError) as e:
            logger.error(f"Failed to send callback for invoice_id {payment.invoice_id} to {url}: {e}")

