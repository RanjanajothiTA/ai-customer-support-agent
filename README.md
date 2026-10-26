
# ShopEase AI Customer Support Agent

ShopEase is a local MVP customer-support demo. A Streamlit chat interface sends
customer messages to a FastAPI backend. The backend routes supported requests
to SQLite tools or a retrieval-augmented generation (RAG) pipeline, and stores
conversation history in SQLite.

## Capabilities

- Look up order status and refund status, scoped to the supplied customer ID.
- Answer return, refund, shipping, and warranty policy questions using the
  knowledge base and display supporting source chunks.
- Ask for missing information for incomplete refund, order, or cancellation
  requests; unsupported requests receive a safe escalation response.
- Require an explicit confirmation before an eligible order cancellation.
- Persist conversation messages, context, and pending cancellation state.
- Reject attempts to reuse a conversation ID under a different customer ID.

The customer ID is an identifier, **not authentication**. This application is
for local demonstration with synthetic data, not production customer accounts.

## Architecture

```text
Streamlit (ui.py)
       | POST /chat
       v
FastAPI (app/main.py)
       |-- Agent routing (app/agent/)
       |-- SQLite tools and conversation memory (app/tools/, app/memory/)
       `-- RAG retrieval and answer grounding (app/rag/)
```

The API accepts `message`, `customer_id`, and `conversation_id`; responses
contain a string `response` and a `sources` list. `GET /health` is the health
check. FastAPI also exposes its interactive API documentation at `/docs`.

## Local setup

Run commands from this project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The Google Gen AI SDK needs a Gemini API key through its supported environment
configuration. A local `.env` file is loaded by the application and is ignored
by Git. Never commit or share the key.

### Required local data

The application uses the following files:

- `data/database/shopease.db` — SQLite database containing the schema and demo
  records.
- `data/vector_store/chunks.json` and `data/vector_store/shopease.index` —
  generated RAG chunks and FAISS index.
- `data/knowledge_base/*.pdf` — source policy and product documents tracked by
  Git.

The SQLite database and generated vector-store files are ignored by Git. On a
fresh clone, create the demo database and build the vector store using the
provided scripts:

```powershell
python scripts\init_demo_database.py
python scripts\build_vector_store.py
```

The database initializer and vector-store builder protect existing files from
accidental overwrites. If the target files already exist, review them before
attempting to rebuild; do not use the vector-store builder's `--force` option
unless you intentionally want to replace the existing artifacts.

The vector-store builder reads the knowledge-base PDFs, generates embeddings,
and creates the FAISS index and corresponding chunk file. The generated files
are required before starting the full application.

A clean-clone setup still needs to be verified using these documented steps.
The setup scripts are present in this working tree but are not yet tracked by
Git, so they must be included in a checkout before these commands are
available there.

## Run the application

In the first PowerShell terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

In a second terminal:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run ui.py
```

Open the URL printed by Streamlit (normally `http://localhost:8501`). The UI
uses `http://127.0.0.1:8000` for FastAPI. Check
`http://127.0.0.1:8000/health` and `/docs` if the UI cannot connect.

The UI keeps a conversation ID stable across Streamlit reruns and starts a new
local conversation when the customer ID changes. It shows connection, timeout,
HTTP, and malformed-response errors without displaying backend exception
details.

## Tests

Run the automated test suite with:

```powershell
python -m pytest -q
```

The latest test run completed with **46 passed and 2 deprecation warnings**.
The warnings originate from the installed Starlette/httpx and AnyIO
dependencies; they did not fail the test suite.

Verify that the RAG vector store can be rebuilt independently without
overwriting the existing artifacts:

```powershell
python scripts\verify_rag_rebuild.py
```

The RAG rebuild verification checks that the index and chunks can be rebuilt
and loaded together, retrieval returns relevant chunks, and a simulated
chunk-save failure does not publish incomplete artifacts. The latest run
passed all three checks.

Some tests may write conversation or support-ticket records to SQLite. Run
tests against a disposable database copy rather than valuable or live data.

See [MVP 1 Release Readiness Report](./MVP1_RELEASE_READINESS_REPORT.md) for
the audit scope, results, and remaining limitations.

## Known MVP limitations

- There is no user authentication; customers can enter an ID in the UI.
- SQLite, the local API URL, and the local data files are intended for a
  single-machine demo, not concurrent or production deployment.
- Database and vector-store setup scripts are available, but a fresh-clone
  setup has not yet been verified end to end.
- Support-ticket tooling exists, but a complete user-facing create-ticket
  conversation flow is not currently routed by the decision engine.
- Dependencies in `requirements.txt` are not version-pinned.
- LLM-dependent answers require a valid Gemini configuration and external
  service availability.

See [MVP 1 Release Readiness Report](./MVP1_RELEASE_READINESS_REPORT.md) for the
audit scope, test results, findings, and freeze decision.
