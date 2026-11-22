from fastapi.testclient import TestClient

from app.main import app


class MockAnalysisService:
    async def analyze(
        self,
        logs: list[str],
        context: str | None = None,
    ) -> str:
        return "Database connection timeout detected."


def test_chat_endpoint():
    with TestClient(app) as client:
        app.state.analysis_service = MockAnalysisService()

        response = client.post(
            "/api/chat",
            json={
                "logs": [
                    "ERROR Database connection timeout",
                    "ERROR Failed to execute query",
                ],
                "context": "Production environment",
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "analysis": "Database connection timeout detected."
    }

def test_chat_endpoint_rejects_empty_logs():
    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={
                "logs": [],
                "context": "Production environment",
            },
        )

    assert response.status_code == 422

from app.ai.providers.base import AIProviderError


class FailingAnalysisService:
    async def analyze(
        self,
        logs: list[str],
        context: str | None = None,
    ) -> str:
        raise AIProviderError("Ollama is unavailable.")

def test_chat_endpoint_returns_503_when_ai_provider_fails():
    with TestClient(app) as client:
        app.state.analysis_service = FailingAnalysisService()

        response = client.post(
            "/api/chat",
            json={
                "logs": ["ERROR Database connection timeout"],
                "context": "Production environment",
            },
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "AI service is temporarily unavailable."
    }