# Project Backlog & Task Breakdown — `tailr`

## 1. Initialize Django Project and Base Test Suite
Goal: Set up an empty Django 5 project with environment configuration and a passing automated test.
Description: Create the virtual environment, install core dependencies (Django, pytest-django, python-dotenv), and initialize the Django project structure with a dedicated core app. Configure settings to support local environment variables and SQLite. Write and execute an initial automated smoke test to verify the Django test runner is fully functional.

## 2. Configure Tailwind CSS, HTMX, Alpine.js, and Base Layout
Goal: Establish the frontend asset pipeline and base responsive HTML shell.
Description: Integrate Tailwind CSS (via standalone CLI), HTMX 2.x, and Alpine.js into the Django template hierarchy. Create `base.html` containing the global HTML shell, responsive navigation bar, toast/alert container, and main content block. Add a sample home view and test asserting that the base layout renders with static assets loaded.

## 3. Define Raw Data Bank Database Models and Migrations
Goal: Create the database schema to store structured work history, accomplishments, and metadata.
Description: Implement the `DataBankEntry` model with fields for entry type (role, project, achievement, education), organization, title, start/end dates, raw description, XYZ metrics JSON, and industry/skill tags. Add model validations, string representations, and database indexes for fast tag filtering. Generate and run initial migrations against SQLite, accompanied by unit tests verifying model creation and queries.

## 4. Configure Django Admin for Data Bank Management
Goal: Provide an administrative interface to view, filter, and modify data bank records.
Description: Register `DataBankEntry` with the Django admin site. Customize list displays, search fields (by title, company, tag), and filters (by entry type and date range) to allow easy manual auditing of work history. Verify that admin authentication works locally and test creating entries via the admin interface.

## 5. Implement Raw Data Bank Web Interface (CRUD)
Goal: Build the user-facing web pages to list, add, edit, and delete work history entries.
Description: Create Django views and HTMX-powered templates for listing all data bank entries with tag-based filtering. Implement modal/inline forms for creating and editing structured work history items with dynamic metric fields. Write view tests covering successful creation, validation errors, and deletion of entries.

## 6. Implement CV Document Parser for Data Bank Ingestion
Goal: Extract structured work history entries from uploaded PDF and DOCX resumes.
Description: Create a document ingestion service using `pdfplumber` and `python-docx` to extract raw text and sections from uploaded files. Implement a Claude prompt with Pydantic validation to parse the extracted text into structured `DataBankEntry` candidate objects for user review before saving. Add tests with mock CV documents verifying text extraction and schema parsing.

## 7. Implement Standalone Data Bank Completeness Audit
Goal: Analyze the raw data bank to flag gaps, missing metrics, and weak bullet points.
Description: Build an audit service that sends the full set of user data bank entries to Claude with a structured evaluation schema. The agent flags coverage gaps, achievements missing measurable metrics, repeated phrasing, and unaddressed career transitions. Create an audit dashboard view displaying the findings with actionable improvement recommendations.

## 8. Define Job Application, CV Version, and Pipeline Models
Goal: Create database models to manage job folders, generated CV versions, and agent run notes.
Description: Implement `JobApplication` (company, role title, job description text, status, timestamps), `CVVersion` (linked to application, version number, structured JSON content, raw markdown, is_current flag), and `ApplicationNote` (critiques, ATS match stats, gap notes). Set up foreign keys, cascading rules, and helper methods for retrieving the latest CV draft. Write unit tests validating relationship constraints and version increments.

## 9. Implement Job Application Folders Management UI
Goal: Build the web interface to create, view, and organize job application records.
Description: Implement views and templates for a dashboard displaying all job application folders as cards or table rows. Build a "New Application" form where users paste a job description and enter company and role details. Add view tests verifying folder creation, listing, and redirection to the application workspace.

## 10. Implement AI Pipeline Infrastructure and Anthropic Client Setup
Goal: Set up the Anthropic API client, Pydantic schemas, and pipeline execution harness.
Description: Create a dedicated AI service module that initializes the Anthropic client using `ANTHROPIC_API_KEY` from `.env`. Define standard Pydantic models for structured agent inputs/outputs and helper functions for invoking Claude 3.7 / 3.5 Sonnet and Haiku with error handling and retry logic. Write unit tests with mock API responses to verify schema validation and error handling.

## 11. Implement Pipeline Step 0: Data Sufficiency Check Agent
Goal: Evaluate whether the user's data bank contains enough material for a given job post.
Description: Build the Step 0 agent function that compares the job description requirements against the user's active `DataBankEntry` items using Claude 3.5 Haiku. Return a structured Pydantic result containing a sufficiency status (sufficient / insufficient), missing critical skills, and guidance on what to add. Write tests validating behavior for both sufficient and insufficient data scenarios.

## 12. Implement Pipeline Step 1: XYZ Bullet Drafter Agent
Goal: Draft tailored CV experience bullets formatted strictly in Google XYZ style.
Description: Build the Step 1 agent function that selects relevant data bank items and drafts CV sections with bullets following the "Accomplished [X], measured by [Y], by doing [Z]" format using Claude Sonnet. Ensure prompt constraints strictly prohibit hallucinating metrics or fabricating experience not in the data bank. Write tests verifying that output bullets conform to the structured Pydantic CV draft schema.

## 13. Implement Pipeline Step 2: Skeptical Senior Recruiter Agent
Goal: Critique the initial CV draft and surface exactly three reasons for rejection.
Description: Build the Step 2 agent function simulating a strict senior recruiter performing a 10-second resume scan using Claude Sonnet. The agent outputs exactly three specific, honest critique points explaining why the draft would be deprioritized or rejected for the target role. Write tests asserting the agent output contains exactly three validated critique items.

## 14. Implement Pipeline Step 3: ATS Keyword Filter Agent
Goal: Extract key job requirements and measure keyword coverage against the draft CV.
Description: Build the Step 3 agent function that parses the job description for critical hard skills, tools, domain keywords, and exact phrasing using Claude 3.5 Haiku. Compare these terms against the draft CV to output a list of matched keywords, missing keywords, and formatting risk warnings. Write tests validating keyword extraction and match percentage calculations.

## 15. Implement Pipeline Step 4: CV Reviser Agent
Goal: Revise the draft CV to address recruiter critiques and improve ATS coverage.
Description: Build the Step 4 agent function that takes the initial draft, recruiter critique (Step 2), and ATS keyword analysis (Step 3) to produce an improved, polished CV draft using Claude Sonnet. Ensure the prompt enforces that revisions only draw from verified data bank facts and explicitly notes unresolvable gaps. Write tests validating the revised CV output against the structured schema.

## 16. Implement Pipeline Step 5: Match Analysis Agent
Goal: Generate a final summary of job fit, keyword match stats, and reach assessment.
Description: Build the Step 5 agent function that evaluates the final revised CV against the job description to produce an overall fit rating (Strong Fit, Good Fit, Reach Role) and a structured match summary. Save the output as an `ApplicationNote` record linked to the job application. Write tests asserting correct calculation and persistence of the match summary.

## 17. Implement Pipeline Orchestrator with Real-Time SSE Streaming
Goal: Execute Steps 0 through 5 in sequence and stream real-time progress events to the browser.
Description: Create a Django view and orchestrator service that executes the agent pipeline sequentially for a given `JobApplication`. Use Django's `StreamingHttpResponse` to push Server-Sent Events (SSE) as each step starts and finishes, persisting intermediate results to the database. Write tests verifying end-to-end pipeline execution and stream event structure.

## 18. Implement Live Agent Progress and Application Workspace UI
Goal: Build the interactive application workspace showing real-time agent execution cards.
Description: Create the application detail view utilizing HTMX SSE extensions to subscribe to the pipeline stream. Render dynamic step cards that transition from pending to active (with animated spinners) to completed (with summary badges and checkmarks). Write template and integration tests verifying DOM updates across pipeline event states.

## 19. Implement CV Draft In-Browser Editor and Versioning
Goal: Allow users to review, edit, and save new versions of the generated CV.
Description: Build an in-browser rich text or markdown editor component in the application workspace for the generated CV draft. Implement an auto-save / manual-save endpoint that creates a new `CVVersion` record while preserving the previous AI-generated baseline. Write view tests verifying version creation, history listing, and rollbacks.

## 20. Implement ATS-Safe DOCX Document Export
Goal: Generate clean, single-column Microsoft Word (.docx) files from a CV version.
Description: Build a DOCX generation service using `python-docx` that styles sections (Contact Info, Summary, Experience, Education, Skills) in a single-column layout without tables, text boxes, or headers/footers. Provide a download endpoint in the job workspace that returns the generated `.docx` file with proper MIME headers. Write tests verifying document structure and valid binary file generation.

## 21. Implement ATS-Safe PDF Document Export
Goal: Generate standard, selectable-text PDF resumes from a CV version.
Description: Create a clean HTML/CSS print template strictly optimized for ATS compliance (single column, standard fonts, linear text flow) and convert it to PDF using `WeasyPrint` or headless Chrome. Implement a download endpoint that streams the generated PDF to the client. Write tests verifying that the resulting PDF contains selectable text and matches the expected layout.

## 22. Implement Notes and Recruiter Critique File Exporters (.md / .txt)
Goal: Allow users to export pipeline critique notes, keyword checks, and match reports separately.
Description: Create export endpoints that bundle recruiter critiques, ATS keyword summaries, and match notes into structured Markdown (`.md`) and plain text (`.txt`) files. Ensure notes remain strictly isolated from the CV document. Write tests checking the formatting, completeness, and download delivery of notes files.

## 23. Implement Application Status Tracking and Search Filters
Goal: Enable users to track and filter job applications through hiring stages.
Description: Add UI controls and endpoints to update a job application's status (`Drafted`, `Applied`, `Interviewing`, `Rejected`, `Offer`) with associated dates. Add search and filter controls on the main dashboard to filter applications by status, company name, or date range. Write unit and view tests verifying status transitions and filter queries.

## 24. Implement Optional Tailored Cover Letter Generator
Goal: Add an optional toggle to generate a tailored cover letter matching the target role.
Description: Build an optional cover letter agent step using Claude Sonnet that pulls relevant career narratives from the data bank and aligns them with the job post's tone and mission. Add a toggle in the application workspace to trigger cover letter generation, display the result in a dedicated tab, and export to PDF/DOCX. Write tests validating cover letter generation and export handling.
