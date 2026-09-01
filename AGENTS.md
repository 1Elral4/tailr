# Agent Guidelines & Workflow

## Commands

- `uv sync` - install dependencies
- `uv run pytest` - run the whole test suite
- `uv run pytest tests/test_home.py` - run a single test file

## Rules

- Work on tasks as defined in GitHub issues, strictly one at a time.
- Always read and verify the task's **Acceptance Criteria** before starting implementation and before marking an issue complete.
- Ensure all tests pass (`uv run pytest`) before completing any task.
- Follow a test-driven or test-verified approach for all new features and bugfixes.
- Commit regularly with clear, descriptive commit messages and push to `main`.
- Keep the application local-first and self-contained; do not introduce external cloud service dependencies.
