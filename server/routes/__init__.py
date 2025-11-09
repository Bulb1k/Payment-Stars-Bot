from fastapi import APIRouter, Depends

from .payment import router as invoice_router
from .webhook import router as webhook_router
from ..security import verify_api_key

api_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(verify_api_key)]
)


api_router.include_router(prefix="/payment", router=invoice_router)
