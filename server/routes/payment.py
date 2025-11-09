from aiogram.exceptions import TelegramBadRequest
from fastapi import APIRouter, HTTPException, Query

from schemas import CreateInvoice, Payment, InvoiceResponse, BaseResponse, PaymentRefound
from services.payment import PaymentService

router = APIRouter()

@router.post("/invoice", response_model=InvoiceResponse)
async def create_invoice(data: CreateInvoice):
    try:
        invoice_link = await PaymentService.create_invoice(**data.model_dump())
    except TelegramBadRequest as error:
        return InvoiceResponse(url=None, status="fail", detail=str(error))

    return InvoiceResponse(url=invoice_link)


@router.post("/refound", response_model=BaseResponse)
async def refound(data: PaymentRefound):
    try:
        result = await PaymentService.refound(**data.model_dump())
    except TelegramBadRequest as error:
        return BaseResponse(status="fail", detail=str(error))

    return BaseResponse(
        status="success" if result else "fail",
        detail="Refund successful" if result else "Refund failed"
    )

@router.get("/")
async def get_payments(
        offset: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
):
    transactions = await PaymentService.get_all(offset, limit)

    return transactions.model_dump()

