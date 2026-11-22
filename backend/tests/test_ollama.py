import pytest
import httpx

from app.ai.models import ChatMessage
from app.ai.providers.base import AIProviderError
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

@pytest.mark.anyio
async def test_ollama_generate_raises_provider_error():
    def mock_response(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=500,
            json={"error": "Internal server error"},
        )

    transport = httpx.MockTransport(mock_response)

    provider = OllamaProvider(
        base_url="http://localhost:11434",
        model="qwen3.5:9b",
    )

    await provider.client.aclose()

    provider.client = httpx.AsyncClient(
        base_url="http://localhost:11434",
        transport=transport,
    )

    messages = [
        ChatMessage(
            role="user",
            content="Test message",
        )
    ]

    try:
        with pytest.raises(AIProviderError):
            await provider.generate(messages)
    finally:
        await provider.close()