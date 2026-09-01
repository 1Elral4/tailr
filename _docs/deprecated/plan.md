# CV Tailoring Web App — Full Plan

## 1. Vision

A hosted web app that takes a **raw data bank** of the user's full work history and, for each job post they paste in, runs it through a multi-step AI agent pipeline to produce an **ATS-safe, tailored CV** — plus separate supporting notes (recruiter critique, ATS keyword check, match analysis) that live apart from the CV itself.

Applications are organized like folders: one per job, holding the job post, the generated CV, and its notes.

---

## 2. Core Concept

- **Raw Data Bank**: everything the user has ever done — roles, projects, achievements, metrics — tagged by industry/skill/seniority so it can be pulled from for very different job types.
- **Per-application pipeline**: paste a job post → agents check, draft, critique, revise, and analyze → output a polished CV + separate notes.
- **Primary output**: the CV file. **Secondary output**: notes (kept separate, not bundled into the CV document).

---

## 3. Architecture

**Type**: Full coded web app, hosted separately (not a Claude Project or Artifact).

**Rough shape**:
- Frontend: web UI for managing the data bank, job folders, and viewing pipeline output
- Backend: orchestrates the agent pipeline, calls the Claude API for each step
- Database: stores raw data bank entries, job applications, generated CVs, notes, run history
- Auth: required — this is sensitive personal/work history data
- File export: PDF and DOCX generation for the CV; text/markdown export for notes

---

## 4. Raw Data Bank

**Purpose**: single source of truth the agents pull from — not a fixed CV, but comprehensive raw material.

**Requirements**:
- Structured entries (not a single text blob): role, project, achievement, metric, dates, tags (industry, skill type, seniority)
- **Import**: parse an existing CV (PDF/DOCX) to bootstrap entries instead of starting from zero
- **Manual add/edit**: UI forms to add or refine entries over time
- **Standalone Data Bank Audit**: on-demand check of the whole bank for completeness — flags:
  - Coverage gaps (roles/skills mentioned but under-detailed)
  - Missing metrics (accomplishments with no measurable outcome)
  - Repetition without variation (same bullet reused with no alternate phrasing)
  - Unexplained career gaps/transitions
  - Generic, non-specific entries

*(Note: user is currently planning to build the raw data bank / import tooling locally with their own AI + agents — this section may end up as a separate system that feeds into this web app rather than being built inside it. Worth confirming before backend design.)*

---

## 5. Job Application Folders

Each application is a self-contained record:
- Job post (pasted text)
- Company, role title, date, status (drafted / applied / interview / rejected / offer) — optional tracking layer
- Generated CV (with version history across pipeline runs)
- Notes (kept separate from the CV — see Section 7)

This effectively makes the tool a lightweight job-search tracker in addition to a CV generator.

---

## 6. Agent Pipeline

Runs automatically, per application, in this order:

| Step | Agent | Purpose |
|---|---|---|
| 0 | **Data Sufficiency Check** | Compares job post requirements against the raw data bank *before* drafting. If material is thin, stops and tells the user what's missing rather than producing a padded/generic CV. |
| 1 | **Drafter** | Pulls relevant raw material, writes bullets in **XYZ format** ("Accomplished [X], measured by [Y], by doing [Z]"), eliminates generic filler phrases. No fabrication. |
| 2 | **Skeptical Senior Recruiter** | Reviews the draft as a real recruiter would in a 10-second scan. Surfaces exactly **3 honest reasons** it would be rejected or deprioritized. |
| 3 | **ATS Filter** | Extracts key terms from the job post (skills, tools, certifications, exact title phrasing) and checks coverage. Flags formatting risks. |
| 4 | **Reviser** | Fixes the draft based on Steps 2 & 3, using only real raw data. Notes any gap that couldn't be honestly closed. |
| 5 | **Match Analysis** | Summarizes keyword coverage (covered / missing) and gives an overall fit read (strong fit / good fit, light on X / reach role). |

**Optional (toggle per application)**:
- **Cover letter agent** — generates a tailored cover letter alongside the CV, off by default

---

## 7. Output & Export

- **Primary: CV** — clean, single-column, standard section headers, no tables/graphics/icons/text boxes. Exportable as **PDF** and **DOCX**.
- **Secondary: Notes** — recruiter critique, ATS check, match analysis, and any flagged raw-data gaps. Lives in its own section/tab, exportable separately as text/markdown — never merged into the CV document.
- **Editable CV view**: before final export, the user can hand-edit the AI-generated CV rather than only accepting it as-is.
- **Run history**: visibility into what changed between the initial draft and the revised final, per application.

---

## 8. Feature List — MVP vs. Later

*(Priority pending your final confirmation — this is a proposed split based on our discussion.)*

**Core (MVP)**
- Job application folders (job post, CV, notes)
- Full agent pipeline (Steps 0–5)
- CV export as PDF, notes exported separately
- Basic raw data bank storage (even if unstructured to start)

**High-value, likely v1.x**
- Structured raw data bank with tagging + import from existing CV
- Editable CV before export + DOCX export
- Application status tracking (drafted/applied/interview/rejected/offer)

**Later / optional**
- Cover letter agent toggle
- Outcome tracking tied to CV version (which tailored CV led to interviews/offers)
- Standalone Data Bank Audit as a scheduled/recurring check
- Agent prompt versioning/tuning UI
- API usage/cost visibility dashboard

---

## 9. Open Decisions

1. **Scope for v1** — confirm which items from Section 8's "High-value" tier should be pulled into MVP.
2. **Raw data bank ownership** — will it be built and maintained inside this web app, or imported from a separate local system the user is building?
3. **Hosting/stack specifics** — not yet defined (framework, hosting provider, database choice) — next planning step once feature scope is locked.

---

## 10. Next Steps

1. Lock MVP scope (Section 8)
2. Decide raw data bank source (Section 9.2)
3. Move into technical design: stack choice, data model, API call structure for the agent pipeline
