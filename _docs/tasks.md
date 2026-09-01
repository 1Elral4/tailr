# Project Backlog & Task Breakdown — `tailr`

## 1. Initialize Django Project and Base Test Suite
## Goal
Initialize an empty Django 5 project configured with `uv`, local SQLite, environment management, and a passing test suite.

## Description
Set up the project foundation using `uv` with a declarative `pyproject.toml` file managing dependencies (Django 5.x, pytest-django, python-dotenv). Configure Django settings for local development with SQLite (`db.sqlite3`), secret key loading from `.env`, and create a `core` app. Establish the test directory structure and a baseline test ensuring `uv run pytest` executes cleanly.

## Acceptance Criteria
- [ ] `pyproject.toml` exists and defines project metadata, Python `>=3.11`, and dependencies: `django>=5.0`, `pytest>=8.0`, `pytest-django>=4.8`, `python-dotenv>=1.0`.
- [ ] `uv sync` installs dependencies and creates a reproducible `uv.lock` file.
- [ ] Django project is initialized with an active `core` app in `INSTALLED_APPS`.
- [ ] `settings.py` loads `SECRET_KEY` and `DEBUG` from `.env` using `python-dotenv` with safe local fallbacks if `.env` is absent.
- [ ] Database is configured to SQLite (`db.sqlite3`) in the project root.
- [ ] `.env.example` exists documenting all required environment variables (`SECRET_KEY`, `DEBUG`, `ANTHROPIC_API_KEY`).
- [ ] `pytest.ini` or `[tool.pytest.ini_options]` in `pyproject.toml` is configured with `DJANGO_SETTINGS_MODULE`.
- [ ] Running `uv run pytest` passes at least one initial smoke test in `tests/test_smoke.py`.

## Out of Scope
- Static asset bundling, Tailwind CSS, or frontend templates (covered in [#2](https://github.com/1Elral4/tailr/issues/2)).
- Database models and business logic (covered in [#3](https://github.com/1Elral4/tailr/issues/3) and [#8](https://github.com/1Elral4/tailr/issues/8)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 2. Configure Tailwind CSS, HTMX, Alpine.js, and Base Layout
## Goal
Integrate Tailwind CSS, HTMX 2.x, Alpine.js 3.x, and a responsive base HTML template layout.

## Description
Configure static files handling and asset integration using standalone Tailwind CSS CLI, HTMX 2.x, and Alpine.js. Build a global `base.html` containing the responsive navigation bar, active route highlighting, toast/flash message container, and main content block. Create a simple home page view at `/` that extends `base.html` and passes view tests.

## Acceptance Criteria
- [ ] `static/` directory configured in Django settings with `STATIC_URL` and `STATICFILES_DIRS`.
- [ ] HTMX 2.x and Alpine.js 3.x loaded via static files or reliable CDN in `templates/base.html`.
- [ ] Tailwind CSS configured (via standalone CLI or Tailwind package) with input and output CSS files.
- [ ] `templates/base.html` contains:
  - HTML5 document shell with responsive `<meta name="viewport">`
  - Top navigation bar with app logo/brand `tailr`, and links to "Data Bank" and "Applications"
  - Flash message / alert notification container rendering Django `messages`
  - `{% block content %}{% endblock %}` block
- [ ] Home view at `/` renders `templates/home.html` extending `base.html`.
- [ ] `uv run pytest tests/test_home.py` verifies:
  - `GET /` returns status code `200`.
  - Response contains `<title>tailr</title>` and expected navigation elements.
  - Static CSS/JS tags are present in the response body.

## Out of Scope
- Real-time SSE streaming components (covered in [#17](https://github.com/1Elral4/tailr/issues/17) and [#18](https://github.com/1Elral4/tailr/issues/18)).
- Specific feature views or forms (covered in [#5](https://github.com/1Elral4/tailr/issues/5) and [#9](https://github.com/1Elral4/tailr/issues/9)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 3. Define Raw Data Bank Database Models and Migrations
## Goal
Create the database model and migrations for storing structured work history, accomplishments, and skills.

## Description
Implement the `DataBankEntry` model to hold raw career records (roles, projects, achievements, education) with structured metadata and JSON fields for metrics and tags. Add model constraints, custom query methods, and database indexes for efficient tag and category filtering. Create migrations and unit tests asserting model validation, serialization, and edge cases.

## Acceptance Criteria
- [ ] `DataBankEntry` model defined in `core/models.py` with fields:
  - `entry_type`: Choice field (`role`, `project`, `achievement`, `education`, `certification`, `other`)
  - `title`: CharField (max 255)
  - `organization`: CharField (max 255, optional for personal projects)
  - `start_date`: DateField (optional)
  - `end_date`: DateField (optional)
  - `is_current`: BooleanField (default False)
  - `raw_text`: TextField (detailed raw description of responsibilities / actions)
  - `metrics`: JSONField (default list/dict for measurable quantitative outcomes)
  - `tags`: JSONField (default list of strings for skills, industries, tools, seniority)
  - `created_at` and `updated_at`: DateTimeFields with auto timestamps
- [ ] Model validation ensures `end_date >= start_date` when both dates are provided.
- [ ] `__str__` returns a readable summary (e.g. `"[Role] Senior Engineer at Acme Corp"`).
- [ ] SQLite database migrations created and applied via `uv run python manage.py migrate`.
- [ ] `uv run pytest tests/test_databank_models.py` verifies:
  - Creating entries with valid data persists to SQLite.
  - Invalid dates raise a `ValidationError`.
  - JSONField correctly stores and retrieves nested dict/list structures.
  - Querying by `entry_type` or filtering by tag works.

## Out of Scope
- Web UI / CRUD forms for data bank entries (covered in [#5](https://github.com/1Elral4/tailr/issues/5)).
- AI parsing of resumes into data bank entries (covered in [#6](https://github.com/1Elral4/tailr/issues/6)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 4. Configure Django Admin for Data Bank Management
## Goal
Register and customize `DataBankEntry` in the Django Admin for manual record inspection and auditing.

## Description
Configure the Django admin site to provide an intuitive management interface for raw work history entries. Add custom search capabilities across titles, organizations, raw text, and tags, alongside list filters for entry types, current roles, and date ranges. Write automated tests ensuring admin views are accessible to staff users and protected from unauthorized access.

## Acceptance Criteria
- [ ] `DataBankEntry` registered with custom `DataBankEntryAdmin` in `core/admin.py`.
- [ ] `list_display` displays: `title`, `organization`, `entry_type`, `is_current`, `start_date`, `end_date`, `created_at`.
- [ ] `list_filter` allows filtering by: `entry_type`, `is_current`, `created_at`.
- [ ] `search_fields` allows searching in: `title`, `organization`, `raw_text`.
- [ ] Form interface formats `metrics` and `tags` JSON fields cleanly.
- [ ] Superuser / staff access documentation included in README or docs.
- [ ] `uv run pytest tests/test_admin.py` verifies:
  - Anonymous users requesting `/admin/core/databankentry/` are redirected to login (HTTP 302).
  - Authenticated staff users receive HTTP 200 on changelist and changeform views.
  - An entry can be created and saved via the admin interface.

## Out of Scope
- Public / user-facing CRUD views (covered in [#5](https://github.com/1Elral4/tailr/issues/5)).
- Bulk import via admin (covered in [#6](https://github.com/1Elral4/tailr/issues/6)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 5. Implement Raw Data Bank Web Interface (CRUD)
## Goal
Build the user-facing web pages and HTMX components to list, filter, add, edit, and delete data bank entries.

## Description
Create the Data Bank dashboard view at `/databank/` with tag filtering and category grouping. Build responsive forms (or modal drawers) powered by HTMX for creating and updating structured entries with dynamic tag and metric inputs without full page reloads. Write view tests covering successful operations, form validation errors, and empty states.

## Acceptance Criteria
- [ ] Data bank index view `/databank/` lists all entries categorized by `entry_type` with tag filter buttons.
- [ ] Empty state renders a friendly message and "Add Your First Entry" button when no entries exist.
- [ ] "Add Entry" form (`/databank/add/`) allows entering title, organization, dates, current toggle, raw text, metrics, and tags.
- [ ] Edit view (`/databank/<id>/edit/`) allows updating existing entry fields and swaps the updated item via HTMX.
- [ ] Delete endpoint (`/databank/<id>/delete/`) prompts for confirmation and removes the item from the list via HTMX swap.
- [ ] Invalid form submissions return HTTP 422 or 200 with inline validation errors highlighted.
- [ ] `uv run pytest tests/test_databank_views.py` verifies:
  - `GET /databank/` returns 200 and lists existing entries.
  - `POST /databank/add/` creates an entry and returns the rendered partial.
  - `POST /databank/<id>/edit/` updates fields and persists changes.
  - `POST /databank/<id>/delete/` deletes the record from the database.

## Out of Scope
- File upload / automatic CV resume parsing (covered in [#6](https://github.com/1Elral4/tailr/issues/6)).
- Automated completeness audit of the data bank (covered in [#7](https://github.com/1Elral4/tailr/issues/7)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 6. Implement CV Document Parser for Data Bank Ingestion
## Goal
Extract and parse work history entries from uploaded PDF and DOCX CVs into structured DataBank candidates.

## Description
Build a resume ingestion service using `pdfplumber` for PDFs and `python-docx` for DOCX files to extract raw textual sections. Use Claude 3.5 Haiku / Sonnet with a strict Pydantic model to parse raw resume text into candidate `DataBankEntry` objects. Provide an ingestion UI at `/databank/import/` allowing users to upload a file, review the extracted entries, select items to keep, and save them to the database.

## Acceptance Criteria
- [ ] File extractor module parses text from `.pdf` and `.docx` uploads, handling multi-page layouts cleanly.
- [ ] Pydantic schema `ResumeParseResult` defined representing a list of structured entry candidates (`entry_type`, `title`, `organization`, dates, `raw_text`, `metrics`, `tags`).
- [ ] Anthropic parsing agent converts extracted text into validated `ResumeParseResult`.
- [ ] Import view `/databank/import/` provides:
  - Drag-and-drop file upload zone accepting `.pdf` and `.docx` files up to 10MB.
  - Rejection of invalid file types (e.g. `.exe`, `.png`) with descriptive error messages.
  - Review step showing extracted items with checkboxes to select which entries to import.
  - "Import Selected" action that creates `DataBankEntry` records in bulk.
- [ ] `uv run pytest tests/test_importer.py` verifies:
  - Text extraction from mock PDF and DOCX fixture files.
  - Pydantic schema validation for valid and malformed LLM responses.
  - Bulk creation of `DataBankEntry` instances from parsed selections.

## Out of Scope
- CV export / generation (covered in [#20](https://github.com/1Elral4/tailr/issues/20) and [#21](https://github.com/1Elral4/tailr/issues/21)).
- Job application tailoring (covered in [#10](https://github.com/1Elral4/tailr/issues/10)-[#17](https://github.com/1Elral4/tailr/issues/17)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 7. Implement Standalone Data Bank Completeness Audit
## Goal
Analyze the user's raw data bank entries with an AI agent to flag gaps, missing metrics, and weak bullet points.

## Description
Create an on-demand audit service that sends the active collection of `DataBankEntry` records to Claude with a structured evaluation rubric. The agent detects missing quantitative metrics, unaddressed career transitions, repetitive phrasing, and generic descriptions. Build an audit report page at `/databank/audit/` displaying the completeness score, categorized flags, and actionable recommendations.

## Acceptance Criteria
- [ ] Audit service compiles all user data bank entries into a structured prompt.
- [ ] Pydantic schema `DataBankAuditReport` defined with fields:
  - `overall_score`: Integer (0-100)
  - `summary`: String summary of data bank health
  - `missing_metrics_flags`: List of entries lacking measurable outcomes with specific suggestions
  - `coverage_gaps`: List of under-detailed skills or roles
  - `repetition_flags`: List of repetitive phrases across entries
  - `action_items`: Prioritized checklist of recommendations
- [ ] View at `/databank/audit/` triggers the audit and renders the report cards.
- [ ] Empty data bank state is handled gracefully with a prompt to add entries first before auditing.
- [ ] `uv run pytest tests/test_databank_audit.py` verifies:
  - Audit schema validation against mock Claude outputs.
  - View returns 200 and renders score and categorized flags.
  - Empty data bank returns appropriate user-facing warning without crashing.

## Out of Scope
- Tailoring CV to a specific job post (covered in [#11](https://github.com/1Elral4/tailr/issues/11)-[#16](https://github.com/1Elral4/tailr/issues/16)).
- Automated auto-fixing of bullets without user input (covered in [#25](https://github.com/1Elral4/tailr/issues/25)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 8. Define Job Application, CV Version, and Pipeline Models
## Goal
Implement database models for job application folders, versioned CV drafts, and pipeline analysis notes.

## Description
Create `JobApplication` to store company, role, status, and raw job post text. Implement `CVVersion` to track generated CV content across iterations with version numbers and active flags, and `ApplicationNote` to store recruiter critique points, ATS keyword checks, and fit analyses. Add model methods, relational cascading, and unit tests validating integrity and constraints.

## Acceptance Criteria
- [ ] `JobApplication` model defined in `core/models.py` with fields:
  - `company`: CharField (max 255)
  - `role_title`: CharField (max 255)
  - `job_description`: TextField (pasted job post text)
  - `status`: CharField with choices (`drafted`, `applied`, `interviewing`, `rejected`, `offer`, default `drafted`)
  - `applied_date`: DateField (optional)
  - `created_at` and `updated_at`: DateTimeFields
- [ ] `CVVersion` model defined with fields:
  - `application`: ForeignKey to `JobApplication` (related_name `cv_versions`, on_delete CASCADE)
  - `version_number`: PositiveIntegerField
  - `content_json`: JSONField (structured sections: summary, experience, skills, education)
  - `content_markdown`: TextField (rendered markdown representation)
  - `is_current`: BooleanField (default True)
  - `created_at`: DateTimeField
- [ ] `ApplicationNote` model defined with fields:
  - `application`: ForeignKey to `JobApplication` (related_name `notes`, on_delete CASCADE)
  - `note_type`: Choice field (`recruiter_critique`, `ats_filter`, `match_analysis`, `sufficiency_check`, `general`)
  - `content_json`: JSONField (structured payload)
  - `content_markdown`: TextField (human-readable formatted text)
  - `created_at`: DateTimeField
- [ ] Unique constraint on `('application', 'version_number')` in `CVVersion`.
- [ ] SQLite database migrations created and applied.
- [ ] `uv run pytest tests/test_application_models.py` verifies:
  - Model creation, foreign key relationships, and cascade deletion.
  - `CVVersion.get_current()` helper returns the active version.
  - Incrementing version numbers on new version creation.

## Out of Scope
- Application folder UI views (covered in [#9](https://github.com/1Elral4/tailr/issues/9)).
- Pipeline execution engine (covered in [#17](https://github.com/1Elral4/tailr/issues/17)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 9. Implement Job Application Folders Management UI
## Goal
Build the user interface to create, list, and open job application folders.

## Description
Build the main applications dashboard view at `/applications/` displaying all job folders with metadata and status badges. Create a "New Application" modal/page at `/applications/new/` where users input the company name, role title, and paste the job description text. Build the application workspace shell at `/applications/<id>/` and write comprehensive view tests.

## Acceptance Criteria
- [ ] Dashboard at `/applications/` displays all job applications as cards with company, role, date created, and status badge.
- [ ] Empty state renders a helpful prompt with a "Create First Application" button.
- [ ] Create view `/applications/new/` includes:
  - Inputs for `company` (required), `role_title` (required), and `job_description` (required, multiline textarea).
  - Validation ensuring none of the three fields are blank or whitespace-only.
  - On submit, redirects to `/applications/<id>/`.
- [ ] Application workspace at `/applications/<id>/` displays:
  - Header with company name, role title, status badge, and "Run Tailr Pipeline" button.
  - Collapsible section showing the full pasted job description.
  - Placeholder tabs for "CV Draft", "Recruiter Critique", "ATS Check", and "Match Analysis".
- [ ] `uv run pytest tests/test_application_views.py` verifies:
  - `GET /applications/` returns 200 and lists applications.
  - `POST /applications/new/` with valid data creates the record and redirects.
  - `POST /applications/new/` with empty fields returns form validation errors (HTTP 422/200).
  - `GET /applications/<invalid-id>/` returns HTTP 404.

## Out of Scope
- Running the multi-step AI pipeline (covered in [#17](https://github.com/1Elral4/tailr/issues/17) and [#18](https://github.com/1Elral4/tailr/issues/18)).
- Inline editing of generated CVs (covered in [#19](https://github.com/1Elral4/tailr/issues/19)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 10. Implement AI Pipeline Infrastructure and Anthropic Client Setup
## Goal
Establish the Anthropic API client wrapper, Pydantic base models, and structured prompt execution harness.

## Description
Create an AI client module in `core/ai/` that initializes the Anthropic Python SDK using `ANTHROPIC_API_KEY`. Implement a robust wrapper function `call_claude_structured()` that accepts system prompts, user prompts, Pydantic response models, and model tier (Sonnet vs. Haiku) with exponential backoff and rate-limit handling. Write unit tests using mocked Anthropic API responses to verify schema parsing, error logging, and retry mechanisms.

## Acceptance Criteria
- [ ] Anthropic client singleton initialized in `core/ai/client.py` reading `ANTHROPIC_API_KEY` from settings/environment.
- [ ] Clear `ConfigurationError` raised with user instructions if `ANTHROPIC_API_KEY` is missing or invalid.
- [ ] `call_claude_structured(prompt, system_prompt, response_model, model_name)` executes structured output tool-calling or JSON schema extraction.
- [ ] Function supports model selection (`claude-3-7-sonnet-20250219`, `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`).
- [ ] Handles rate limits (`RateLimitError`) and network failures with retry attempts before raising a clean application exception.
- [ ] `uv run pytest tests/test_ai_client.py` verifies:
  - Successful structured parsing when Claude returns valid JSON matching a test Pydantic model.
  - Proper retry execution when API returns 429/500 errors.
  - Graceful exception raised when response fails schema validation.

## Out of Scope
- Specific prompt engineering for Steps 0–5 (covered in [#11](https://github.com/1Elral4/tailr/issues/11)–[#16](https://github.com/1Elral4/tailr/issues/16)).
- Django view integration / SSE streaming (covered in [#17](https://github.com/1Elral4/tailr/issues/17)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 11. Implement Pipeline Step 0: Data Sufficiency Check Agent
## Goal
Build the Step 0 agent to check if the user's data bank has enough experience to pursue a given job post.

## Description
Implement the Step 0 agent function that compares the target job requirements against the user's active `DataBankEntry` records using Claude 3.5 Haiku. The agent evaluates whether there is sufficient raw material to craft an honest, competitive CV without hallucination or extreme padding. If material is insufficient, it stops the pipeline and surfaces specific missing skills and experiences for the user to add.

## Acceptance Criteria
- [ ] Pydantic schema `DataSufficiencyResult` defined with fields:
  - `is_sufficient`: Boolean (`True` if enough data exists to draft a credible CV, `False` if critically deficient)
  - `confidence_score`: Float (0.0 to 1.0)
  - `key_requirements_found`: List of strings (requirements well supported in data bank)
  - `missing_critical_requirements`: List of strings (must-have skills/roles completely absent)
  - `recommendation_message`: Human-readable summary for the user
- [ ] Agent prompt instructs Claude 3.5 Haiku to act as an objective intake assessor, strictly disallowing fabricated assumptions.
- [ ] Function `check_data_sufficiency(job_description, databank_entries)` returns a validated `DataSufficiencyResult`.
- [ ] `uv run pytest tests/test_pipeline_step0.py` verifies:
  - Mock sufficient work history returns `is_sufficient=True` and populated `key_requirements_found`.
  - Mock sparse/unrelated work history returns `is_sufficient=False` with `missing_critical_requirements`.
  - Empty data bank returns `is_sufficient=False` with actionable recommendation.

## Out of Scope
- Drafting the CV bullets (covered in [#12](https://github.com/1Elral4/tailr/issues/12)).
- Recruiter critique and ATS filtering (covered in [#13](https://github.com/1Elral4/tailr/issues/13) and [#14](https://github.com/1Elral4/tailr/issues/14)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 12. Implement Pipeline Step 1: XYZ Bullet Drafter Agent
## Goal
Build the Step 1 agent to draft tailored experience bullets formatted strictly in Google XYZ style.

## Description
Implement the Step 1 agent function that extracts relevant work history items and writes tailored resume bullets following the XYZ format ("Accomplished [X], measured by [Y], by doing [Z]"). The prompt strictly forbids fabricating facts, metrics, or technologies not present in the raw data bank. Write unit tests validating output structure and schema conformity.

## Acceptance Criteria
- [ ] Pydantic schema `CVDraft` defined containing:
  - `full_name`, `contact_info` (phone, email, links)
  - `summary`: Short tailored professional summary (2-3 sentences)
  - `experiences`: List of experience blocks (`company`, `role`, `dates`, `bullets` list of XYZ strings)
  - `skills`: Categorized dictionary or list of skills aligned to the job
  - `education`: List of education blocks
- [ ] Agent prompt for Claude Sonnet enforces:
  - Strict XYZ bullet syntax ("Accomplished [X], measured by [Y], by doing [Z]").
  - Zero fabrication or hallucinated statistics.
  - Elimination of passive filler words (e.g. "Responsible for", "Assisted with").
- [ ] Function `draft_cv(job_description, databank_entries)` returns a validated `CVDraft`.
- [ ] `uv run pytest tests/test_pipeline_step1.py` verifies:
  - Output validates against `CVDraft` schema on sample inputs.
  - Bullets contain action verbs and measurable metrics from mock data bank entries.

## Out of Scope
- Recruiter critique (covered in [#13](https://github.com/1Elral4/tailr/issues/13)).
- Revisions based on critique (covered in [#15](https://github.com/1Elral4/tailr/issues/15)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 13. Implement Pipeline Step 2: Skeptical Senior Recruiter Agent
## Goal
Build the Step 2 agent simulating a strict recruiter scan to identify exactly three reasons for rejection.

## Description
Implement the Step 2 agent simulating a skeptical senior recruiter performing a rapid 10-second resume screening using Claude Sonnet. The agent critically reviews the draft CV from Step 1 against the target job post and returns strictly three specific, actionable reasons why the candidate would be rejected or deprioritized. Write tests asserting exact output schema constraints.

## Acceptance Criteria
- [ ] Pydantic schema `RecruiterCritique` defined with fields:
  - `critique_points`: List of exactly 3 critique items, each containing:
    - `title`: Short punchy title (e.g., "Lack of demonstrated scale in distributed systems")
    - `severity`: Choice (`high`, `medium`)
    - `explanation`: 2-3 sentence recruiter observation
    - `actionable_fix`: Specific guidance on what to emphasize or clarify
  - `first_impression_score`: Integer (1-10)
  - `summary`: One-paragraph brutal honest take
- [ ] Agent prompt instructs Claude Sonnet to be brutally realistic, not encouraging or soft.
- [ ] Validation enforces `len(critique_points) == 3`.
- [ ] Function `critique_cv_draft(job_description, cv_draft)` returns a validated `RecruiterCritique`.
- [ ] `uv run pytest tests/test_pipeline_step2.py` verifies:
  - Returned critique contains exactly 3 items.
  - Schema validation fails if fewer or more than 3 critique points are returned.

## Out of Scope
- Applying fixes to the draft (covered in [#15](https://github.com/1Elral4/tailr/issues/15)).
- ATS keyword matching (covered in [#14](https://github.com/1Elral4/tailr/issues/14)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 14. Implement Pipeline Step 3: ATS Keyword Filter Agent
## Goal
Build the Step 3 agent to extract job keywords, check draft coverage, and flag ATS formatting risks.

## Description
Implement the Step 3 agent using Claude 3.5 Haiku to extract critical hard skills, tool names, required certifications, and exact phrasing from the job post. The agent scans the Step 1 draft CV to identify matched keywords, missing keywords, and any risky formatting patterns. Write tests verifying keyword extraction accuracy and match score computation.

## Acceptance Criteria
- [ ] Pydantic schema `ATSScreenResult` defined with fields:
  - `matched_keywords`: List of terms found in both job post and CV draft
  - `missing_keywords`: List of required job post terms absent from CV draft
  - `match_percentage`: Float (0.0 to 100.0)
  - `formatting_risks`: List of flagged formatting/readability issues (e.g., non-standard section headers, overly dense text)
  - `keyword_density_assessment`: Short evaluation of keyword naturalness vs stuffing
- [ ] Function `screen_ats_keywords(job_description, cv_draft)` returns a validated `ATSScreenResult`.
- [ ] `uv run pytest tests/test_pipeline_step3.py` verifies:
  - Extraction of keywords from sample job posts.
  - Correct calculation of matched vs missing keywords and percentage score.
  - Detection of missing critical skills from a mock CV draft.

## Out of Scope
- Automatic injection of missing keywords into the draft (covered in [#15](https://github.com/1Elral4/tailr/issues/15)).
- Overall match analysis tier (covered in [#16](https://github.com/1Elral4/tailr/issues/16)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 15. Implement Pipeline Step 4: CV Reviser Agent
## Goal
Build the Step 4 agent to polish and revise the draft CV using recruiter critiques and ATS keyword findings.

## Description
Implement the Step 4 reviser agent using Claude Sonnet to take the Step 1 draft CV, Step 2 recruiter critiques, and Step 3 ATS keyword results to produce a polished final CV draft. The reviser resolves recruiter concerns and integrates missing keywords only if they can be honestly backed by raw data bank entries, explicitly listing any unclosable gaps. Write tests validating revised schema adherence and unresolvable gap tracking.

## Acceptance Criteria
- [ ] Pydantic schema `RevisedCVDraft` defined containing:
  - `cv`: Validated `CVDraft` (revised summary, experiences, skills, education)
  - `revisions_applied`: List of specific changes made in response to Steps 2 & 3
  - `unresolvable_gaps`: List of missing requirements or critiques that could NOT be honestly closed from raw data
- [ ] Agent prompt instructs Claude Sonnet to:
  - Address the 3 recruiter critique points directly.
  - Naturally weave in missing ATS keywords where supported by raw data facts.
  - NEVER fabricate accomplishments to satisfy a critique.
  - Document every honest gap that could not be resolved.
- [ ] Function `revise_cv(cv_draft, recruiter_critique, ats_result, databank_entries)` returns a validated `RevisedCVDraft`.
- [ ] `uv run pytest tests/test_pipeline_step4.py` verifies:
  - Revised CV structure conforms to `CVDraft` schema.
  - `unresolvable_gaps` is populated when mock raw data lacks required skills.
  - `revisions_applied` records changes made.

## Out of Scope
- Overall fit rating synthesis (covered in [#16](https://github.com/1Elral4/tailr/issues/16)).
- Document file rendering / PDF export (covered in [#20](https://github.com/1Elral4/tailr/issues/20) and [#21](https://github.com/1Elral4/tailr/issues/21)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 16. Implement Pipeline Step 5: Match Analysis Agent
## Goal
Build the Step 5 agent to produce the final overall job match score, fit tier, and keyword coverage summary.

## Description
Implement the Step 5 match analysis agent using Claude Sonnet to synthesize the final revised CV, ATS score, and remaining gaps into an executive summary of candidate fit. The agent assigns a fit tier (`Strong Fit`, `Good Fit`, `Reach Role`) with a detailed breakdown of strengths, risks, and interview talking points. Write tests asserting correct schema generation and persistence as an `ApplicationNote`.

## Acceptance Criteria
- [ ] Pydantic schema `MatchAnalysisReport` defined with fields:
  - `fit_tier`: Choice (`strong_fit`, `good_fit`, `reach_role`)
  - `overall_match_score`: Integer (1 to 100)
  - `executive_summary`: 2-3 paragraph breakdown of candidate competitiveness
  - `key_strengths`: List of top competitive advantages
  - `remaining_risks`: List of potential interviewer concerns
  - `talking_points`: Recommended interview angles to proactively address experience gaps
- [ ] Function `generate_match_analysis(job_description, revised_cv, ats_result, unresolvable_gaps)` returns a validated `MatchAnalysisReport`.
- [ ] Output is serialized and persisted as an `ApplicationNote` with `note_type='match_analysis'` linked to the `JobApplication`.
- [ ] `uv run pytest tests/test_pipeline_step5.py` verifies:
  - Score and fit tier generation across strong and reach candidate test fixtures.
  - Persistence of `ApplicationNote` record with valid JSON and markdown fields.

## Out of Scope
- SSE real-time event publishing (covered in [#17](https://github.com/1Elral4/tailr/issues/17)).
- User-facing UI tabs (covered in [#18](https://github.com/1Elral4/tailr/issues/18)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 17. Implement Pipeline Orchestrator with Real-Time SSE Streaming
## Goal
Orchestrate Steps 0 through 5 sequentially in a Django streaming view emitting real-time Server-Sent Events.

## Description
Build the backend pipeline runner that coordinates Steps 0 to 5 for a `JobApplication`. Implement an async or generator-based view at `/applications/<id>/run-pipeline/` using `StreamingHttpResponse` to push SSE event packets (`step_start`, `step_complete`, `pipeline_finish`, `error`) as each agent finishes. Save intermediate results (`CVVersion`, `ApplicationNote`) to SQLite and handle early exits if Step 0 reports insufficient data.

## Acceptance Criteria
- [ ] Pipeline orchestrator module `core/ai/orchestrator.py` executes:
  - Step 0 (Sufficiency) $\rightarrow$ If insufficient, halts and emits early-exit SSE event.
  - Step 1 (Drafter) $\rightarrow$ Saves initial draft.
  - Step 2 (Recruiter) $\rightarrow$ Saves `ApplicationNote(note_type='recruiter_critique')`.
  - Step 3 (ATS Filter) $\rightarrow$ Saves `ApplicationNote(note_type='ats_filter')`.
  - Step 4 (Reviser) $\rightarrow$ Creates new `CVVersion` marked current.
  - Step 5 (Match Analysis) $\rightarrow$ Saves `ApplicationNote(note_type='match_analysis')`.
- [ ] Endpoint `POST /applications/<id>/run-pipeline/` returns `StreamingHttpResponse` with `content_type='text/event-stream'`.
- [ ] SSE event format adheres to standard `event: <name>\ndata: <json>\n\n`.
- [ ] Exceptions during pipeline execution yield an `error` SSE event with a safe user message and log traceback on server.
- [ ] `uv run pytest tests/test_pipeline_orchestrator.py` verifies:
  - Mocked full pipeline execution stream yields events in correct order (0 through 5).
  - Database records (`CVVersion`, `ApplicationNote`) are created after run.
  - Insufficient data triggers early completion event without running Steps 1–5.

## Out of Scope
- Frontend DOM event listeners and CSS animations (covered in [#18](https://github.com/1Elral4/tailr/issues/18)).
- Manual hand-editing of the CV (covered in [#19](https://github.com/1Elral4/tailr/issues/19)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 18. Implement Live Agent Progress and Application Workspace UI
## Goal
Build the interactive application workspace with live HTMX SSE pipeline progress cards and tabbed outputs.

## Description
Update the application workspace template at `/applications/<id>/` to connect to the SSE streaming endpoint via the HTMX SSE extension. Render dynamic progress cards for Steps 0–5 showing pending, active (animated pulse/spinner), and completed states. When the pipeline finishes, dynamically reveal and populate tabs for "Tailored CV", "Recruiter Critique (3 Reasons)", "ATS Keyword Breakdown", and "Match Analysis".

## Acceptance Criteria
- [ ] "Run Tailr Pipeline" button initiates SSE connection via `hx-ext="sse"`.
- [ ] Visual step cards for Steps 0 through 5 update dynamically based on received SSE events:
  - Pending: Muted badge with step name
  - Running: Active blue/indigo badge with spinning indicator
  - Completed: Green checkmark with summary metric (e.g., "ATS: 91%", "Recruiter: 3 issues identified")
  - Insufficient/Failed: Yellow/Red alert card with details
- [ ] On completion, tabs become active and populated:
  - Tab 1: **Tailored CV** (rendered clean single-column view)
  - Tab 2: **Recruiter Critique** (3 rejection reasons with severity tags)
  - Tab 3: **ATS Keywords** (matched/missing badges and match score)
  - Tab 4: **Match Analysis** (fit tier badge and executive summary)
- [ ] Works cleanly on browser refresh by loading persisted `CVVersion` and `ApplicationNote` records.
- [ ] `uv run pytest tests/test_workspace_ui.py` verifies:
  - Workspace template renders SSE triggers and step card containers.
  - Detail view returns 200 with persisted versions and notes displayed in correct tabs.

## Out of Scope
- In-browser CV text editing (covered in [#19](https://github.com/1Elral4/tailr/issues/19)).
- File exports (covered in [#20](https://github.com/1Elral4/tailr/issues/20), [#21](https://github.com/1Elral4/tailr/issues/21), [#22](https://github.com/1Elral4/tailr/issues/22)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 19. Implement CV Draft In-Browser Editor and Versioning
## Goal
Build an in-browser editor allowing users to hand-edit the generated CV and save new version snapshots.

## Description
Add an editable mode or structured form to the "Tailored CV" tab in the application workspace. When users modify summary, bullet points, or skills and save, create a new `CVVersion` record incrementing `version_number` while preserving previous versions in history. Include a version selector dropdown to view, compare, or restore prior drafts.

## Acceptance Criteria
- [ ] "Edit CV" button toggles interactive editing mode for summary, experience bullets, and skills.
- [ ] "Save Changes" endpoint `POST /applications/<id>/versions/` saves the edited content as a new `CVVersion` with `version_number = latest + 1` and `is_current = True`.
- [ ] Previous version's `is_current` is set to `False`.
- [ ] Version history dropdown lists all versions (e.g. "v1 (AI Revised)", "v2 (User Edited)") and switches active display.
- [ ] `uv run pytest tests/test_cv_editor.py` verifies:
  - `POST` creates a new `CVVersion` and updates `is_current`.
  - Version history accurately displays all historical drafts.
  - Invalid/empty content returns form validation error without creating a corrupt version.

## Out of Scope
- DOCX/PDF export functionality (covered in [#20](https://github.com/1Elral4/tailr/issues/20) and [#21](https://github.com/1Elral4/tailr/issues/21)).
- Notes editing (covered in [#22](https://github.com/1Elral4/tailr/issues/22)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 20. Implement ATS-Safe DOCX Document Export
## Goal
Generate clean, single-column Microsoft Word (.docx) documents from a CV version.

## Description
Create a document generation service in `core/export/docx.py` using `python-docx` that converts a `CVVersion` into a professional, ATS-safe Word file. Ensure the document uses standard typography, single-column linear layout, standard section headings (`Summary`, `Experience`, `Education`, `Skills`), and zero tables, text boxes, or floating elements. Provide a download endpoint in the workspace.

## Acceptance Criteria
- [ ] `generate_docx_cv(cv_version)` produces a valid `.docx` binary stream adhering to ATS rules:
  - Single-column standard page layout with 0.75" margins.
  - Standard headings (`SUMMARY`, `PROFESSIONAL EXPERIENCE`, `EDUCATION`, `SKILLS`).
  - Clean bullet lists without nested tables or graphic shapes.
  - Standard fonts (e.g. Calibri, Arial, or Times New Roman).
- [ ] Download endpoint `GET /applications/<id>/export/docx/` returns:
  - HTTP status 200 with binary payload.
  - Header `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
  - Header `Content-Disposition: attachment; filename="<Candidate>_<Company>_CV.docx"`.
- [ ] If application has no `CVVersion`, returns 404 or redirect with warning message.
- [ ] `uv run pytest tests/test_export_docx.py` verifies:
  - Generation of non-empty binary stream.
  - Valid docx structure parsable by `python-docx` asserting expected paragraphs and text.
  - Correct HTTP headers returned by download view.

## Out of Scope
- PDF document export (covered in [#21](https://github.com/1Elral4/tailr/issues/21)).
- Notes export (covered in [#22](https://github.com/1Elral4/tailr/issues/22)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 21. Implement ATS-Safe PDF Document Export
## Goal
Generate standard, selectable-text PDF resumes from a CV version.

## Description
Create a clean, single-column HTML/CSS print template strictly optimized for ATS compliance (selectable text, standard headers, no multi-column layouts) and convert it to PDF using `WeasyPrint` or headless Chrome. Build a download endpoint `GET /applications/<id>/export/pdf/` that streams the generated PDF to the client. Write tests verifying PDF creation, selectable text layer, and response headers.

## Acceptance Criteria
- [ ] Clean HTML/CSS print template `templates/export/cv_pdf.html` created with single-column layout, standard typography, and clean margin rules (`@page { margin: 0.75in; }`).
- [ ] PDF generator function `generate_pdf_cv(cv_version)` renders template to PDF binary.
- [ ] Generated PDF contains fully selectable, extractable text without image-flattened text.
- [ ] Download endpoint `GET /applications/<id>/export/pdf/` returns:
  - HTTP status 200.
  - Header `Content-Type: application/pdf`.
  - Header `Content-Disposition: attachment; filename="<Candidate>_<Company>_CV.pdf"`.
- [ ] `uv run pytest tests/test_export_pdf.py` verifies:
  - Successful PDF compilation from mock `CVVersion`.
  - Generated file starts with `%PDF-` magic bytes.
  - Text extracted from generated PDF matches candidate name and experience text.

## Out of Scope
- DOCX export (covered in [#20](https://github.com/1Elral4/tailr/issues/20)).
- Exporting recruiter notes (covered in [#22](https://github.com/1Elral4/tailr/issues/22)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 22. Implement Notes and Recruiter Critique File Exporters (.md / .txt)
## Goal
Allow users to export recruiter critiques, ATS keyword analyses, and match reports as separate `.md` and `.txt` files.

## Description
Create export utilities and endpoints that compile all `ApplicationNote` records for a job into organized Markdown and plain text documents. Ensure notes remain strictly isolated from the CV file to preserve ATS cleanliness while giving the candidate a portable interview preparation guide. Write tests verifying document formatting, completeness, and download delivery.

## Acceptance Criteria
- [ ] Exporter module formats all notes into structured Markdown and plain text sections:
  - Section 1: Executive Match Summary & Fit Tier
  - Section 2: Skeptical Recruiter Critique (Top 3 Rejection Reasons & Fixes)
  - Section 3: ATS Keyword Coverage (Matched & Missing Keywords)
  - Section 4: Identified Gaps & Interview Talking Points
- [ ] Download endpoints created:
  - `GET /applications/<id>/export/notes/md/` (`Content-Type: text/markdown`)
  - `GET /applications/<id>/export/notes/txt/` (`Content-Type: text/plain`)
- [ ] Downloaded file names formatted as `<Candidate>_<Company>_Notes.md` and `.txt`.
- [ ] `uv run pytest tests/test_export_notes.py` verifies:
  - Exported text contains all 4 sections with complete content from `ApplicationNote` entries.
  - Endpoints return HTTP 200 with valid content types and attachment headers.

## Out of Scope
- Merging notes into the CV document (explicitly disallowed by product architecture).
- Exporting cover letters (covered in [#24](https://github.com/1Elral4/tailr/issues/24)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 23. Implement Application Status Tracking and Search Filters
## Goal
Enable users to track application status progression and filter applications on the dashboard.

## Description
Add UI controls to update a job application's status (`Drafted`, `Applied`, `Interviewing`, `Rejected`, `Offer`) and record applied/outcome dates. Enhance the main applications dashboard with instant HTMX-powered search by company/role and filtering by status chips. Write unit and view tests verifying status updates, date validations, and search query filters.

## Acceptance Criteria
- [ ] Status dropdown selector on application workspace updates `status` via HTMX `POST /applications/<id>/status/`.
- [ ] When status changes to `Applied`, `applied_date` automatically defaults to today's date if not already set.
- [ ] Main dashboard `/applications/` provides:
  - Live search input filtering by company name or role title.
  - Filter chips for status (`All`, `Drafted`, `Applied`, `Interviewing`, `Rejected`, `Offer`) with record counts.
  - Sorting by date created or last updated.
- [ ] `uv run pytest tests/test_application_tracking.py` verifies:
  - Status update endpoint updates record in SQLite and returns updated badge partial.
  - Querying dashboard with `?search=Acme` returns only matching company records.
  - Querying dashboard with `?status=interviewing` returns only interviewing records.

## Out of Scope
- Email notification integrations (covered in [#29](https://github.com/1Elral4/tailr/issues/29)) or calendar sync (covered in [#30](https://github.com/1Elral4/tailr/issues/30)).
- External job board imports (covered in [#28](https://github.com/1Elral4/tailr/issues/28)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.

---

## 24. Implement Optional Tailored Cover Letter Generator
## Goal
Add an optional toggle and agent to generate a tailored cover letter matching the target role.

## Description
Build an optional cover letter agent using Claude Sonnet that analyzes the job post's mission/tone and pulls relevant career narratives from the user's data bank. In the application workspace, provide a toggle to generate a cover letter, display it in a dedicated "Cover Letter" tab, and allow in-browser editing and PDF/DOCX downloads. Write tests validating generation, editing, and export handling.

## Acceptance Criteria
- [ ] Pydantic schema `CoverLetter` defined with fields: `recipient_name`, `company_name`, `salutation`, `paragraphs` (list of strings), `sign_off`.
- [ ] Agent prompt instructs Claude Sonnet to craft a concise, compelling cover letter (3-4 paragraphs) bridging user background to company needs without generic clichés.
- [ ] Workspace includes a "Generate Cover Letter" action in a dedicated tab.
- [ ] Cover letter tab allows editing text and exporting as `.docx`, `.pdf`, and `.txt`.
- [ ] If not generated, tab displays a clean empty state with a "Generate Cover Letter" button.
- [ ] `uv run pytest tests/test_cover_letter.py` verifies:
  - Cover letter generation from mock data bank entries and job description.
  - View endpoints for generating, updating, and exporting cover letters return HTTP 200.

## Out of Scope
- Automated cover letter sending via email (covered in [#26](https://github.com/1Elral4/tailr/issues/26)).
- Multi-language translation (covered in [#27](https://github.com/1Elral4/tailr/issues/27)).

## Constraints
- Keep the application local-first and self-contained; add no external dependency beyond a library or service explicitly named in this issue.
- Follow the existing Django, SQLite, and `uv` project conventions.
- Add or update the specified automated tests, and ensure `uv run pytest` passes.
