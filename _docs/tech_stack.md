# Tech Stack Specification — `tailr`

## 1. Overview & Architecture Philosophy

`tailr` is designed as a **100% locally hosted, local-first web application**. It runs completely on the user's local machine with zero required cloud database or external authentication services.

- **Hosting Environment**: Localhost (macOS / Unix / Windows)
- **Primary Language**: Python 3.11+
- **Architecture Pattern**: Monolithic Django application with reactive HTMX frontend and direct async LLM pipeline orchestration
- **Workflow & Process**: Follows [`_docs/process.md`](file:///Users/dani-guerra/Documents/tailr/_docs/process.md) and [`AGENTS.md`](file:///Users/dani-guerra/Documents/tailr/AGENTS.md) (one GitHub issue at a time, test-verified via `uv run pytest`).

---

## 2. Technology Choices

### 2.1 Backend Framework & Core
| Component | Technology | Rationale |
|---|---|---|
| **Web Framework** | **Django 5.x** | Batteries-included web framework with robust ORM, routing, template engine, and middleware. |
| **Database** | **SQLite (`db.sqlite3`)** | Zero-configuration local database. Supports `JSONField` natively for flexible raw data bank entries, tag taxonomies, and multi-step pipeline run logs. |
| **Authentication** | **Django Built-in Auth** | Secure local user sessions, login, and registration out of the box without external SaaS auth dependencies. |
| **Admin Panel** | **Django Admin** | Built-in interface to inspect, filter, edit, and audit Raw Data Bank records, inspect prompt logs, and manage job folders. |

---

### 2.2 Frontend & User Interface (Option A)
| Component | Technology | Rationale |
|---|---|---|
| **Templating** | **Django Templates (HTML5)** | Clean server-rendered HTML with full access to Django context, template tags, and filters. |
| **Reactivity** | **HTMX 2.x** | Provides Single-Page-App (SPA) speed and interactivity using HTML attributes. Handles partial page swaps, inline form validation, and Server-Sent Events (SSE). |
| **Client Interactivity** | **Alpine.js 3.x** | Lightweight (15kb) JavaScript utility for client-only UI states (modals, dropdowns, collapsible sections, copy-to-clipboard). |
| **Styling** | **Tailwind CSS 3.x / 4.x** | Utility-first CSS framework for a modern, responsive, and clean design system. Compiled via standalone Tailwind CLI. |
| **Icons** | **Lucide Icons** | Clean, consistent SVG icon set. |

---

### 2.3 AI Pipeline & LLM Orchestration
| Component | Technology | Rationale |
|---|---|---|
| **LLM Provider** | **Anthropic Claude API** (`anthropic` Python SDK) | Leading reasoning and document generation capabilities. |
| **Models** | • **Claude 3.7 / 3.5 Sonnet** (Drafter, Skeptical Recruiter, Reviser)<br>• **Claude 3.5 Haiku** (Data Sufficiency Check, ATS Keyword Extraction) | Balance of deep reasoning for content creation and high-speed efficiency for parsing/matching. |
| **Schema Validation** | **Pydantic v2** | Enforces strict structured JSON outputs from Claude (e.g., exactly 3 recruiter rejection reasons, structured XYZ bullet points with measurable metrics). |
| **Pipeline Streaming** | **Server-Sent Events (SSE)** | Uses Django's `StreamingHttpResponse` paired with HTMX SSE to stream live progress indicators to the user as each agent finishes its step. |

---

### 2.4 Document Processing & Generation (ATS-Safe CV & Notes)
| Task | Library | Description |
|---|---|---|
| **CV Ingestion / Import** | `pdfplumber`, `pypdf`, `python-docx` | Extracts structured text and metadata from user-uploaded PDFs and Word documents to populate the Raw Data Bank. |
| **ATS-Safe PDF Export** | `WeasyPrint` or `Playwright` | Renders clean, single-column, standard-header HTML/CSS templates into selectable-text, ATS-friendly PDFs. |
| **ATS-Safe DOCX Export** | `python-docx` | Generates native Microsoft Word (.docx) files without tables, text boxes, or floating elements that trigger ATS parsing errors. |
| **Notes Export** | Native Python file streams | Exports recruiter critiques, keyword match analysis, and gap assessments as standard `.txt` and `.md` files. |

---

### 2.5 Development, Security & Tooling
| Tool | Technology | Rationale |
|---|---|---|
| **Package & Env Manager** | **`uv` (`pyproject.toml`)** | Ultra-fast Python package resolver, dependency lockfile (`uv.lock`), and virtual environment manager. |
| **Test Runner** | **`pytest` + `pytest-django`** | High-performance testing suite executed via `uv run pytest`. |
| **Secrets & Configuration** | `python-dotenv` | Loads `ANTHROPIC_API_KEY` and Django settings from a local `.env` file (excluded from git via `.gitignore`). |
| **Code Quality** | `ruff` | Fast, unified linter and formatter. |
| **Version Control** | `git` & GitHub | Issue tracking and source code version control. |

---

## 3. Data Flow & Execution Pipeline

```
1. User uploads existing CV / enters work history
   └─► pdfplumber / python-docx parses entries
       └─► Pydantic validates structured schema
           └─► Stored in SQLite (DataBankEntry with tags & JSON metrics)

2. User creates a Job Application Folder & pastes job description
   └─► User clicks "Run Tailr Pipeline"
       └─► Django triggers async pipeline (SSE Stream):
           ├─► Step 0: Data Sufficiency Check (Haiku)
           ├─► Step 1: XYZ Bullet Drafter (Sonnet)
           ├─► Step 2: Skeptical Senior Recruiter (3 Critique Points - Sonnet)
           ├─► Step 3: ATS Keyword Filter & Coverage Check (Haiku)
           ├─► Step 4: Reviser (Sonnet)
           └─► Step 5: Final Match Analysis (Sonnet)
       └─► HTMX live-updates UI status cards in real time

3. Output & Export
   ├─► Primary View: Editable CV draft ──► Export to PDF (WeasyPrint) & DOCX (python-docx)
   └─► Secondary Tab: Notes & Critiques ──► Export to Markdown (.md) / Text (.txt)
```
