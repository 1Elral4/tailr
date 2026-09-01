  
Roles

- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
- Engineer - implements one groomed task, follows _docs/team/software-engineer.md
- QA - checks the result against the acceptance criteria, follows _docs/team/qa-engineer.md


Orchestrator

The main session is the orchestrator. It launches the PM, the engineer
and QA as subagents. It does not groom, implement or test itself.

Lifecycle

1. Pick the next open issue from the backlog
2. PM grooms it
3. Engineer implements it
4. QA verifies it
5. On FAIL, back to step 3 with the QA comment as input
6. On PASS, close the issue
7. Repeat until the backlog is empty

Rules

- Do not skip step 2
- The engineer does not close the issue
- QA does not fix the code, only outputs PASS or FAIL
- The orchestrator closes the issue only after QA outputs PASS
- Work on tasks as defined in GitHub issues, strictly one at a time.
- Always read and verify the task's **Acceptance Criteria** before starting implementation and before marking an issue complete.
- Ensure all tests pass (`uv run pytest`) before completing any task.
- Follow a test-driven or test-verified approach for all new features and bugfixes.
- Commit regularly with clear, descriptive commit messages and push to `main`.
- Keep the application local-first and self-contained; do not introduce external cloud service dependencies.