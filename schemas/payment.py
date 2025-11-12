from typing import Literal

from pydantic import BaseModel


class CreateInvoice(BaseModel):
    amount: int
    callback_url: str
    title: str = "Goods"
    description: str = "buy goods"


class BaseResponse(BaseModel):
    status: Literal["success", "fail"] = "success"
    detail: str = ""


class InvoiceResponse(BaseResponse):
    invoice_url: str | None = None
    payment_id: str | None = None


class PaymentRefound(BaseModel):
    chat_id: int
    charge_id: str


class Payment(BaseModel):
    id: str
    status: str
    amount: int
    charge_id: str | None
