
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.providers.ollama import OllamaProvider
from app.api.health import router as health_router
from app.core.config import get_settings
from app.services.analysis import AnalysisService
from app.api.chat import router as chat_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    provider = OllamaProvider(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL,
        timeout=settings.AI_REQUEST_TIMEOUT_SECONDS,
    )

    app.state.analysis_service = AnalysisService(provider)

    try:
        yield
    finally:
        await provider.close()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(
    health_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    chat_router,
    prefix=settings.API_PREFIX,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)