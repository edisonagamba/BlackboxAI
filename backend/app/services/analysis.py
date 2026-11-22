from collections.abc import Sequence

from app.ai.models import ChatMessage
from app.ai.providers.base import AIProvider


class AnalysisService:
    system_prompt = """
    You are an experienced Site Reliability Engineer (SRE) specializing
    in application troubleshooting and log analysis.

    Your task is to analyze application logs and identify potential
    root causes of incidents.

    Rules:
    - Base your analysis strictly on the provided logs and context.
    - Never invent events, errors, or evidence.
    - Distinguish confirmed facts from hypotheses.
    - If the evidence is insufficient, explicitly say so.
    - Provide practical recommendations to investigate the issue further.
    """

    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    async def analyze(
        self,
        logs: Sequence[str],
        context: str | None = None,
    ) -> str:

        formatted_logs = "\n".join(logs)

        user_message = f"""
        Analyze the following application logs.

        Context:
        {context or "No additional context provided."}

        Logs:
        {formatted_logs}
        """

        messages = [
            ChatMessage(
                role="system",
                content=self.system_prompt,
            ),
            ChatMessage(
                role="user",
                content=user_message,
            ),
        ]

        return await self.provider.generate(messages)