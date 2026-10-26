# SPARK --- Scientific Paper Analysis & Research Knowledge Discovery

SPARK is an AI-powered research assistant designed to help users explore
scientific literature, retrieve related papers, and eventually discover
research gaps and possible research directions.

> **Current status:** Early MVP / active development. The arXiv search
> and semantic-retrieval API endpoints have been tested successfully.
> The Streamlit interface has been created, but its complete end-to-end
> workflow still needs to be verified. Research-gap detection,
> multi-agent analysis, and the production frontend are not implemented
> yet.

## Project Goals

SPARK aims to:

-   Search scientific papers by research topic.
-   Process paper metadata, abstracts, and eventually full-text PDFs.
-   Summarize and compare papers.
-   Retrieve semantically related research using embeddings.
-   Build concept and citation relationships between papers.
-   Identify potential research gaps, clearly distinguishing
    AI-generated hypotheses from verified findings.
-   Suggest research ideas and experiments.
-   Produce a structured research-analysis report.

## Current Features

-   **FastAPI backend** with interactive API documentation.
-   **arXiv paper search** for retrieving paper metadata and abstracts.
-   **Sentence Transformers embeddings** using
    `sentence-transformers/all-MiniLM-L6-v2`.
-   **Qdrant vector search** using local persistent storage; Docker is
    not required for the current development setup.
-   **Semantic retrieval endpoint** returning papers ranked by embedding
    similarity.
-   **Streamlit MVP interface** for submitting a topic and displaying
    retrieved paper information (end-to-end UI testing is pending).
-   **PostgreSQL foundation** configured for structured data storage;
    persistence of all retrieved paper records is still to be completed.

## Technology Stack

  -----------------------------------------------------------------------
  Layer                   Technology              Current role
  ----------------------- ----------------------- -----------------------
  API backend             Python, FastAPI,        Implemented
                          Uvicorn                 

  Paper source            arXiv API               Implemented

  Embeddings              Sentence Transformers   Implemented

  Vector database         Qdrant local mode       Implemented for MVP

  Prototype UI            Streamlit               Created; integration
                                                  test pending

  Relational database     PostgreSQL, SQLAlchemy  Foundation started

  Planned frontend        Next.js, React,         Planned
                          Tailwind CSS            

  Planned agent workflow  LangGraph               Planned

  Planned knowledge graph Neo4j, NetworkX         Planned

  Planned local language  Ollama with a suitable  Planned
  models                  Llama/Qwen/Gemma model  
  -----------------------------------------------------------------------

## Project Roadmap --- 16 Phases

The roadmap below tracks the current implementation honestly.
"Implemented" means an initial working version exists; it does not mean
production-ready.

  -------------------------------------------------------------------------
  Phase             Name              Status            Notes
  ----------------- ----------------- ----------------- -------------------
  0                 Programming       Deferred          Intentionally
                    Foundations                         postponed while the
                                                        MVP is built;
                                                        learning will be
                                                        revisited later.

  1                 Backend           In progress       FastAPI setup,
                    Foundation                          configuration,
                                                        database
                                                        foundation, and
                                                        health/API routes.

  2                 Scientific Paper  Implemented ---   arXiv search
                    Search            MVP               endpoint returns
                                                        paper metadata and
                                                        abstracts.

  3                 PDF Processing    Not started       Extract text from
                                                        uploaded or
                                                        downloaded PDFs.

  4                 Paper             Not started       Generate structured
                    Summarization                       summaries from
                                                        paper content.

  5                 Embeddings        Implemented ---   Sentence
                                      MVP               Transformers
                                                        creates vectors for
                                                        paper title +
                                                        abstract and search
                                                        queries.

  6                 Vector Database   Implemented ---   Qdrant local
                                      MVP               persistent storage,
                                                        indexing, and
                                                        semantic retrieval.

  7                 Knowledge Graph   Not started       Extract concepts
                                                        and relationships
                                                        between papers.

  8                 Citation Graph    Not started       Represent paper
                                                        citations and
                                                        relationships.

  9                 Research Gap      Not started       Compare findings
                    Detection                           and identify
                                                        candidate gaps for
                                                        human review.

  10                Multi-Agent AI    Not started       Coordinate research
                                                        tasks with
                                                        LangGraph agents.

  11                Experiment        Not started       Suggest possible
                    Recommendation                      experiments to
                                                        investigate
                                                        candidate gaps.

  12                Confidence        Not started       Add transparent
                    Scoring                             evidence-based
                                                        confidence
                                                        indicators.

  13                Frontend          Prototype in      Streamlit UI
                                      progress          created; planned
                                                        production
                                                        interface is
                                                        Next.js.

  14                Deployment        Not started       Containerization,
                                                        hosting,
                                                        environment
                                                        configuration, and
                                                        deployment.

  15                Optimization      Not started       Improve latency,
                                                        reliability,
                                                        retrieval quality,
                                                        evaluation, and
                                                        cost.
  -------------------------------------------------------------------------

### Progress Summary

-   **Working core:** paper search → embedding generation → Qdrant
    indexing → semantic retrieval.
-   **API verification:** `POST /papers/index` and
    `POST /papers/semantic-search` were reported working.
-   **UI status:** Streamlit code is in place, but the complete
    UI-to-API flow must still be confirmed.
-   **Not yet available:** automated research-gap detection, full-paper
    analysis, citation/knowledge graphs, multi-agent workflow,
    experiment suggestions, and production deployment.
-   This is a feature-status report, not a claim that a specific
    percentage of the project is complete.

## Team Split-Up

  -----------------------------------------------------------------------
  Team member             Primary responsibility  Planned work
  ----------------------- ----------------------- -----------------------
  **Daya (Team Lead)**    AI/ML core              Embeddings, semantic
                                                  retrieval, paper
                                                  analysis, research-gap
                                                  detection, evaluation,
                                                  and coordinating
                                                  integration.

  **Praveen**             Backend and data        API structure,
                                                  scientific data
                                                  ingestion, PostgreSQL,
                                                  metadata handling, and
                                                  backend reliability.

  **Balaji**              Frontend and            User interface, search
                          visualization           experience,
                                                  paper-result views,
                                                  charts, and
                                                  research-report
                                                  presentation.
  -----------------------------------------------------------------------

The split is a working responsibility plan. Team members should
coordinate on API contracts, data schemas, and integration before
merging changes.

## Repository Structure

The structure may evolve as the project grows. The current backend is
developed in the `backend` directory.

``` text
SPARK/
├── README.md
└── backend/
    ├── app/
    │   ├── main.py
    │   ├── config.py
    │   ├── database.py
    │   ├── models.py
    │   ├── init_db.py
    │   ├── api/
    │   │   └── routes/
    │   │       └── papers.py
    │   └── services/
    │       ├── paper_search.py
    │       └── vector_store.py
    ├── streamlit_app.py
    ├── requirements.txt
    ├── .env.example
    └── .gitignore
```

Only commit files that actually exist in your working tree. The local
Qdrant database directory (`qdrant_data/`), virtual environment
(`.venv/`), secrets, and generated caches should not be committed.

## Prerequisites

-   Python 3.10 or compatible version supported by your installed
    dependencies.
-   PostgreSQL installed and a `spark` database created if your current
    configuration requires it.
-   Internet access for arXiv requests and the first download of the
    embedding model.
-   Git for version control.

Docker is **not required** for the current Qdrant local-mode
configuration.

## Local Setup (Windows PowerShell)

### 1. Clone the repository

``` powershell
git clone https://github.com/Dayanand-MK/SPARK.git
cd SPARK
cd backend
```

If you already have the project locally, open your existing
`D:\SPARK\backend` directory instead of cloning it over your files.

### 2. Create and activate a virtual environment

``` powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a package is missing, install it in the virtual environment and
update `requirements.txt`.

### 4. Configure environment variables

Create a local `.env` file in `backend/`. Use `.env.example` as a
template and replace placeholders with your own local values.

Example:

``` env
APP_NAME=SPARK API
APP_VERSION=0.1.0
ENVIRONMENT=development
DATABASE_URL=postgresql://postgres:YOUR_LOCAL_PASSWORD@localhost:5432/spark
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=scientific_papers
MAX_PAPERS=20
```

Use your own PostgreSQL credentials. **Never commit `.env`, passwords,
API keys, or tokens.** The current vector-store code uses Qdrant local
mode; the `QDRANT_URL` setting may remain in configuration for
compatibility but is not used by that local client.

### 5. Start the API

From `backend/`, in Terminal 1:

``` powershell
uvicorn app.main:app --reload
```

-   API base URL: `http://127.0.0.1:8000`
-   Interactive API docs: `http://127.0.0.1:8000/docs`

### 6. Start the Streamlit interface

Keep the API terminal running. Open a second terminal in `backend/`,
activate the same virtual environment, and run:

``` powershell
.\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

Streamlit normally opens at `http://localhost:8501`.

## API Endpoints

The following endpoints are part of the current MVP:

  ---------------------------------------------------------------------------
  Method                  Endpoint                    Purpose
  ----------------------- --------------------------- -----------------------
  `GET`                   `/health`                   Basic API health check,
                                                      if enabled in the
                                                      current app.

  `POST`                  `/papers/search`            Search arXiv for papers
                                                      matching a query.

  `POST`                  `/papers/index`             Fetch papers and index
                                                      their embeddings in
                                                      Qdrant.

  `POST`                  `/papers/semantic-search`   Retrieve semantically
                                                      similar indexed papers.

  `GET`                   `/docs`                     Interactive FastAPI
                                                      documentation.
  ---------------------------------------------------------------------------

Use `/docs` as the source of truth for the exact routes currently
registered by your local API.

### Example: Index papers

``` json
{
  "query": "plant disease detection",
  "limit": 5
}
```

### Example: Semantic search

``` json
{
  "query": "deep learning for crop health monitoring",
  "limit": 5
}
```

Similarity scores represent embedding similarity. They are **not**
percentages of factual correctness, research quality, or confidence.

## Data, Privacy, and Research Limitations

-   Paper metadata and abstracts are retrieved from arXiv; availability
    and response quality depend on the external service.
-   The current MVP embeds paper titles and abstracts, not full PDF
    contents.
-   Semantic similarity is a retrieval signal and should not be
    interpreted as proof that two papers make equivalent claims.
-   Research-gap suggestions, when implemented, must be treated as
    hypotheses requiring verification against the literature.
-   Keep local credentials and private research documents out of Git
    history.
-   Check the license and terms of any external model, dataset, or data
    source before redistribution.

## Development Workflow

1.  Create a feature branch for substantial changes.
2.  Keep API request/response formats documented.
3.  Test endpoints in `/docs` before integrating them into the UI.
4.  Avoid committing `.env`, `.venv/`, `qdrant_data/`, `__pycache__/`,
    or generated artifacts.
5.  Update this README when a phase changes status.
6.  Mark a phase complete only after its key behavior has been tested.

## Current Next Steps

1.  Verify the Streamlit interface can successfully call the running
    FastAPI backend.
2.  Improve PostgreSQL persistence for paper metadata and avoid
    duplicate records.
3.  Add PDF text extraction.
4.  Implement paper summarization.
5.  Build evaluation datasets and tests before adding research-gap
    claims.
6.  Continue through the roadmap in order, revisiting Phase 0
    foundations when the MVP is stable.

## Contributors

-   **Daya** --- Team Lead, AI/ML core
-   **Praveen** --- Backend and data
-   **Balaji** --- Frontend and visualization

------------------------------------------------------------------------

**SPARK is an active student research-engineering project.** Features
and roadmap statuses will change as implementation and testing progress.
