# TraceGuard

TraceGuard is a deterministic requirements derivation coverage checker for AI-assisted requirements engineering.

It helps engineering teams verify whether lower-level requirements sufficiently derive from higher-level requirements by atomizing requirements, validating trace links, checking numeric constraints, and producing auditable coverage evidence.

TraceGuard is designed for safety-critical and process-assessed environments where AI-generated requirements must be reviewable, explainable, and independently checked.

Core principle:

> AI proposes. Deterministic rules decide.

## What It Does

TraceGuard checks coverage at requirement-atom level, not just requirement-to-requirement level.

Given:

- Parent requirements, such as system or stakeholder requirements
- Child requirements, such as software requirements
- Explicit trace links
- Optional project glossary

TraceGuard produces:

- Atom-level coverage decisions
- Missing or partial derivation findings
- Numeric constraint compatibility checks
- Vague or unverifiable wording findings
- Markdown, CSV, JSON, and rich HTML review reports

Every coverage result includes the parent requirement, parent atom, linked children, matched child atoms where available, rule ID, deterministic explanation, status, severity, and recommended action.

## Deterministic Pipeline

```text
Natural-language requirements
        |
Import and normalization
        |
Rule-based atomization
        |
Canonical requirement model
        |
Traceability graph
        |
Deterministic rule engine
        |
Coverage reports and review evidence
```

AI-generated requirements or trace proposals may be imported later as structured artifacts, but TraceGuard does not call an AI model and does not accept AI confidence as a final coverage decision.

## Install

TraceGuard targets Python 3.12+.

On this machine, use the Python launcher explicitly:

```bash
py -3.12 -m pip install -e ".[dev]"
```

If your default `python` is already Python 3.12+, this also works:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

Create a new project skeleton:

```bash
py -3.12 -m traceguard.cli init my_traceguard_project
```

Validate inputs:

```bash
py -3.12 -m traceguard.cli validate --project examples/braking_project/traceguard.yaml
```

Run deterministic coverage analysis:

```bash
py -3.12 -m traceguard.cli check --project examples/braking_project/traceguard.yaml
```

Generate reports:

```bash
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format markdown
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format csv
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format json
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format html
```

Explain one coverage result:

```bash
py -3.12 -m traceguard.cli explain --project examples/braking_project/traceguard.yaml --parent ROC-SYS-027 --atom ROC-SYS-027.A2
```

## Radar-on-Chip Example

The repository includes an example project under:

```text
examples/braking_project/
```

Despite the directory name, this project currently contains both:

- A small braking-system example
- A larger Radar-on-Chip system/software derivation example

Important files:

```text
examples/braking_project/traceguard.yaml
examples/braking_project/requirements/radar_on_chip_system_requirements.md
examples/braking_project/requirements/radar_on_chip_software_requirements_derivation.md
examples/braking_project/traces/radar_system_to_sw.yaml
examples/braking_project/glossary.yaml
examples/braking_project/reports/coverage.html
examples/braking_project/reports/evidence.json
```

Run the radar analysis:

```bash
py -3.12 -m traceguard.cli check --project examples/braking_project/traceguard.yaml
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format html
```

Open the human review report:

```text
examples/braking_project/reports/coverage.html
```

The HTML report includes search, status/severity filters, parent requirement text, atom predicates, linked child requirement text, trace rationale, findings, and recommended actions.

## Atomizer

The atomizer lives here:

```text
src/traceguard/parser/atomizer.py
```

Supporting controlled-language and numeric constraint parsing lives here:

```text
src/traceguard/parser/controlled_language.py
```

Atomization runs automatically when requirements are loaded through:

```text
src/traceguard/importers/project_loader.py
```

You can also export atomizer output directly:

```bash
py -3.12 -m traceguard.cli atomize --input examples/braking_project/requirements/radar_on_chip_system_requirements.md --output examples/braking_project/build/radar_system_atoms.yaml
```

Trace YAML files reference atom IDs, but they do not store full atom details. Full atom details are generated in memory and appear in report/evidence outputs.

## Project File

A TraceGuard project is configured with `traceguard.yaml`:

```yaml
name: braking_example
baseline: "2026-01-01"
requirements:
  - requirements/system.md
  - requirements/software.md
  - requirements/radar_on_chip_system_requirements.md
  - requirements/radar_on_chip_software_requirements_derivation.md
traces:
  - traces/system_to_sw.yaml
  - traces/radar_system_to_sw.yaml
glossary: glossary.yaml
reports_dir: reports
build_dir: build
```

Requirement inputs currently support:

- Markdown `## REQ-ID` blocks
- Markdown tables used by the Radar-on-Chip example
- CSV files with `id, level, type, text, asil, status, source`

Trace inputs use YAML:

```yaml
links:
  - source_id: ROC-SYS-027
    target_id: ROC-SWR-027-01
    link_type: decomposes
    covered_atom_ids:
      - ROC-SYS-027.A1
    rationale: The software requirement is listed under ROC-SYS-027 in the derivation table.
```

## Coverage Statuses

TraceGuard can produce statuses such as:

- `full`
- `partial`
- `missing`
- `conflicting`
- `weaker_than_parent`
- `stronger_than_parent`
- `over_specified`
- `ambiguous`
- `unverifiable`
- `manual_review_required`

The MVP currently implements the first deterministic checks for atom coverage, numeric constraint comparison, safety-integrity review, trace validation, glossary ambiguity, and vague wording.

## Reports

Generated reports are written to the configured `reports_dir`.

Available formats:

- `coverage.md`: Markdown summary and atom coverage table
- `coverage.csv`: Spreadsheet-friendly coverage matrix
- `evidence.json`: Stable deterministic evidence package for review diffing
- `coverage.html`: Rich human review report

Example:

```bash
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format html
```

## AI Agent Usage

TraceGuard is designed to work with AI-assisted requirements workflows while keeping final coverage decisions deterministic.

AI agents should follow the operating guideline in:

```text
docs/ai_agent_usage_guideline.md
```

Short version:

- AI may draft requirements, trace links, rationales, glossary additions, and review summaries.
- AI must run TraceGuard before claiming coverage status.
- AI must not use model confidence as final evidence.
- Non-full results must be surfaced for human review.

## Quality Gates

Before considering changes complete, run:

```bash
py -3.12 -m ruff check .
py -3.12 -m mypy src
py -3.12 -m pytest
```

Current expected result:

```text
ruff: all checks passed
mypy: no issues found
pytest: tests pass
```

## Current Limitations

TraceGuard is an MVP. Important limitations:

- Atomization is rule-based and intentionally conservative.
- The Radar-on-Chip trace file is generated from derivation-table grouping, not yet from hand-reviewed atom-level semantic mapping.
- Glossary resolution exists, but broad terminology coverage still depends on project glossary quality.
- ReqIF, Excel, database storage, and external requirements-management connectors are placeholders or future work.
- Logical implication checks are limited; deeper compound logic can later use Z3.

When uncertain, TraceGuard should prefer explicit findings and manual review over silent automatic acceptance.

## Repository Layout

```text
src/traceguard/
  ai/              deterministic AI proposal schema and validator
  domain/          Pydantic domain models
  graph/           trace graph helpers
  importers/       Markdown, CSV, and derivation import helpers
  parser/          atomizer, controlled language parser, glossary resolver
  reporting/       Markdown, CSV, JSON, and HTML reports
  rules/           deterministic coverage and validation rules
tests/
  unit/
  integration/
  golden/
docs/
examples/
```
