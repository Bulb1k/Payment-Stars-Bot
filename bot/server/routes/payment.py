from aiogram.exceptions import TelegramBadRequest
from fastapi import APIRouter, Query, HTTPException, status

from schemas import CreateInvoice, InvoiceResponse, BaseResponse, PaymentRefund
from services.payment import PaymentService

router = APIRouter()


@router.post("/invoice", response_model=InvoiceResponse)
async def create_invoice(data: CreateInvoice):
    try:
        invoice_data = await PaymentService.create_invoice(**data.model_dump())
        return InvoiceResponse(**invoice_data)
    except TelegramBadRequest as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.post("/refund", response_model=BaseResponse)
async def refund(data: PaymentRefund):
    try:
        result = await PaymentService.refund(
            chat_id=data.chat_id,
            charge_id=data.payment_id
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refund failed"
            )

        return BaseResponse(
            status="success",
            detail="Refund successful"
        )
    except TelegramBadRequest as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get("/")
async def get_payments(
        offset: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
):
    transactions = await PaymentService.get_all(offset, limit)
    return transactions.model_dump()