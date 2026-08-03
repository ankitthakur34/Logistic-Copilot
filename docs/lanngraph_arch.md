Logistics Copilot - LangGraph Architecture
Overview

The Logistics Copilot is an Agentic AI application built using LangGraph.

Instead of directly calling one LLM, the system behaves like an intelligent employee that:

Understands the user's question
Decides which tools are required
Executes tools independently
Collects results
Produces one final response

The system is modular, scalable and production-ready.

High Level Flow
                User Question
                      │
                      ▼
                Service Registry
                      │
                      ▼
                 LangGraph Invoke
                      │
                      ▼
                  Router Node
                      │
        ┌─────────────┼─────────────┐
        │             │             │
       SQL           RAG         (Future ML)
        │             │
        └───────┬─────┘
                ▼
          Coordinator Node
                │
                ▼
            Merge Node
                │
                ▼
          Final Answer
                │
                ▼
            Flask API
                │
                ▼
            React Frontend
Overall Project Structure
backend/

app/

    agents/
        router_agent/
        rag_agent/
        sql_agent/
        merger_agent/

    langgraph/
        graph.py
        state.py
        nodes/

    tools/
        rag/
        sql/
        (future ml)

    bootstrap/
        service_registry.py

frontend/
Service Registry
Purpose

Service Registry acts as the application's Dependency Injection container.

Instead of creating objects repeatedly, everything is created once.

Example:

LLMs

Database

Embeddings

Retriever

Graph

Tools

All are initialized only once.

Then any API simply does

registry = ServiceRegistry()

and gets access to every service.

Why?

Without Service Registry

Request

↓

Create LLM

↓

Load Vector DB

↓

Connect SQL

↓

Create Graph

Every request becomes slow.

With Registry

Application Starts

↓

Everything loads once

↓

Every request reuses them

Much faster.

LangGraph State

Every node shares one common state.

Example

AgentState

Contains

question

router_result

tool_results

all_tools_success

execution_result

answer

Instead of passing 20 variables, every node reads/writes from the same state.

Router Node

First node.

Responsibility

Understand the user's question.

It DOES NOT answer.

It only decides

Which tools should run?

Example

Question

Show delayed shipments

Router returns

SQL

Question

Explain customs SOP

Router returns

RAG

Question

Why was SHP0001 delayed?

Router returns

SQL

+

RAG

Future

Will SHP0001 be delayed?

Router

SQL

+

ML
Router Agent

Inside Router Node we use Router Agent.

It is only responsible for classification.

Returns

RouterResult

Example

tools=[SQL,RAG]

confidence=0.96

reason="Shipment explanation requires structured data and documents."
SQL Node

Runs only when Router selects SQL.

Responsibilities

Query Postgres
Fetch shipment
Incident
Customer
ETA
Structured data

Returns

ToolResult

Example

Shipment

ETA

Delay Reason
RAG Node

Runs only when Router selects RAG.

Responsibilities

Search Vector Database.

Pipeline

Question

↓

Retriever

↓

Children

↓

Parents

↓

LLM

↓

Answer

Returns

ToolResult
Why Parent Retrieval?

Instead of sending only tiny chunks

Customs

We retrieve

Whole SOP

This gives better answers.

Coordinator Node

One of the most important nodes.

Its responsibility

Wait until every required tool has completed.

Example

Router

SQL

+

RAG

SQL finishes

↓

Coordinator

Wait.

RAG finishes

↓

Coordinator

Proceed.

Without Coordinator

Merge could happen before all tools finish.

Merge Node

Last intelligent node.

Responsibilities

Collect all tool outputs.

Send them to Merger Agent.

Generate final response.

Example

Inputs

SQL

Shipment delayed due to weather

RAG

Incident report

Customer email

Weather SOP

Output

One clean answer.

Merger Agent

Unlike Router

Merger actually uses LLM.

Responsibilities

Combine SQL
Combine RAG
Remove duplicate information
Produce coherent answer

Returns

RouterExecutionResult

Contains

answer

tool_results
ToolResult

Every tool returns identical structure.

ToolResult

Contains

tool_name

success

answer

sources

metadata

error

Because every tool returns the same format,

Merge Node doesn't care whether the result came from

SQL

RAG

Future ML

Everything is uniform.

Current Graph
START

↓

Router

↓

SQL

↓

Coordinator

↓

Merge

↓

END

or

START

↓

Router

↓

RAG

↓

Coordinator

↓

Merge

↓

END

or

START

↓

Router

↓

SQL

↓

Coordinator

↑

↓

RAG

↓

Merge

↓

END

Coordinator prevents waiting forever while still ensuring Merge runs only after the required tools finish.

Flask API

Frontend never interacts with LangGraph directly.

Flow

Frontend

↓

POST /chat

↓

registry.graph.invoke()

↓

LangGraph

↓

execution_result

↓

JSON

↓

Frontend
Frontend

Current React UI

Contains

Sidebar
Chat Window
Chat Input
Chat History
Source Badges

Frontend only consumes

{
  "answer": "...",
  "tool_results":[]
}

It has no knowledge of LangGraph internals.

Current Features

✅ Router Agent

✅ SQL Tool

✅ RAG Tool

✅ Coordinator

✅ Merge Node

✅ Parent Retrieval

✅ Flask API

✅ React Frontend

✅ Sidebar History

✅ Source Badges

Future Extension

The architecture is designed to be easily extensible.

ML Prediction Tool

Add

ML Node

Router

SQL

+

ML

Coordinator waits

↓

Merge

No existing code changes.

Future Tools

Can be added similarly:

Email Tool
Slack Tool
Calendar Tool
Weather Tool
SAP Tool
Jira Tool
Notification Tool

The Router decides which tools to invoke, Coordinator synchronizes them, and Merge combines the results.

Why this Architecture?

This architecture follows key software engineering principles:

Single Responsibility Principle: Each node has one job (routing, querying, coordination, merging).
Open/Closed Principle: New tools can be added without modifying existing nodes.
Loose Coupling: Tools are independent and communicate only through the shared AgentState.
Dependency Injection: ServiceRegistry creates and manages shared services once.
Scalability: The graph can grow from 2 tools (SQL, RAG) to many tools (ML, Email, Slack, etc.) without redesigning the architecture.
Production Readiness: Clean separation between API, orchestration, tools, agents, and frontend makes testing, maintenance, and deployment straightforward.
Final Architecture
                React UI
                    │
                    ▼
               Flask API
                    │
                    ▼
             Service Registry
                    │
                    ▼
                LangGraph
                    │
        ┌───────────┴───────────┐
        │                       │
    Router Agent          Shared State
        │
        ▼
   Tool Selection
        │
 ┌──────┼─────────────┐
 │      │             │
SQL    RAG        Future ML
 │      │             │
 └──────┴─────────────┘
        │
        ▼
  Coordinator Node
        │
        ▼
   Merger Agent
        │
        ▼
   Final Response
        │
        ▼
     React UI

This summarizes the architecture you've built: a modular, agentic logistics copilot with clear orchestration, reusable services, extensible tools, and a frontend that remains decoupled from the AI workflow.