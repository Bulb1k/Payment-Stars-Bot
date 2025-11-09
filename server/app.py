from fastapi import FastAPI

from core.config import WEBHOOK_PATH
from server.routes import api_router, webhook_router

app = FastAPI(
    title="Api Bot",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)

app.include_router(api_router, prefix='/api', tags=["API"])
app.include_router(webhook_router, prefix=WEBHOOK_PATH)
