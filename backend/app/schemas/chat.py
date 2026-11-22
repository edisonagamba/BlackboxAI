from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    logs: list[str] = Field(min_length=1)
    context: str | None = None


class ChatResponse(BaseModel):
    analysis: str