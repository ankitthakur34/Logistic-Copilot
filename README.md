# 🚢 Logistics Copilot

> An agentic AI logistics assistant that combines structured SQL analytics, document-grounded RAG, and shipment-delay prediction through LangGraph orchestration.

Logistics Copilot is a full-stack prototype for asking natural-language questions about shipments, containers, vessels, ports, users, tasks, SOPs, incidents, emails, manuals, PDFs, weather information, and shipment-delay risk. A routing LLM decides which specialized tool(s) are required, the selected tools execute independently, and a merger produces one final response for the user.

---

## Table of Contents

- [Prerequisites](#prerequisites)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [External services](#external-services)
- [Installation](#installation)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Create the Python environment](#2-create-the-python-environment)
  - [3. Install backend dependencies](#3-install-backend-dependencies)
  - [4. Configure environment variables](#4-configure-environment-variables)
  - [5. Install frontend dependencies](#5-install-frontend-dependencies)
  - [6. Start PostgreSQL](#6-start-postgresql)
  - [7. Apply the database migration](#7-apply-the-database-migration)
  - [8. Seed sample database data](#8-seed-sample-database-data)
  - [9. Start the backend](#9-start-the-backend)
  - [10. Start the frontend](#10-start-the-frontend)
- [Environment Variables](#environment-variables)
- [Database](#database)
- [Migrations and Seed Data](#migrations-and-seed-data)
- [Running the Project](#running-the-project)
- [Core Tools](#core-tools)
  - [SQL Tool](#sql-tool)
  - [RAG Tool](#rag-tool)
  - [ML Tool](#ml-tool)
- [RAG Pipeline](#rag-pipeline)
- [ML Prediction Pipeline](#ml-prediction-pipeline)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [API Documentation](#api-documentation)
- [RAG Evaluation](#rag-evaluation)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Security](#security)
- [Error Handling and Logging](#error-handling-and-logging)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [Performance and Scalability](#performance-and-scalability)
- [Development Guidelines](#development-guidelines)
- [Contributing](#contributing)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [License](#license)
- [Authors / Maintainers](#authors--maintainers)
- [Acknowledgements](#acknowledgements)
- [Documentation Quality Check](#documentation-quality-check)

---

# Prerequisites

## Backend

Install:

- Python
- PostgreSQL
- `pip`
- A Groq API key

The repository does not pin a Python runtime version in a `pyproject.toml` or runtime-version file, so use a Python version compatible with the listed dependencies.

## Frontend

Install:

- Node.js
- npm

The frontend package specifies:

```text
Next.js 16.2.12
React 19.2.4
```

## External services

The application requires a PostgreSQL database and a Groq API key for the LLM-backed components.

The repository does not contain Docker configuration, so Docker is not required by the current codebase.

---

---

# Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd Logistic-Copilot-main
```

Replace `<your-repository-url>` with the actual Git repository URL if/when one is published.

## 2. Create the Python environment

From the repository root:

```bash
cd backend
python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

## 3. Install backend dependencies

```bash
pip install -r ../requirements.txt
```

The dependency file is stored at the repository root as `requirements.txt`.

## 4. Configure environment variables

Create:

```text
backend/.env
```

with at least:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
GROQ_API_KEY=<your-groq-api-key>
```

Do not commit this file.

## 5. Install frontend dependencies

Open a second terminal:

```bash
cd frontend
npm install
```

## 6. Start PostgreSQL

Make sure the PostgreSQL database referenced by `DATABASE_URL` is reachable.

The current application uses PostgreSQL through SQLAlchemy/psycopg2.

## 7. Apply the database migration

The project contains Flask-Migrate/Alembic configuration. From `backend/`:

```bash
flask --app app.py db upgrade
```

If your Flask CLI configuration differs, the migration files are located under `backend/migrations/` and the application factory is `create_app()` in `backend/app/__init__.py`.

## 8. Seed sample database data

The repository contains a seed runner:

```bash
python scripts/tests/seed_database.py
```

It seeds:

- users
- ports
- vessels
- shipments
- containers
- tasks

The seed functions are idempotent at the table level: they skip seeding when the corresponding table already contains records.

## 9. Start the backend

From `backend/`:

```bash
python app.py
```

The Flask development server is started with `debug=True`.

## 10. Start the frontend

From `frontend/`:

```bash
npm run dev
```

The Next.js development server normally runs on:

```text
http://localhost:3000
```

The frontend currently calls the backend at:

```text
http://localhost:5000/chat
```

This URL is hard-coded in `frontend/lib/api.ts` in the current codebase.

---

---

# Environment Variables

The application currently reads these environment variables from code:

| Variable | Required | Description | Example |
|---|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection URL used by Flask-SQLAlchemy | `postgresql://user:password@host:5432/postgres` |
| `GROQ_API_KEY` | Yes | API key used by the Groq LLM client | `<redacted>` |

### Notes

`backend/app/config.py` loads `.env` using `python-dotenv`.

`backend/app/rag/llm/groq_llm.py` reads `GROQ_API_KEY` directly from the environment.

Do not put real secrets into this README, source code, screenshots, Git history, or issue reports.

The frontend currently has no application environment variable for the backend URL; `frontend/lib/api.ts` contains the local URL directly.

---

---

# Database

## Technology

PostgreSQL accessed through:

- Flask-SQLAlchemy
- SQLAlchemy
- psycopg2-binary
- Flask-Migrate/Alembic

## Schema

The initial migration creates these tables:

```mermaid
erDiagram
    VESSELS ||--o{ SHIPMENTS : carries
    PORTS ||--o{ SHIPMENTS : origin
    PORTS ||--o{ SHIPMENTS : destination
    SHIPMENTS ||--o{ CONTAINERS : contains
    SHIPMENTS ||--o{ TASKS : has
    USERS ||--o{ TASKS : owns

    VESSELS {
        int id PK
        string imo UK
        string name
        string status
    }

    PORTS {
        int id PK
        string code UK
        string name
        string country
    }

    SHIPMENTS {
        int id PK
        string shipment_no UK
        string customer
        string status
        date eta
        int vessel_id FK
        int origin_port_id FK
        int destination_port_id FK
    }

    CONTAINERS {
        int id PK
        string container_no UK
        string size
        string type
        string status
        int shipment_id FK
    }

    USERS {
        int id PK
        string name
        string email UK
        string role
    }

    TASKS {
        int id PK
        string title
        string priority
        string status
        date due_date
        int shipment_id FK
        int owner_id FK
    }
```

## Tables

### `shipments`

Stores shipment-level operational facts including shipment number, customer, status, ETA, vessel, origin port, and destination port.

### `containers`

Stores containers assigned to shipments.

### `vessels`

Stores vessel identity and status.

### `ports`

Stores port codes, names, and countries.

### `users`

Stores users who own operational tasks.

### `tasks`

Stores shipment-related operational tasks, priority, status, due date, and owner.

---

---

# Migrations and Seed Data

Migration configuration:

```text
backend/migrations/alembic.ini
backend/migrations/env.py
backend/migrations/versions/637622811a4a_initial_schema1.py
```

### Upgrade

From `backend/`:

```bash
flask --app app.py db upgrade
```

### Generate a migration

When model changes are made:

```bash
flask --app app.py db migrate -m "describe change"
```

Then apply it:

```bash
flask --app app.py db upgrade
```

### Seed sample data

```bash
python scripts/tests/seed_database.py
```

### Important startup behavior

`backend/app.py` also calls:

```python
db.create_all()
```

inside the Flask application context before starting the development server. For schema evolution, prefer the project's migration mechanism rather than relying on `create_all()`.

---

---

# Running the Project

## Development

### Terminal 1 — backend

```bash
cd backend
venv\Scripts\activate
python app.py
```

### Terminal 2 — frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

The frontend sends chat requests to:

```text
http://localhost:5000/chat
```

## Production

The repository does not currently contain a production process manager, Dockerfile, Docker Compose file, Kubernetes manifests, or backend deployment configuration. Therefore this README does not claim a specific production deployment platform.

The frontend does expose the standard Next.js production commands:

```bash
npm run build
npm run start
```

A production backend deployment should use a production WSGI server rather than the `debug=True` Flask development server. The repository currently does not specify one.

---

---

# Core Tools

## SQL Tool

The SQL agent is composed of:

```text
Question
   ↓
SchemaBuilder
   ↓
SQLGenerator
   ↓
SQLNormalizer
   ↓
SQLValidator
   ↓
SQLExecutor
   ↓
PostgreSQL
   ↓
SQLAnswerGenerator
   ↓
Answer
```

The SQL tool is intended for structured information such as:

- shipments
- containers
- vessels
- ports
- users
- tasks
- counts and aggregations
- reports

### SQL safety

The `SQLValidator` only accepts statements beginning with `SELECT` and rejects destructive keywords including:

- `DELETE`
- `UPDATE`
- `INSERT`
- `DROP`
- `ALTER`
- `TRUNCATE`
- `CREATE`
- `GRANT`
- `REVOKE`

This is a code-level read-only guard, not a replacement for database permissions.

---

## RAG Tool

The RAG tool handles unstructured information.

Supported document types include:

- Markdown
- PDF
- CSV
- JSON

The application loads data from:

```text
backend/data/rag/
backend/data/pdf/
backend/data/csv/
backend/data/json/
```

The configured RAG loader is assembled in `backend/app/bootstrap/rag.py`.

---

## ML Tool

The ML tool predicts shipment delay risk.

The model is loaded from:

```text
backend/app/ml/models/shipment_delay_model.pkl
```

Supporting files include:

```text
backend/app/ml/models/label_encoders.pkl
backend/app/ml/models/feature_columns.pkl
backend/app/ml/models/metadata.json
```

The prediction pipeline obtains operational features from PostgreSQL, transforms categorical fields using persisted encoders, selects the persisted feature columns, and calls the trained model.

Returned prediction information includes:

- prediction
- confidence
- delay probability
- on-time probability
- risk factors

Current risk factors are derived from operational data and include:

- Maintenance vessel
- Reefer container
- Many pending tasks
- Shipment near ETA
- Multiple high-priority tasks

---

---

# RAG Pipeline

The configured RAG architecture is:

```mermaid
flowchart TD
    D[Documents] --> L[MultiLoader]
    L --> PC[Parent/Child Chunker]
    PC --> P[Parent Chunks]
    PC --> C[Child Chunks]

    C --> E[Sentence Transformer Embeddings]
    E --> V[ChromaDB]
    C --> B[BM25 Index]

    Q[User Question] --> DEC[Query Decomposition]
    Q --> MQ[Multi Query Generator]

    MQ --> H[Hybrid Retriever]
    V --> H
    B --> H

    H --> RRF[Reciprocal Rank Fusion]
    DEC --> R[Retrieval Pipeline]
    RRF --> R
    R --> CE[Cross Encoder Reranker]
    CE --> CC[Context Compression]
    CC --> AG[Answer Generator]
    AG --> A[Grounded Answer]
```

### Ingestion components

The application configures:

- `MarkdownLoader("data/rag")`
- `PdfLoader("data/pdf")`
- `CsvLoader("data/csv")`
- `JsonLoader("data/json")`
- `ParentChildChunker()`

### Retrieval components

The retrieval stack includes:

1. Sentence Transformer query embeddings.
2. ChromaDB dense retrieval.
3. BM25 sparse retrieval.
4. Hybrid retrieval.
5. Reciprocal Rank Fusion.
6. LLM-generated query variants.
7. Query decomposition.
8. Metadata extraction/filtering.
9. Cross-encoder reranking.
10. Parent/child context compression.
11. Answer generation.

### Persistent vector store

ChromaDB is configured with:

```text
persist_directory = ./chroma_db
collection_name = cargo_ai
```

The repository currently contains a `backend/chroma_db/` directory with a persisted Chroma SQLite database.

### Important RAG implementation detail

`build_rag()` creates the ingestion result and BM25 index during service construction. The persisted Chroma vector store is read during retrieval. The repository also contains separate embedding/index pipeline components under `backend/app/rag/` and dedicated test scripts for indexing and embedding.

---

---

# ML Prediction Pipeline

```mermaid
flowchart LR
    Q[Shipment Number] --> R[ShipmentRepository]
    R --> F[Operational Features]
    F --> S[MLPredictionService]
    S --> E[Persisted Label Encoders]
    E --> M[Shipment Delay Model]
    M --> P[Prediction + Probabilities]
    F --> RF[Risk Factor Rules]
    P --> OUT[Prediction Response]
    RF --> OUT
```

The repository derives features including:

- shipment status
- origin/destination
- vessel status
- container count
- container type
- pending tasks
- completed tasks
- high-priority tasks
- remaining ETA days
- maintenance-vessel flag
- reefer-container flag
- many-pending-tasks flag

---

---

# Project Structure

```text
Logistic-Copilot-main/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── agents/
│   │   │   ├── router_agent/
│   │   │   └── sql_agent/
│   │   ├── bootstrap/
│   │   │   ├── llm.py
│   │   │   ├── rag.py
│   │   │   ├── sql.py
│   │   │   └── service_registry.py
│   │   ├── database/
│   │   ├── debug/
│   │   ├── langgraph/
│   │   │   ├── graph.py
│   │   │   ├── state.py
│   │   │   ├── edges/
│   │   │   └── nodes/
│   │   ├── ml/
│   │   │   ├── facade/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── routes/
│   │   │   ├── schemas/
│   │   │   └── services/
│   │   ├── models/
│   │   ├── rag/
│   │   │   ├── bm25/
│   │   │   ├── chunking/
│   │   │   ├── context/
│   │   │   ├── context_compression/
│   │   │   ├── decomposition/
│   │   │   ├── embeddings/
│   │   │   ├── evaluation/
│   │   │   ├── generation/
│   │   │   ├── ingestion/
│   │   │   ├── loader/
│   │   │   ├── llm/
│   │   │   ├── metadata/
│   │   │   ├── multi_query/
│   │   │   ├── pipeline/
│   │   │   ├── reranker/
│   │   │   ├── retrieval/
│   │   │   └── vector_store/
│   │   ├── routes/
│   │   └── tools/
│   ├── chroma_db/
│   ├── data/
│   │   ├── csv/
│   │   ├── json/
│   │   ├── pdf/
│   │   ├── postgres/
│   │   └── rag/
│   ├── migrations/
│   │   ├── alembic.ini
│   │   └── versions/
│   └── scripts/
│       ├── seed/
│       ├── test_agents/
│       ├── test_tools/
│       └── tests/
│
├── frontend/
│   ├── app/
│   ├── components/
│   │   ├── chat/
│   │   ├── sidebar/
│   │   └── ui/
│   ├── lib/
│   ├── public/
│   ├── types/
│   ├── package.json
│   ├── next.config.ts
│   ├── tsconfig.json
│   └── eslint.config.mjs
│
├── docs/
│   ├── lanngraph_arch.md
│   └── project_state.md
│
├── requirements.txt
└── .gitignore
```

### Important backend files

| File | Responsibility |
|---|---|
| `backend/app.py` | Creates the Flask app and starts the development server |
| `backend/app/__init__.py` | Flask application factory, extensions, blueprints, ML loading |
| `backend/app/config.py` | Environment-backed Flask/SQLAlchemy configuration |
| `backend/app/bootstrap/service_registry.py` | Application composition root |
| `backend/app/langgraph/graph.py` | LangGraph definition |
| `backend/app/langgraph/state.py` | Shared agent state |
| `backend/app/routes/chat.py` | `/chat` endpoint |
| `backend/app/ml/routes/ml_routes.py` | ML prediction endpoint |
| `backend/app/agents/sql_agent/` | SQL agent implementation |
| `backend/app/rag/` | RAG implementation |
| `backend/app/ml/` | Prediction implementation |
| `backend/app/models/` | SQLAlchemy models |
| `backend/migrations/` | Alembic/Flask-Migrate migrations |
| `backend/scripts/seed/` | Database seed functions |

### Important frontend files

| File | Responsibility |
|---|---|
| `frontend/app/page.tsx` | Main page and local chat-session state |
| `frontend/components/chat/ChatWindow.tsx` | Chat display and backend request handling |
| `frontend/components/chat/ChatInput.tsx` | User question input |
| `frontend/components/chat/ChatMessage.tsx` | Individual message rendering |
| `frontend/components/sidebar/Sidebar.tsx` | Chat session sidebar |
| `frontend/lib/api.ts` | HTTP call to Flask `/chat` |
| `frontend/types/chat.ts` | Frontend chat data types |

---

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16.2.12 |
| UI | React 19.2.4 |
| Styling | Tailwind CSS 4 |
| UI components | shadcn-style components, Base UI, Lucide |
| Markdown | `react-markdown` |
| HTTP client | Browser `fetch` |
| Backend | Flask |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Database driver | psycopg2-binary |
| Database | PostgreSQL |
| Migrations | Alembic / Flask-Migrate |
| Orchestration | LangGraph |
| LLM | Groq API |
| LLM model | `llama-3.3-70b-versatile` by default |
| RAG embeddings | Sentence Transformers |
| Vector store | ChromaDB |
| Sparse retrieval | rank-bm25 |
| Reranking | Cross Encoder / Sentence Transformers stack |
| PDF parsing | PyMuPDF |
| ML model loading | Joblib |
| Data processing | Pandas |
| Validation | Pydantic |
| Evaluation | DeepEval |
| Observability dependency | LangSmith |
| Testing | pytest and project-specific test scripts |
| Frontend linting | ESLint / eslint-config-next |
| Frontend language | TypeScript |
| Backend language | Python |

---

---

# API Documentation

## `POST /chat`

Runs the complete agentic workflow.

### Request

```http
POST /chat
Content-Type: application/json
```

Body:

```json
{
  "question": "What is the revised ETA of SHP0001?"
}
```

### Response

```json
{
  "answer": "...",
  "tool_results": [
    {
      "tool_name": "sql",
      "success": true,
      "sources": []
    }
  ]
}
```

### Behavior

The endpoint:

1. Reads `question` from the JSON body.
2. Invokes `registry.graph.invoke(...)`.
3. Reads `execution_result` from the resulting state.
4. Returns the merged answer.
5. Returns the selected tool results and their sources.

### Authentication

No authentication or authorization middleware is implemented in the current codebase.

---

## `POST /api/ml/predict-delay`

Predicts delay risk for a shipment.

### Request

```http
POST /api/ml/predict-delay
Content-Type: application/json
```

Body:

```json
{
  "shipment_no": "SHP0005"
}
```

### Successful response

The response contains:

```json
{
  "shipment_no": "SHP0005",
  "prediction": "Delayed",
  "confidence": 0.82,
  "delay_probability": 0.82,
  "on_time_probability": 0.18,
  "risk_factors": [
    "Shipment Near ETA"
  ]
}
```

The exact numeric values depend on the current database data and loaded model.

### Shipment not found

```http
404 Not Found
```

Example:

```json
{
  "message": "Shipment not found."
}
```

### Authentication

No authentication or authorization is implemented for this endpoint.

---

---

# RAG Evaluation

RAG evaluation code is under:

```text
backend/app/rag/evaluation/
```

Important components include:

```text
backend/app/rag/evaluation/dataset/
backend/app/rag/evaluation/metrics/
backend/app/rag/evaluation/models/
backend/app/rag/evaluation/runners/
backend/app/rag/evaluation/synthetic/
backend/app/rag/evaluation/reports/
```

The repository contains generated and golden datasets as well as timestamped evaluation reports.

The evaluation flow builds RAG test cases, runs the pipeline, evaluates answer metrics through DeepEval, and compares expected versus retrieved source sets to calculate retrieval precision and recall.

Example report location:

```text
backend/app/rag/evaluation/reports/
```

---

---

# Testing

The project uses `pytest` and also contains many executable test/debug scripts under:

```text
backend/scripts/tests/
backend/scripts/test_agents/
backend/scripts/test_tools/
```

Examples include tests for:

- BM25
- Chroma
- Chroma metadata
- chunking
- context building
- context compression
- CSV loading
- dataset loading
- document grouping
- embeddings
- hybrid retrieval
- metadata extraction
- metadata filtering
- multi-query retrieval
- PDF loading
- query decomposition
- RAG retrieval
- reranking
- synthetic evaluation
- SQL generation/execution
- router parsing
- ML

### Running pytest

From `backend/` or the repository root, use the test command appropriate to the specific script/module. The repository does not define a dedicated `pytest.ini`, `pyproject.toml`, or Makefile test command.

For the standalone scripts, execute the relevant Python file directly, for example:

```bash
python scripts/tests/test_rag.py
```

Only run scripts whose external dependencies and local data are configured.

---

---

# Code Quality

## Frontend

ESLint is configured through:

```text
frontend/eslint.config.mjs
```

Run:

```bash
cd frontend
npm run lint
```

TypeScript is configured through:

```text
frontend/tsconfig.json
```

## Backend

The repository does not contain a dedicated Black, Ruff, Flake8, mypy, or pre-commit configuration. Do not assume one is required.

---

---

# Security

The current codebase includes several useful safety mechanisms, but it is not yet an authenticated production service.

### Implemented protections / controls

- Secrets are intended to be supplied through environment variables.
- Root `.gitignore` ignores `.env`.
- Frontend `.gitignore` ignores `.env*`.
- ML request input is modeled with Pydantic.
- SQL execution is guarded by a read-only SQL validator.
- SQL destructive keywords are rejected by the validator.
- SQL is executed through SQLAlchemy.

### Current security limitations

- No authentication is implemented.
- No authorization/role enforcement is implemented at API level.
- Flask-CORS is enabled without a restricted origin list in the current application factory.
- The Flask development server is configured with `debug=True`.
- The chat endpoint assumes a JSON body containing `question` and does not expose a documented schema validator.
- Secrets must be supplied externally; they are not provisioned by the repository.

For production, these areas should be reviewed before exposing the application publicly.

---

---

# Error Handling and Logging

Tool execution uses `ToolResult`, which provides a common structure:

```python
ToolResult(
    tool_name=...,
    success=...,
    answer=...,
    data=...,
    metadata=...,
    sources=...,
    error=...,
)
```

The SQL, RAG, and ML tools catch execution exceptions and return unsuccessful `ToolResult` objects rather than directly propagating every tool exception to the caller.

The merger uses successful tool results when available and returns a fallback message if no successful tool result exists.

### Debug output

Several components print execution information to stdout, including:

- registered Flask routes
- router decisions
- RAG decomposed questions
- RAG sub-questions
- ML model loading
- seed progress

The repository does not currently define a centralized structured logging configuration for application events.

---

---

# Troubleshooting

## `GROQ_API_KEY` error

If the application fails while initializing the LLM:

1. Confirm `backend/.env` exists.
2. Confirm it contains:

```env
GROQ_API_KEY=<your-key>
```

3. Restart the backend.

The Groq client reads the key directly from the environment.

## Database connection failure

Check:

```env
DATABASE_URL=postgresql://...
```

Then verify that:

- PostgreSQL is running.
- The hostname is reachable.
- The port is correct.
- The credentials are correct.
- The database exists.

## Frontend says `Unable to contact backend.`

Check that Flask is running on the URL currently configured in:

```text
frontend/lib/api.ts
```

The current value is:

```text
http://localhost:5000/chat
```

## Database tables are missing

Run:

```bash
cd backend
flask --app app.py db upgrade
```

Then seed the database:

```bash
python scripts/tests/seed_database.py
```

## ML shipment not found

The prediction endpoint returns 404 if the requested shipment number does not exist in the database.

Verify the shipment first using SQL or the seeded sample data.

## Chroma/RAG issues

The project uses a persistent local Chroma database under:

```text
backend/chroma_db/
```

Also verify that the expected source documents exist under:

```text
backend/data/rag/
backend/data/pdf/
backend/data/csv/
backend/data/json/
```

## Port 5000 already in use

The backend uses Flask's default development port unless changed outside the current code. Stop the process using port 5000 or explicitly change the development server configuration.

## Port 3000 already in use

Next.js will report a port conflict and can be started on another available port using the normal Next.js CLI options.

---

---

# Deployment

## Current repository state

The repository currently provides:

- Flask backend
- Next.js frontend
- PostgreSQL database integration
- local persistent ChromaDB
- persisted ML artifacts
- Alembic/Flask-Migrate configuration

It does **not** include:

- Dockerfile
- docker-compose configuration
- Kubernetes manifests
- GitHub Actions workflow
- Terraform/IaC
- production WSGI configuration
- platform-specific deployment configuration

Therefore no specific cloud platform is documented as an officially supported deployment target by the repository itself.

### Frontend production build

```bash
cd frontend
npm install
npm run build
npm run start
```

### Backend production consideration

Do not use:

```python
app.run(debug=True)
```

as the production server. Deploy Flask behind an appropriate production WSGI server and reverse proxy according to the target platform.

The repository does not prescribe a specific WSGI server, so one should be selected and documented as part of the deployment environment rather than pretending it is already configured.

### PostgreSQL deployment

A managed PostgreSQL provider such as Supabase can be used because the application consumes a standard PostgreSQL connection URL through `DATABASE_URL`. The repository itself does not contain a Supabase-specific integration.

---

---

# Performance and Scalability

The architecture already separates the frontend, API, orchestration, tools, database, vector store, and ML model.

### Existing architectural advantages

- Shared service construction through `ServiceRegistry`.
- LLM client reuse through `get_llm()`.
- Persistent Chroma storage.
- BM25 indexing.
- Dense + sparse hybrid retrieval.
- Cross-encoder reranking.
- Persisted ML artifacts rather than retraining during requests.
- Frontend/backend separation.

### Current scalability limitations

The repository does not currently implement:

- distributed task queues
- background workers
- application-level caching
- Redis
- request rate limiting
- load balancing configuration
- distributed Chroma deployment
- horizontal worker configuration
- conversation persistence in PostgreSQL

These should be treated as future production architecture work rather than existing capabilities.

---

---

# Development Guidelines

The codebase follows a modular separation between:

```text
API
 ↓
Orchestration
 ↓
Tools / Agents
 ↓
Infrastructure
```

### Tool abstraction

Tools implement the common `BaseTool` interface:

```python
class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        ...
```

This allows SQL, RAG, and ML to be exposed to the router using the same conceptual interface.

### Shared result abstraction

Tools return `ToolResult` instead of forcing the graph to understand tool-specific result types.

### Service composition

Shared services are created in `ServiceRegistry` rather than being constructed separately in every request handler.

### Naming / organization

Keep new code close to the existing responsibility boundaries:

- API routes → `routes/`
- LangGraph nodes → `langgraph/nodes/`
- agents → `agents/`
- reusable tools → `tools/`
- model/repository/service code → `ml/`
- retrieval components → `rag/`
- database models → `models/`

---

---

# Contributing

1. Create a branch for your change.
2. Make the smallest focused change possible.
3. Keep responsibilities separated according to the existing architecture.
4. Do not commit `.env` or real credentials.
5. Run relevant backend test scripts.
6. Run frontend linting:

```bash
cd frontend
npm run lint
```

7. Verify the application can start.
8. Verify affected API routes manually or through tests.
9. Update documentation when architecture or commands change.
10. Open a pull request describing the change and its testing status.

The repository does not currently specify a formal commit-message convention or PR template.

---

---

# Known Limitations

The following limitations are visible from the current repository:

- No authentication/authorization layer.
- Flask-CORS is enabled broadly.
- Backend starts in Flask debug mode.
- Frontend backend URL is hard-coded in `frontend/lib/api.ts`.
- No Docker or deployment manifests.
- No CI/CD workflow in the repository.
- No centralized application logging configuration.
- No dedicated production server configuration.
- No persistent frontend chat-history backend; chat sessions are maintained in frontend state.
- The ML prediction endpoint and tool depend on the persisted model artifacts in the repository.
- The RAG system depends on the local Chroma persistence and source-document layout.
- The root requirements file includes several libraries that are not necessarily exercised by every runtime path.

These limitations do not prevent local development, but they should be addressed before treating the application as a public production service.

---

---

# Roadmap

The repository's existing documentation describes a broader roadmap around improving the agentic system. Items explicitly described in project documentation include:

- Better router evaluation
- Memory
- Human-in-the-loop workflows
- MCP integration
- Specialized agents
- Multi-agent collaboration
- Observability
- Production deployment

The RAG documentation also identifies potential future improvements such as:

- Self-query retrieval
- Better metadata extraction
- Parent reranking
- Query caching
- Answer grounding/citations
- Hallucination guardrails
- Incremental indexing
- Multi-modal RAG
- Agentic retrieval
- Long-context memory

These are roadmap ideas, not claims about current implementation.

---

---

# FAQ

## What does the router do?

The router determines which specialized tools should answer a question. It can select SQL, RAG, ML, or multiple tools.

## When should I use SQL?

Use SQL for structured database facts such as shipment status, ETA, ports, vessels, users, tasks, counts, and aggregations.

## When should I use RAG?

Use RAG for information contained in documents such as SOPs, emails, incidents, manuals, PDFs, weather reports, and operational communications.

## When should I use ML?

Use ML for future-looking shipment-delay predictions and probabilities.

## Can one question use multiple tools?

Yes. The router can select multiple tools. Their results are represented using the common `ToolResult` abstraction and passed to the merger.

## Where is the shipment-delay model stored?

```text
backend/app/ml/models/shipment_delay_model.pkl
```

## Where is the vector database stored?

```text
backend/chroma_db/
```

## Where are RAG documents stored?

```text
backend/data/rag/
backend/data/pdf/
backend/data/csv/
backend/data/json/
```

## Does the project have authentication?

No. Authentication and authorization are not implemented in the current repository.

## Is Docker supported?

There is no Dockerfile or Docker Compose configuration in the repository, so Docker is not currently part of the documented setup.

---

---

# License

No license file or explicit license declaration was identified in the repository.

**License: Not specified.**

Add an appropriate `LICENSE` file before distributing the project under an open-source license.

---

---

# Authors / Maintainers

The repository does not contain authoritative package metadata identifying a formal maintainer list.

Project-specific seed data contains sample operational user names, but those records should not be treated as project authors or maintainers.

---

---

# Acknowledgements

The project directly uses and integrates the following open-source libraries/services:

- Flask
- SQLAlchemy / Flask-SQLAlchemy
- Alembic / Flask-Migrate
- LangGraph
- LangChain Core
- Groq
- ChromaDB
- Sentence Transformers
- rank-bm25
- PyMuPDF
- Pandas
- Pydantic
- Joblib
- DeepEval
- LangSmith
- Next.js
- React
- Tailwind CSS
- shadcn-style components
- Lucide React

The project also contains its own RAG, agent, orchestration, SQL, and ML integration layers around these technologies.

---

---

# Documentation Quality Check

This README was prepared by inspecting the uploaded repository structure and source/configuration files.

The following were specifically checked against the repository:

- Project structure
- Root README
- Python dependency file
- Flask application factory
- Flask routes
- LangGraph state and graph
- Router implementation
- SQL tool implementation
- RAG bootstrap and retrieval components
- ML routes, service, model loader, and repository
- SQLAlchemy models
- Alembic migration
- Seed scripts
- Frontend `package.json`
- Frontend API client
- Frontend chat components
- `.gitignore` files
- Existing architecture/project-state documentation

### Documentation decisions

- No real secrets or credentials are included.
- No authentication is claimed because none is implemented.
- No Docker or CI/CD support is claimed because corresponding configuration files are absent.
- No fabricated screenshots are included because the repository contains no application screenshot assets.
- No production cloud platform is presented as officially supported by the codebase.
- Future ideas are clearly separated from implemented functionality.

---

## Project at a Glance

```text
                         ┌───────────────────────┐
                         │       User            │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     Next.js UI        │
                         │  Chat + Sidebar       │
                         └───────────┬───────────┘
                                     │
                              POST /chat
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      Flask API        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Service Registry    │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      LangGraph        │
                         │                       │
                         │ Normalize → Router    │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
             ┌────────────┐   ┌────────────┐   ┌────────────┐
             │ SQL Tool   │   │ RAG Tool   │   │  ML Tool   │
             └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
                   │                │                │
                   ▼                ▼                ▼
             PostgreSQL        Chroma/BM25       ML Model
                    \               │              /
                     \              │             /
                      └─────────────┼────────────┘
                                    ▼
                            ┌───────────────┐
                            │  Coordinator  │
                            └───────┬───────┘
                                    ▼
                            ┌───────────────┐
                            │ Answer Merger │
                            └───────┬───────┘
                                    │
                                    ▼
                              Final Answer
```

**Logistics Copilot = one conversational interface over structured data, unstructured operational knowledge, and predictive shipment intelligence.**

---
