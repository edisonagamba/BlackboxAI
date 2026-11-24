# Blackbox AI

**Local AI-powered application log analysis for incident investigation.**

Blackbox AI is an engineering tool designed to help developers and Site Reliability Engineers (SREs) investigate application incidents by analyzing application logs with locally running Large Language Models (LLMs).

It processes log data and incident context to identify potential root causes, distinguish observed evidence from hypotheses, and suggest practical next steps for investigation.

Built with React, TypeScript, Python, FastAPI, and Ollama, the project explores the integration of local AI models into a modular, testable software architecture.

> **Project status:** Active development

---

## Overview

Troubleshooting production incidents often requires engineers to inspect large volumes of logs, correlate error messages, and identify possible failure points.

Blackbox AI aims to simplify this investigation process by providing an AI-assisted analysis workflow.

### Current capabilities

- **Log analysis:** Submit application logs and incident context for AI analysis.
- **Root cause investigation:** Identify potential causes supported by the supplied evidence.
- **Evidence-based reasoning:** Distinguish confirmed observations from hypotheses.
- **Investigation recommendations:** Suggest practical steps to investigate potential issues further.
- **Local AI inference:** Run analysis using Ollama without requiring a hosted LLM API.
- **Provider abstraction:** Separate AI integration from business logic to support future provider implementations.
- **API validation and error handling:** Validate requests and handle AI provider failures.
- **Automated tests:** Test analysis logic, API behaviour, and provider error handling.

## Architecture

The application follows a layered architecture that separates presentation, API handling, business logic, and AI provider integration.

<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/676d1f05-0a27-4073-87f1-daafa082b5b2" />

### Architectural responsibilities

| Component | Responsibility |
|---|---|
| React frontend | Collect logs and incident context; display analysis |
| FastAPI | Expose HTTP endpoints and validate requests |
| AnalysisService | Build analysis prompts and coordinate AI requests |
| AIProvider | Define the provider integration contract |
| OllamaProvider | Handle communication with the Ollama API |
| Ollama | Run the local language model |

### Technology stack

**Frontend**
- React
- TypeScript
- Vite

**Backend**
- Python
- FastAPI
- Pydantic
- HTTPX

**AI infrastructure**
- Ollama
- Qwen 3.5:9b

**Testing**
- Pytest
- HTTPX MockTransport


## Getting started

### Prerequisites

- Python 3.12+
- Node.js and npm
- Ollama
- Git

### 1. Clone the repository

```bash
git clone https://github.com/edisonagamba/BlackboxAI.git
cd BlackboxAI
```

### 2. Set up Ollama

Install Ollama from [ollama.com](https://ollama.com/).

Start the Ollama service:

```bash
ollama serve
```

In another terminal, download the model:

```bash
ollama pull qwen3.5:9b
```

Verify the installation:

```bash
ollama list
```

### 3. Configure the backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
APP_NAME='Blackbox AI'
ENVIRONMENT=development

AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:9b
AI_REQUEST_TIMEOUT_SECONDS=120
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: http://localhost:8000
- Interactive API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

### 4. Set up the frontend

Open another terminal from the project root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

http://localhost:5173

## Running the application

The application requires three running services:

| Service | Port | Purpose |
|---|---:|---|
| Ollama | 11434 | Local LLM inference |
| FastAPI | 8000 | Backend API |
| Vite | 5173 | Frontend development server |

Once all services are running, submit application logs and optional incident context through the Blackbox AI interface.

## API reference

### `POST /api/chat`

Submit application logs for analysis.

**Request**

```json
{
  "logs": [
    "INFO Application started",
    "INFO Database connection established",
    "ERROR Database connection timeout",
    "ERROR Request processing failed"
  ],
  "context": "Users are experiencing intermittent application failures."
}
```

**Response**

```json
{
  "analysis": "AI-generated incident analysis..."
}
```

**Error handling**

| HTTP status | Description |
|---|---|
| 200 | Analysis completed |
| 422 | Invalid request payload |
| 503 | AI provider unavailable |

### `GET /api/health`

Returns the backend service health status.

## Testing

Backend tests are located in `backend/tests/`.

Activate the virtual environment and navigate to the backend directory:

```bash
cd backend
source .venv/bin/activate
pytest -v
```

The test suite covers:

- Analysis service behaviour.
- Chat API request validation.
- AI provider failure handling.
- Ollama provider response handling.

## Engineering principles

The project is being developed around the following principles:

- **Separation of concerns:** Keep API, business logic, and infrastructure responsibilities independent.
- **Provider abstraction:** Avoid coupling analysis logic to a specific LLM provider.
- **Testability:** Use isolated tests and mocked external dependencies where appropriate.
- **Local-first AI:** Support inference using locally hosted language models.
- **Evidence-based analysis:** Avoid presenting unsupported assumptions as confirmed facts.
- **Maintainability:** Build a modular foundation that can support additional analysis capabilities.


## Scope and limitations

Blackbox AI is an investigative assistant, not an autonomous incident remediation system.

Its findings depend on the quality and completeness of the supplied logs and context. AI-generated root causes are hypotheses that require engineering verification.

The current implementation is an early-stage application focused on establishing the core analysis workflow and architecture.

---

**Built as an exploration of AI engineering, local LLM integration, and reliable backend architecture.**
