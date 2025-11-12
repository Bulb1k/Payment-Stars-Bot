from typing import Literal
from pydantic import BaseModel

class CreateInvoice(BaseModel):
    amount: int
    order_id: str | None = None
    callback_url: str
    title: str = "Goods"
    description: str = "buy goods"


class BaseResponse(BaseModel):
    status: Literal["success", "fail"] = "success"
    detail: str = ""

class InvoiceResponse(BaseResponse):
    invoice_url: str | None = None
    invoice_id: str | None = None


class PaymentRefound(BaseModel):
    payment_id: str
    chat_id: int

class Payment(BaseModel):
    invoice_id: str
    order_id: str | None = None
    payment_id: str
    status: str
    amount: int