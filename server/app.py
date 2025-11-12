from fastapi import FastAPI, Depends

from core.config import WEBHOOK_PATH
from server.routes import api_router, webhook_router
from server.security import verify_api_key

app = FastAPI(
    title="Api Bot",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)

app.include_router(api_router, prefix='/api', dependencies=[Depends(verify_api_key)], tags=["API"])
app.include_router(webhook_router, prefix=WEBHOOK_PATH)
