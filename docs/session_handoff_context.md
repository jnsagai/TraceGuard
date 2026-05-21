# TraceGuard Session Handoff Context

This file is the first-read context for a new Codex chat working on TraceGuard.

## Project

Project name: TraceGuard

Workspace:

```text
c:\Users\jnsag\Documents\TraceGuard
```

TraceGuard is a deterministic requirements derivation coverage checker for AI-assisted requirements engineering.

Core principle:

> AI proposes. Deterministic rules decide.

## Python and Quality Gates

Use Python 3.12 explicitly:

```bash
py -3.12 -m ...
```

Before considering code changes complete, run:

```bash
py -3.12 -m ruff check .
py -3.12 -m mypy src
py -3.12 -m pytest
```

Latest known status before this handoff:

```text
ruff: all checks passed
mypy: no issues found in 41 source files
pytest: 13 passed
```

## Important Files

Project and guidance:

```text
AGENTS.md
README.md
traceguard_codex_agent_planning_guideline.md
docs/ai_agent_usage_guideline.md
docs/session_handoff_context.md
```

Radar example inputs:

```text
examples/braking_project/traceguard.yaml
examples/braking_project/glossary.yaml
examples/braking_project/requirements/system.md
examples/braking_project/requirements/software.md
examples/braking_project/requirements/radar_on_chip_system_requirements.md
examples/braking_project/requirements/radar_on_chip_software_requirements_derivation.md
examples/braking_project/traces/system_to_sw.yaml
examples/braking_project/traces/radar_system_to_sw.yaml
```

Generated outputs:

```text
examples/braking_project/build/radar_system_atoms.yaml
examples/braking_project/build/radar_software_atoms.yaml
examples/braking_project/reports/coverage.html
examples/braking_project/reports/coverage.md
examples/braking_project/reports/coverage.csv
examples/braking_project/reports/evidence.json
```

Main source areas:

```text
src/traceguard/parser/atomizer.py
src/traceguard/parser/controlled_language.py
src/traceguard/importers/markdown_importer.py
src/traceguard/importers/derivation_markdown.py
src/traceguard/rules/atom_coverage_rules.py
src/traceguard/reporting/html_report.py
src/traceguard/cli.py
```

## Recent Major Work

1. Bootstrapped the TraceGuard Python package.
2. Added Pydantic domain models, importers, atomizer, glossary resolver, trace loader, deterministic rule engine, reports, and CLI.
3. Added the Radar-on-Chip example requirements.
4. Added deterministic derivation trace generation for grouped Radar-on-Chip Markdown tables.
5. Generated radar atom YAML outputs:

   ```text
   examples/braking_project/build/radar_system_atoms.yaml
   examples/braking_project/build/radar_software_atoms.yaml
   ```

6. Created a rich HTML human review report.
7. Added colored parent requirement atom spans:

   ```text
   green: full or stronger coverage
   yellow: partial, weaker, manual-review, or ambiguous
   red: missing, conflicting, or unverifiable
   ```

8. Added hover synthesis over colored parent text.
9. Added click behavior from colored parent text or atom chip to the full evidence block.
10. Fixed HTML escaping so large `data-text` or `data-tooltip-html` attributes do not leak visibly.
11. Tooltip content now lives in inert `<template>` elements.
12. Report generation is deterministic: no AI calls, no randomness, no timestamps.

## Current HTML Report Behavior

Main report:

```text
examples/braking_project/reports/coverage.html
```

The HTML report currently supports:

- Search
- Status and severity filters
- Parent requirement text with colored atom spans
- Colored atom chips
- Hover synthesis
- Click-to-full-evidence navigation
- Parent atom details
- Child atom evidence
- Linked child requirement text
- Trace evidence and rationale
- Manual review checklist

Hover tooltip behavior:

- Shows parent atom ID.
- Shows coverage verdict.
- Shows all mapped child atom IDs and short atom remarks.
- Shows rule and severity.
- Shows click hint.
- Does not intentionally truncate child atom remarks.
- Expands to fit content instead of using an internal scrollbar.

Click behavior:

- Click colored parent text or atom chip.
- The page scrolls to the full atom evidence block.
- All evidence panels open.
- The evidence block is briefly highlighted.

## Useful Commands

Run analysis:

```bash
py -3.12 -m traceguard.cli check --project examples/braking_project/traceguard.yaml
```

Generate HTML report:

```bash
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format html
```

Generate all report types:

```bash
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format markdown
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format csv
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format json
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format html
```

Export radar atomizer YAML:

```bash
py -3.12 -m traceguard.cli atomize --input examples/braking_project/requirements/radar_on_chip_system_requirements.md --output examples/braking_project/build/radar_system_atoms.yaml

py -3.12 -m traceguard.cli atomize --input examples/braking_project/requirements/radar_on_chip_software_requirements_derivation.md --output examples/braking_project/build/radar_software_atoms.yaml
```

Explain one result:

```bash
py -3.12 -m traceguard.cli explain --project examples/braking_project/traceguard.yaml --parent ROC-SYS-027 --atom ROC-SYS-027.A2
```

## Known Radar Analysis Issue

`ROC-SYS-027.A2` is currently partial because the parent has a `100 ms` timing constraint, but linked child atoms do not expose a mechanically comparable numeric child constraint.

## User Preferences

- TraceGuard may be used with older GPT models such as GPT-4.1, but GPT must remain advisory only.
- The final coverage decision must come from deterministic TraceGuard rules.
- The user wants rich, human-reviewable HTML evidence.
- The user wants hover tooltip synthesis to be concise but to show all mapped child atoms.
- The user wants full detailed evidence available on click.
- The user wants report and report content to be deterministic.

## First Actions in a New Chat

When a new Codex chat starts on this repository:

1. Read this file first.
2. Read `AGENTS.md`.
3. Read `README.md` if user-facing behavior is relevant.
4. Read `docs/ai_agent_usage_guideline.md` if the task involves AI-assisted workflows.
5. Before changing report behavior, inspect `src/traceguard/reporting/html_report.py`.
6. After changes, regenerate `coverage.html` and run the quality gates.

