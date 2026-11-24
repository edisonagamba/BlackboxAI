import type { ChatRequest, ChatResponse } from "../types/chat";

const API_URL = "http://localhost:8000/api";

export async function analyzeLogs(
  payload: ChatRequest,
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(
      error.detail || "Failed to analyze logs.",
    );
  }

  return response.json();
}