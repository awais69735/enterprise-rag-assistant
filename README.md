# Enterprise RAG Assistant

An enterprise-oriented RAG application for internal company knowledge, combining document retrieval with structured HR analytics, JWT authentication, RBAC, guardrails, and AI-powered query routing.

The project is designed to demonstrate how an internal AI assistant can work with both **unstructured company documents** and **structured employee data** while enforcing access control before data reaches the retrieval or tool layer.

---

## Project Status

### Completed

* Project structure
* Company document ingestion
* Document chunking
* Local embeddings
* Qdrant vector database
* RAG retrieval
* Groq LLM integration
* JWT authentication
* Role-Based Access Control
* Department-level document filtering
* HR structured data access
* HR field-level access control
* HR analytics tools
* PII input detection
* PII response validation
* Out-of-scope guardrail
* Guardrail audit logging
* Streamlit interface
* FastAPI `/chat` endpoint
* AI HR intent router foundation

### In Progress

* HR AI router integration
* Semantic scope routing
* Unified HR + RAG query routing
* Unified answer orchestration
* Automated evaluation
* LangSmith monitoring
* Token/cost tracking
* Prometheus metrics
* Docker application deployment
* Azure deployment
* Full integration testing
* Production security hardening

---

# Architecture

```text
                         User
                           |
                           v
                    Streamlit UI
                           |
                           v
                       FastAPI
                           |
                           v
                 JWT Authentication
                           |
                           v
                          RBAC
                           |
                           v
                      Guardrails
                           |
                           v
                    AI Query Router
                     /           \
                    /             \
                  HR              RAG
                  |                |
                  v                v
             HR Intent          Qdrant
               Router          Retriever
                  |                |
                  v                v
            HR Analytics       Documents
               Tools
                  |
                  v
              Pandas
                  |
                  +-------+
                          |
                          v
                         LLM
                          |
                          v
                  Response Guardrail
                          |
                          v
                       Response
```

---

# Core Design Principle

Authorization is enforced **before retrieval and tool execution**.

The application does not retrieve restricted information and then rely on the LLM to hide it.

The intended security flow is:

```text
Authentication
      ↓
Authorization
      ↓
Input Guardrails
      ↓
AI Routing
      ↓
Restricted Retrieval / Tool
      ↓
LLM
      ↓
Response Guardrails
      ↓
Response
```

---

# Technology Stack

## Backend

* Python
* FastAPI
* LangChain
* Pydantic

## LLM

* Groq
* `openai/gpt-oss-20b`

## RAG

* Qdrant
* Sentence Transformers
* `BAAI/bge-small-en-v1.5`
* LangChain text splitters

## Structured Data

* Pandas
* CSV

## Authentication

* JWT
* `python-jose`

## Frontend

* Streamlit

## Infrastructure

* Docker
* Docker Compose

## Planned

* LangSmith
* Ragas
* Prometheus
* Azure

---

# Project Structure

```text
enterprise-rag-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── authentication.py
│   │   ├── jwt.py
│   │   ├── rbac.py
│   │   ├── users.py
│   │   ├── hr_access.py
│   │   ├── hr_tools.py
│   │   └── hr_router.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── retriever.py
│   │   ├── llm.py
│   │   └── pipeline.py
│   │
│   ├── guardrails/
│   │   ├── __init__.py
│   │   ├── pii.py
│   │   ├── scope.py
│   │   ├── manager.py
│   │   └── audit.py
│   │
│   ├── evaluation/
│   │
│   └── ui/
│       ├── __init__.py
│       └── streamlit_app.py
│
├── data/
│   ├── engineering/
│   ├── finance/
│   ├── general/
│   ├── hr/
│   └── marketing/
│
├── processed_data/
│   └── document_chunks.json
│
├── scripts/
│   ├── ingest_documents.py
│   ├── create_vector_db.py
│   ├── test_retriever.py
│   ├── test_hr_tools.py
│   └── test_hr_router.py
│
├── tests/
│
├── docs/
│
├── logs/
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Dataset

The current project uses company-style internal documents organized by department.

```text
data/
├── engineering/
│   └── engineering_master_doc.md
│
├── finance/
│   ├── financial_summary.md
│   └── quarterly_financial_report.md
│
├── general/
│   └── employee_handbook.md
│
├── hr/
│   └── hr_data.csv
│
└── marketing/
    ├── marketing_report_2024.md
    ├── marketing_report_q1_2024.md
    ├── marketing_report_q2_2024.md
    ├── marketing_report_q3_2024.md
    └── market_report_q4_2024.md
```

The current dataset contains:

* 9 Markdown documents
* 1 structured HR CSV
* 123 generated document chunks
* 100 HR employee records

---

# Document Ingestion

Markdown documents are recursively loaded and split using:

```text
RecursiveCharacterTextSplitter
```

Current configuration:

```text
chunk_size = 1000
chunk_overlap = 150
```

The resulting chunks are stored in:

```text
processed_data/document_chunks.json
```

Each chunk contains metadata such as:

```json
{
  "source": "finance/financial_summary.md",
  "filename": "financial_summary.md",
  "department": "finance",
  "access_roles": [
    "finance",
    "executive"
  ],
  "chunk_index": 0
}
```

---

# Embeddings

The project uses:

```text
BAAI/bge-small-en-v1.5
```

The embedding dimension is:

```text
384
```

The model runs locally, avoiding a separate embedding API dependency.

---

# Vector Database

Qdrant is used as the vector database.

Local development endpoint:

```text
http://localhost:6333
```

Collection:

```text
enterprise_documents
```

Qdrant runs using Docker Compose.

Start it with:

```powershell
docker compose up -d
```

---

# RAG Pipeline

The current document RAG pipeline is:

```text
User Question
      ↓
Question Embedding
      ↓
Qdrant Search
      ↓
RBAC Department Filter
      ↓
Relevant Chunks
      ↓
Context
      ↓
Groq LLM
      ↓
Answer
```

The model is instructed to answer using the retrieved company context and avoid inventing information that is not present in the context.

---

# Authentication

The API uses JWT authentication.

Demo users:

| Username   | Role        |
| ---------- | ----------- |
| `alice`    | finance     |
| `bob`      | hr          |
| `charlie`  | marketing   |
| `david`    | engineering |
| `ceo`      | executive   |
| `employee` | employee    |

These credentials are for local development only.

A production implementation should use:

* Password hashing
* A persistent user database
* A production identity provider
* Secret management
* Token rotation and stronger security controls

---

# RBAC

The application defines access by role.

```text
Finance
 ├── Finance documents
 └── General documents

HR
 ├── HR data
 └── General documents

Marketing
 ├── Marketing documents
 └── General documents

Engineering
 ├── Engineering documents
 └── General documents

Executive
 ├── Finance
 ├── HR
 ├── Marketing
 ├── Engineering
 └── General

Employee
 └── General
```

RBAC is enforced at the application/data layer rather than relying on the LLM.

---

# HR Structured Data

HR data is stored in:

```text
data/hr/hr_data.csv
```

The dataset contains:

```text
employee_id
full_name
role
department
email
location
date_of_birth
date_of_joining
manager_id
salary
leave_balance
leaves_taken
attendance_pct
performance_rating
last_review_date
```

There are currently:

```text
100 employee records
```

---

# HR Field-Level Access

HR data uses field-level permissions.

The following fields are available to HR:

```text
employee_id
full_name
role
department
email
location
date_of_joining
manager_id
salary
leave_balance
leaves_taken
attendance_pct
performance_rating
last_review_date
```

`date_of_birth` is intentionally excluded from the accessible field set.

Executive access also excludes `date_of_birth`.

---

# Why HR Data Uses Pandas Instead of RAG

Structured questions such as:

```text
How many employees do we have?
```

require exact calculations.

Embedding the entire CSV and relying on semantic retrieval could result in:

* Incorrect aggregation
* Missing records
* Numerical hallucination
* Stale answers

Instead, this project uses:

```text
Natural Language Question
          ↓
AI Intent Classification
          ↓
Structured HR Operation
          ↓
Pandas
          ↓
Exact Result
          ↓
LLM Explanation
```

The LLM determines **what operation is required**.

Python/Pandas determines **the actual number**.

---

# HR Analytics Tools

Currently implemented operations:

```text
employee_count
employee_joining_trend
employee_count_by_department
```

## Employee Count

Current result:

```text
100 employees
```

## Employee Joining Trend

Current dataset:

```text
2018: 14
2019: 15
2020: 13
2021: 19
2022: 10
2023: 15
2024: 14
```

## Department Distribution

```text
Business: 6
Compliance: 5
Data: 8
Design: 3
Finance: 16
HR: 4
Marketing: 7
Operations: 6
Product: 3
Quality Assurance: 7
Risk: 5
Sales: 15
Technology: 15
```

---

# AI HR Intent Router

The project intentionally avoids static keyword matching.

The system should understand different ways of expressing the same request.

For example:

```text
How many employees do we have?

What's our current headcount?

How large is our workforce?
```

All represent:

```text
employee_count
```

Another example:

```text
How many people joined each year?

Show workforce growth over the years.

Give me the yearly employee trend.
```

These represent:

```text
employee_joining_trend
```

The router uses structured output from the LLM.

Supported intents:

```text
employee_count
employee_joining_trend
employee_count_by_department
unknown
```

Current router file:

```text
app/auth/hr_router.py
```

Test:

```powershell
python -m scripts.test_hr_router
```

The Groq model must be configured as:

```python
model="openai/gpt-oss-20b"
```

---

# Guardrails

The application currently contains multiple guardrail layers.

## PII Detection

The system detects patterns such as:

* Email addresses
* Phone numbers
* National ID patterns

Example:

```text
john@example.com
```

can be blocked before reaching the RAG/LLM pipeline.

---

## Response PII Validation

Generated answers are checked before being returned.

If sensitive information is detected in the generated response, the response can be blocked.

---

## Out-of-Scope Detection

The application also has an out-of-scope guardrail.

Examples:

```text
How many employees do we have?
```

is relevant.

While:

```text
Tell me a joke.
```

is outside the intended company knowledge scope.

The current implementation uses a scope classifier based on allowed topics. A later project stage will replace this with semantic/LLM-based scope classification so natural-language variations are handled more reliably.

---

# Guardrail Audit Logging

Blocked guardrail events are written to:

```text
logs/guardrail_audit.jsonl
```

Example:

```json
{
  "timestamp": "...",
  "username": "alice",
  "role": "finance",
  "action": "blocked",
  "blocked": true,
  "reason": "pii_detected",
  "details": [
    "email"
  ]
}
```

The audit layer intentionally avoids logging the complete sensitive question or response.

---

# FastAPI API

Start the backend:

```powershell
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Login

Endpoint:

```text
POST /auth/login
```

Example:

```json
{
  "username": "alice",
  "password": "alice123"
}
```

The API returns a JWT access token.

---

# Current User

Endpoint:

```text
GET /auth/me
```

Requires:

```text
Authorization: Bearer <JWT>
```

---

# Chat

Endpoint:

```text
POST /chat
```

Example:

```json
{
  "question": "What were our financial results?"
}
```

The endpoint requires a valid JWT.

The user's role is taken from the authenticated session and passed into the RAG layer.

---

# Streamlit

The Streamlit application is located at:

```text
app/ui/streamlit_app.py
```

Start it with:

```powershell
streamlit run app/ui/streamlit_app.py
```

The UI currently supports:

* User login
* JWT authentication
* Role display
* Chat
* Answer display
* Source display
* Guardrail responses
* Logout

---

# Installation

## 1. Create Virtual Environment

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

Example:

```env
GROQ_API_KEY=your_groq_api_key

JWT_SECRET=your_secure_random_secret

LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=enterprise-rag-assistant
```

Never commit `.env`.

Use `.env.example` as the template.

---

# Running the Project

## Start Qdrant

```powershell
docker compose up -d
```

---

## Ingest Documents

```powershell
python -m scripts.ingest_documents
```

---

## Create Vector Database

```powershell
python -m scripts.create_vector_db
```

---

## Test Retriever

```powershell
python -m scripts.test_retriever
```

---

## Test HR Tools

```powershell
python -m scripts.test_hr_tools
```

---

## Test HR Router

```powershell
python -m scripts.test_hr_router
```

---

## Start FastAPI

```powershell
uvicorn app.main:app --reload
```

---

## Start Streamlit

Open another terminal:

```powershell
streamlit run app/ui/streamlit_app.py
```

---

# Testing

The project is being developed with tests covering:

```text
Authentication
JWT
RBAC
HR data access
HR analytics
Guardrails
RAG retrieval
API endpoints
AI routing
```

Run the complete test suite with:

```powershell
pytest
```

---

# Example Queries

## HR

```text
How many employees do we have?

What's our current headcount?

How large is our workforce?

How many people joined the company each year?

Show workforce growth over the years.

Give me the employee breakdown by department.

How many people work in Finance?
```

## Finance

```text
What were the company's financial results?

Show me the quarterly financial report.

What were our major financial expenses?
```

## Marketing

```text
What were our Q2 marketing expenses?

Show me the marketing report.

What were the major marketing activities?
```

## General

```text
What is the company leave policy?

What does the employee handbook say about attendance?
```

## Out of Scope

```text
Tell me a joke.

Write me a poem.

What's the weather today?
```

---

# Current Development Roadmap

## Phase 1 — Foundation

* [x] Project structure
* [x] Dataset
* [x] Document ingestion
* [x] Chunking
* [x] Embeddings
* [x] Qdrant
* [x] RAG retriever
* [x] LLM integration

## Phase 2 — Security

* [x] Authentication
* [x] JWT
* [x] RBAC
* [x] Department filtering
* [x] HR field-level access
* [x] PII guardrails
* [x] Response validation
* [x] Audit logging

## Phase 3 — Structured HR Intelligence

* [x] HR CSV integration
* [x] Employee count
* [x] Joining trend
* [x] Department analysis
* [x] HR authorization
* [x] HR tools
* [x] AI HR router foundation

## Phase 4 — AI Orchestration

* [ ] Connect HR router to HR tools
* [ ] Semantic scope classifier
* [ ] Unified HR/RAG query router
* [ ] Unified answer service
* [ ] Connect unified service to `/chat`

## Phase 5 — Evaluation

* [ ] Evaluation dataset
* [ ] Retrieval evaluation
* [ ] Answer evaluation
* [ ] Ragas integration
* [ ] RBAC security evaluation
* [ ] Automated evaluation pipeline

## Phase 6 — Monitoring

* [ ] LangSmith
* [ ] Request tracing
* [ ] Token tracking
* [ ] Cost tracking
* [ ] Prometheus metrics
* [ ] Monitoring dashboard

## Phase 7 — Deployment

* [ ] Application Docker image
* [ ] Docker Compose production setup
* [ ] Azure
