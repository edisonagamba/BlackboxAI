from collections.abc import Sequence

import pytest

from app.ai.models import ChatMessage
from app.services.analysis import AnalysisService


class MockAIProvider:
    def __init__(self) -> None:
        self.messages: Sequence[ChatMessage] = []

    async def generate(
        self,
        messages: Sequence[ChatMessage],
    ) -> str:
        self.messages = messages

        return "Database connection timeout detected."


provider = MockAIProvider()
service = AnalysisService(provider)


@pytest.mark.anyio
async def test_analysis_returns_provider_response():
    logs = [
        "2026-11-21 10:00:01 ERROR Database connection timeout",
        "2026-11-21 10:00:05 ERROR Failed to execute query",
    ]

    context = "Production database server."

    result = await service.analyze(
        logs=logs,
        context=context,
    )

    assert result == "Database connection timeout detected."

    assert len(provider.messages) == 2

    system_message = provider.messages[0]
    user_message = provider.messages[1]

    assert system_message.role == "system"
    assert "Site Reliability Engineer" in system_message.content

    assert user_message.role == "user"
    assert context in user_message.content

    for log in logs:
        assert log in user_message.content