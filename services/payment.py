import uuid
from datetime import timedelta

from aiogram.types import LabeledPrice

from bot import bot
from services.redis import BaseRepository


class PaymentRepository(BaseRepository):
    PREFIX = "payment"
    TTL = int(timedelta(days=3).total_seconds())


class PaymentService:
    repo = PaymentRepository()

    @classmethod
    async def create_invoice(cls, callback_url: str, amount: int, title: str = "Goods",
                             description: str = "buy goods") -> str:
        payment_id = str(uuid.uuid4())

        invoice_link = await bot.create_invoice_link(
            title=title,
            description=description,
            payload=payment_id,
            currency="XTR",
            prices=[LabeledPrice(label="Price", amount=amount)]
        )

        await cls.repo.set(payment_id, callback_url)

        return invoice_link

    @classmethod
    async def refound(cls, chat_id: int, charge_id: str) -> str:
        return await bot.refund_star_payment(chat_id, charge_id)

    @classmethod
    async def get_all(cls, offset: int | None = None, limit: int | None = None):
        return await bot.get_star_transactions(offset, limit)
