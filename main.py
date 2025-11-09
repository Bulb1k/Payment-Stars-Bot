# main.py
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Dispatcher

from bot import bot, dp
from core.config import SERVER_ADDRESS, SERVER_HOST, SERVER_PORT, USE_NGROK, WEBHOOK_PATH
from core.logger import logger
from handlers.payment import router as payment_router
from server.app import app
from utils import get_ngrok_url


async def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(payment_router)


@asynccontextmanager
async def lifespan(app):
    logger.info("Configuring aiogram")
    await setup_handlers(dp)

    if USE_NGROK:
        public = await get_ngrok_url()
        webhook_url = f"{public}{WEBHOOK_PATH}"
    else:
        webhook_url = f"{SERVER_ADDRESS}{WEBHOOK_PATH}"

    logger.info("Webhook URL: %s", webhook_url)
    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query", "pre_checkout_query"]
    )
    logger.info("Configured aiogram")

    yield

    logger.info("Deleting webhook")
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Bot stopped")


app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=False,
        log_level="info",
    )
