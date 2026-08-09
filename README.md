# Logistics Copilot

Agentic AI logistics assistant combining **SQL**, **RAG**, and **Machine
Learning** tools with **LangGraph** orchestration.

## Architecture

``` mermaid
flowchart TD
    A[User Question] --> B[Flask API]
    B --> C[Service Registry]
    C --> D[LangGraph]
    D --> E[Normalizer]
    E --> F[Router Agent]
    F --> G[SQL]
    F --> H[RAG]
    F --> I[ML]
    G --> J[Coordinator]
    H --> J
    I --> J
    J --> K[Answer Merger]
    K --> L[Final Answer]
```

## Core Tools

### SQL Tool

``` mermaid
flowchart TD
    A[Question] --> B[Schema Builder]
    B --> C[SQL Generator]
    C --> D[SQL Validator]
    D --> E[SQL Executor]
    E --> F[(PostgreSQL)]
    F --> G[Rows]
    G --> H[SQL Answer Generator]
    H --> I[Answer]
```

Flow:

`Question → Schema Builder → SQL Generator → Validator → Executor → Database → Answer Generator → Answer`

The SQL agent contains `SchemaBuilder`, `SQLGenerator`, `SQLValidator`,
`SQLExecutor`, and `SQLAnswerGenerator`.

### RAG Tool

``` mermaid
flowchart TD
    A[Documents] --> B[MultiLoader]
    B --> C[Parent Child Chunker]
    C --> D[Child Chunks]
    D --> E[Chroma]
    D --> F[BM25]
    G[Question] --> H[Query Decomposition]
    G --> I[Multi Query Generation]
    I --> J[Hybrid Retrieval]
    E --> J
    F --> J
    J --> K[RRF]
    K --> L[Cross Encoder Reranker]
    H --> L
    L --> M[Context Compression]
    M --> N[Answer Generator]
    N --> O[Answer]
```

RAG supports Markdown, PDF, CSV and JSON ingestion.

Retrieval stack:

`Dense Chroma + Sparse BM25 → Hybrid Retrieval → RRF → Multi Query → Reranking → Query Decomposition → Context Compression → Generation`

The RAG system also includes DeepEval-based evaluation with answer
metrics and retrieval precision/recall.

### ML Tool

``` mermaid
flowchart TD
    A[Shipment Number] --> B[Shipment Repository]
    B --> C[Prediction Features]
    C --> D[ML Prediction Service]
    D --> E[Trained Model]
    E --> F[Prediction]
    C --> G[Risk Factors]
    F --> H[Prediction Response]
    G --> H
```

The ML system predicts shipment delay probability and exposes
confidence, on-time probability and risk factors.

Current risk factors include:

-   Maintenance vessel
-   Reefer container
-   Many pending tasks
-   Shipment near ETA
-   Multiple high-priority tasks

## LangGraph

Graph:

`START → Normalize → Router → SQL/RAG/ML → Coordinator → Merge → END`

Shared state contains:

-   `question`
-   `shipment_no`
-   `router_result`
-   `tool_results`
-   `all_tools_success`
-   `answer`
-   `execution_result`

## Service Registry

`ServiceRegistry` is the composition root. It creates and wires:

-   SQL agent/tool
-   RAG pipeline/tool
-   ML tool
-   Router LLM
-   Answer merger
-   LangGraph
-   Router Agent

Tools implement a common `BaseTool` abstraction.

## API

### Chat

``` http
POST /chat
Content-Type: application/json
```

``` json
{
  "question": "What is the revised ETA of SHP0001?"
}
```

### ML Prediction

``` http
POST /api/ml/predict-delay
Content-Type: application/json
```

``` json
{
  "shipment_no": "SHP0005"
}
```

## Project Structure

``` text
app/
├── agents/
│   ├── router_agent/
│   └── sql_agent/
├── bootstrap/
├── langgraph/
│   └── nodes/
├── rag/
│   ├── chunking/
│   ├── ingestion/
│   ├── retrieval/
│   ├── reranker/
│   ├── multi_query/
│   ├── decomposition/
│   ├── context_compression/
│   ├── generation/
│   └── evaluation/
├── ml/
│   ├── repositories/
│   ├── services/
│   ├── routes/
│   └── models/
└── tools/
    ├── base_tool.py
    ├── sql_tool.py
    ├── rag_tool.py
    └── ml_tool.py
```

## Installation

``` bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` with database, Groq and optional LangSmith configuration.
Never commit secrets.

## Requirements

Main technologies:

-   Flask
-   SQLAlchemy / PostgreSQL
-   LangGraph
-   LangChain Core
-   Groq
-   ChromaDB
-   Sentence Transformers
-   BM25
-   PyMuPDF
-   DeepEval
-   LangSmith
-   Alembic
-   Pydantic
-   Pandas
-   pytest

## Evaluation

RAG evaluation stores timestamped reports under:

``` text
app/rag/evaluation/reports/
```

Reports contain:

-   expected answer
-   actual answer
-   expected sources
-   retrieved sources
-   DeepEval metric scores
-   retrieval precision
-   retrieval recall

## Future Roadmap

``` text
Current Architecture
        ↓
Better Router Evaluation
        ↓
Memory
        ↓
Human-in-the-Loop
        ↓
MCP Integration
        ↓
Specialized Agents
        ↓
Multi-Agent Collaboration
        ↓
Observability
        ↓
Production Deployment
```

Future tools can include Email, Slack, Calendar, Shipment Tracking, Web
Search and Notification tools.

## Project Goal

Build a production-oriented **Agentic AI Logistics Copilot**
demonstrating RAG engineering, SQL agents, ML integration, LangGraph
orchestration, multi-agent systems, memory, MCP, tool calling,
evaluation, observability and scalable backend architecture.



