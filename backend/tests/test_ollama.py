import pytest

from app.ai.models import ChatMessage
from app.ai.providers.ollama import OllamaProvider


@pytest.mark.anyio
async def test_ollama_generate():
    provider = OllamaProvider(
        base_url="http://localhost:11434",
        model="qwen2.5:7b",
    )

    try:
        messages = [
            ChatMessage(
                role="user",
                content="Explain what a REST API is in two sentences.",
            )
        ]

        response = await provider.generate(messages)

        assert isinstance(response, str)
        assert len(response) > 0

    finally:
        await provider.close()