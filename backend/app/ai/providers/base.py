
from collections.abc import AsyncIterator, Sequence
from typing import Protocol

from app.ai.models import ChatMessage


class AIProvider(Protocol):

    async def generate(
        self,
        messages: Sequence[ChatMessage],
    ) -> str:
        pass

    async def stream(
        self,
        messages: Sequence[ChatMessage],
    ) -> AsyncIterator[str]:
        pass

class AIProviderError(Exception):
    """Raised when an AI provider request fails."""