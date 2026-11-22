from fastapi import APIRouter, HTTPException, Request

from app.ai.providers.base import AIProviderError
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def analyze_logs(
    payload: ChatRequest,
    request: Request,
) -> ChatResponse:

    analysis_service = request.app.state.analysis_service

    try:
        analysis = await analysis_service.analyze(
            logs=payload.logs,
            context=payload.context,
        )
    except AIProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable.",
        ) from exc

    return ChatResponse(analysis=analysis)