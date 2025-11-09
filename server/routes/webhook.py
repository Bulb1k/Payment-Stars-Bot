import traceback

from aiogram.types import Update
from fastapi import APIRouter, Request

from bot import bot, dp

router = APIRouter()


@router.post("")
async def bot_webhook(request: Request):
    update = Update(**(await request.json()))
    try:
        await dp.feed_update(bot, update)
    except Exception:
        traceback.print_exc()
    return {"status": "ok"}
