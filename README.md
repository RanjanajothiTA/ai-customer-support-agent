
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

The application expects these files at runtime:

- `data/database/shopease.db` — initialized SQLite schema and demo records.
- `data/vector_store/chunks.json` and `data/vector_store/shopease.index` —
  prebuilt RAG data.
- `data/knowledge_base/*.pdf` — source policy and product documents.

The SQLite database and vector-store outputs are ignored by Git. The repository
does not currently provide a complete database seed and vector-index build
workflow. A new clone therefore needs approved local demo data and generated
vector-store files before the full application can be run; creating only an
empty SQLite database is not sufficient.

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

Run the automated suite with:

```powershell
python -m pytest -q
```

The tests use the project's local database path. Some API tests persist
conversation rows and the support-ticket success test creates a ticket, so run
the suite against a disposable database copy rather than valuable or live data.
The release-readiness report records the isolated test procedure used for this
audit.

## Known MVP limitations

- There is no user authentication; customers can enter an ID in the UI.
- SQLite, the local API URL, and the local data files are intended for a
  single-machine demo, not concurrent or production deployment.
- Database seed data and generated vector-store files are not reproducibly
  created by the current repository setup.
- Support-ticket tooling exists, but a complete user-facing create-ticket
  conversation flow is not currently routed by the decision engine.
- Dependencies in `requirements.txt` are not version-pinned.
- LLM-dependent answers require a valid Gemini configuration and external
  service availability.

See [MVP 1 Release Readiness Report](./MVP1_RELEASE_READINESS_REPORT.md) for the
audit scope, test results, findings, and freeze decision.
