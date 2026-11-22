
from collections.abc import Sequence

import httpx

from app.ai.models import ChatMessage


class OllamaProvider:
    def __init__(
        self,
        base_url: str,
        model: str,
        timeout: int = 120,
    ) -> None:
        self.model = model
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(timeout),
        )

    async def generate(
        self,
        messages: Sequence[ChatMessage],
    ) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
            "stream": False,
        }

        response = await self.client.post(
            "/api/chat",
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    async def close(self) -> None:
        await self.client.aclose()
