export interface ChatRequest {
  logs: string[];
  context?: string | null;
}

export interface ChatResponse {
  analysis: string;
}