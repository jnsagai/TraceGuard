# TraceGuard Project Guidance

TraceGuard is a deterministic requirements derivation coverage checker for AI-assisted requirements engineering.

Core principle:

> AI proposes. Deterministic rules decide.

Use `traceguard_codex_agent_planning_guideline.md` as the durable product and engineering guideline for this repository. Preserve the deterministic-core design: natural-language requirements are normalized, atomized into canonical structures, linked through explicit trace data, checked by deterministic rules, and emitted as auditable evidence.

At the start of a new chat or after context loss, read `docs/session_handoff_context.md` before making changes. It contains the latest project state, user preferences, generated outputs, and report behavior expectations.

Quality gates before completion:

```bash
py -3.12 -m ruff check .
py -3.12 -m mypy src
py -3.12 -m pytest
```
