from aiogram import F, Router, types
from aiogram.filters import Command

from core import logger
from schemas.payment import Payment
from services.payment import PaymentService
from utils import send_callback, AdminFilter

router = Router()


@router.message(Command("pay"), AdminFilter())
async def pay(message: types.Message):
    invoice_link = await PaymentService.create_invoice("https://af699b204019.ngrok-free.app/", 1)

    await message.answer(invoice_link, parse_mode="HTML")


@router.message(Command("refound"), AdminFilter())
async def pay(message: types.Message):
    charge_id = message.text.split(" ")[-1]

    result = await PaymentService.refound(message.chat.id, charge_id)

    await message.answer("Refound success" if result else "Refound failed")


@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: types.PreCheckoutQuery):
    is_exists = await PaymentService.repo.exists(pre_checkout_query.invoice_payload)

    if not is_exists:
        logger.error(f"Invoice not found: {pre_checkout_query.invoice_payload}")
        return await pre_checkout_query.answer(ok=False,
                                               error_message="The payment time has expired, create a new invoice")

    logger.debug(f"Pre_checkout_query: {pre_checkout_query}")
    return await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    payment_id = message.successful_payment.invoice_payload

    invoice_callback_url = await PaymentService.repo.get(payment_id)
    await PaymentService.repo.delete(payment_id)

    await send_callback(
        url=invoice_callback_url,
        payment=Payment(
            id=payment_id,
            status="success",
            amount=message.successful_payment.total_amount,
            charge_id=message.successful_payment.telegram_payment_charge_id,
        )
    )
