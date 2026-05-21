# AI Agent Usage Guideline for TraceGuard

This guideline explains how an AI agent should use TraceGuard when helping engineers create, validate, refine, or review requirements derivation coverage.

TraceGuard is not an AI judge. It is a deterministic requirements coverage checker. The agent may draft, organize, propose, and explain, but TraceGuard must produce the authoritative coverage evidence through explicit rules.

Core rule:

> AI proposes. Deterministic rules decide.

## 1. Agent Role

An AI agent using TraceGuard may:

- Draft parent or child requirements.
- Rewrite requirements into clearer controlled language.
- Propose trace links.
- Propose atom coverage mappings.
- Propose rationales.
- Suggest missing derived requirements.
- Suggest glossary terms and aliases.
- Explain TraceGuard findings to a human reviewer.
- Generate report artifacts by running TraceGuard commands.

An AI agent must not:

- Treat its own confidence as coverage evidence.
- Mark coverage as complete without running TraceGuard.
- Silently ignore TraceGuard findings.
- Invent synonym equivalence outside the project glossary.
- Replace human safety, ASPICE, ISO 26262, or quality review decisions.
- Send proprietary requirements to external services unless the project explicitly enables that integration.

## 2. Required Operating Sequence

When asked to analyze requirements with TraceGuard, the agent should follow this sequence.

1. Locate the project file.

   Usually:

   ```text
   traceguard.yaml
   ```

   Example:

   ```text
   examples/braking_project/traceguard.yaml
   ```

2. Inspect configured inputs.

   Check:

   - Requirement files
   - Trace files
   - Glossary file
   - Reports directory
   - Build directory

3. Confirm that all user-provided requirement files are included in `traceguard.yaml`.

   If a requirement file exists but is not referenced, add it to the project configuration before analysis.

4. Confirm that trace files exist.

   If trace links are missing but can be deterministically derived from a structured derivation document, generate a trace file and make that derivation rule explicit. If links cannot be derived deterministically, ask for trace input or generate a proposal clearly marked for review.

5. Validate the project.

   ```bash
   py -3.12 -m traceguard.cli validate --project examples/braking_project/traceguard.yaml
   ```

6. Run coverage analysis.

   ```bash
   py -3.12 -m traceguard.cli check --project examples/braking_project/traceguard.yaml
   ```

7. Generate review reports.

   ```bash
   py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format html
   py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format markdown
   py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format csv
   py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format json
   ```

8. Summarize findings for the human reviewer.

   Include:

   - Number of coverage results
   - Status counts
   - Findings count
   - High/medium severity items
   - Missing, partial, weaker, conflicting, unverifiable, or manual-review-required results
   - Report file paths

9. Run quality gates if code or tests changed.

   ```bash
   py -3.12 -m ruff check .
   py -3.12 -m mypy src
   py -3.12 -m pytest
   ```

## 3. File Responsibilities

The agent should understand these file roles.

### Project Configuration

```text
traceguard.yaml
```

Defines the project name, baseline, requirement input files, trace input files, glossary, reports directory, and build directory.

The agent may edit this file when adding new requirement or trace files.

### Requirement Files

Examples:

```text
requirements/system.md
requirements/software.md
requirements/radar_on_chip_system_requirements.md
requirements/radar_on_chip_software_requirements_derivation.md
```

Requirement files contain natural-language requirements. TraceGuard imports them and atomizes them.

The agent may add or revise requirements, but should preserve IDs and avoid changing baselined wording unless the user explicitly requests it.

### Trace Files

Examples:

```text
traces/system_to_sw.yaml
traces/radar_system_to_sw.yaml
```

Trace files connect parent requirements to child requirements and list covered parent atom IDs.

Trace YAML stores references to atom IDs, not full atomizer output.

Example:

```yaml
links:
  - source_id: ROC-SYS-027
    target_id: ROC-SWR-027-01
    link_type: decomposes
    covered_atom_ids:
      - ROC-SYS-027.A1
    rationale: The child requirement is derived from the parent timing behavior.
```

The agent may propose or generate trace links, but should identify whether they were:

- Manual
- Imported
- Tool-generated
- AI-proposed
- Approved by review

### Glossary

Example:

```text
glossary.yaml
```

The glossary defines deterministic term equivalence.

Example:

```yaml
terms:
  radar_on_chip:
    type: system
    aliases:
      - Radar-on-Chip
      - radar SoC
      - FMCW radar SoC
```

The agent may suggest glossary additions, but must not assume arbitrary synonyms are equivalent unless the glossary defines them.

### Build Outputs

Example:

```text
build/radar_system_atoms.yaml
build/radar_software_atoms.yaml
```

Build outputs are generated artifacts. They may be regenerated.

### Reports

Examples:

```text
reports/coverage.html
reports/coverage.md
reports/coverage.csv
reports/evidence.json
```

Reports are generated artifacts used for review. The rich HTML report is intended for human manual validation.

## 4. Atomizer Usage

The atomizer is implemented in:

```text
src/traceguard/parser/atomizer.py
```

Supporting controlled-language parsing is implemented in:

```text
src/traceguard/parser/controlled_language.py
```

Atomization runs automatically when TraceGuard loads requirements. The agent can also export atomization output explicitly:

```bash
py -3.12 -m traceguard.cli atomize --input examples/braking_project/requirements/radar_on_chip_system_requirements.md --output examples/braking_project/build/radar_system_atoms.yaml
```

For radar software requirements:

```bash
py -3.12 -m traceguard.cli atomize --input examples/braking_project/requirements/radar_on_chip_software_requirements_derivation.md --output examples/braking_project/build/radar_software_atoms.yaml
```

The agent should use atomizer output to:

- Inspect parent atom IDs.
- Check whether numeric constraints were extracted.
- Detect vague or unverifiable atomization.
- Build or correct trace `covered_atom_ids`.
- Explain why a result was `partial`, `missing`, or `manual_review_required`.

The agent should not manually edit atomizer output and treat it as authoritative input unless the project explicitly introduces a reviewed atom-baseline workflow.

## 5. Trace Proposal Workflow

When trace links are absent or incomplete, the agent should use this workflow.

1. Atomize parent requirements.
2. Atomize child requirements.
3. For each parent atom, identify candidate child requirements.
4. Create trace links with `covered_atom_ids`.
5. Add a rationale for every non-obvious mapping.
6. Use `origin: ai_proposed` or `origin: tool_generated` when appropriate.
7. Run TraceGuard validation and coverage checks.
8. Present all non-full results to the human reviewer.

Good trace rationale:

```text
The child requirement states that software-controlled fault reactions complete within 100 ms, matching the parent fault reaction time constraint.
```

Weak trace rationale:

```text
Looks related.
```

The agent should reject or flag weak rationales before asking a human to approve them.

## 6. Radar-on-Chip Example Workflow

For the included radar example, use:

```text
examples/braking_project/traceguard.yaml
```

Run analysis:

```bash
py -3.12 -m traceguard.cli check --project examples/braking_project/traceguard.yaml
```

Generate the human review report:

```bash
py -3.12 -m traceguard.cli report --project examples/braking_project/traceguard.yaml --format html
```

Export atomizer output:

```bash
py -3.12 -m traceguard.cli atomize --input examples/braking_project/requirements/radar_on_chip_system_requirements.md --output examples/braking_project/build/radar_system_atoms.yaml

py -3.12 -m traceguard.cli atomize --input examples/braking_project/requirements/radar_on_chip_software_requirements_derivation.md --output examples/braking_project/build/radar_software_atoms.yaml
```

Review outputs:

```text
examples/braking_project/reports/coverage.html
examples/braking_project/reports/evidence.json
examples/braking_project/build/radar_system_atoms.yaml
examples/braking_project/build/radar_software_atoms.yaml
```

Example issue pattern:

```text
Parent:
ROC-SYS-027 shall complete acquisition, processing, and output transmission within 100 ms.

TraceGuard result:
partial / R-CONSTRAINT-002

Reason:
The linked child requirements discuss timing budgets, but no linked child atom contains a mechanically checkable numeric constraint such as within 100 ms.

Agent recommendation:
Propose a child requirement or rewrite that explicitly states the software-controlled deadline within 100 ms, then rerun TraceGuard.
```

## 7. How to Report Results to Humans

When reporting TraceGuard results, the agent should be concise but complete.

Minimum summary:

```text
TraceGuard analyzed <N> atom-level coverage results.

Status counts:
- full: <N>
- partial: <N>
- missing: <N>
- weaker_than_parent: <N>
- manual_review_required: <N>

Key findings:
- <requirement/atom>: <status>, <rule>, <short explanation>

Reports:
- coverage.html
- evidence.json
```

For every significant issue, include:

- Parent requirement ID
- Parent atom ID
- Status
- Rule ID
- Explanation
- Recommended action
- Linked child requirement IDs, if any

Do not summarize a `partial`, `missing`, `weaker_than_parent`, `conflicting`, or `unverifiable` result as acceptable without human review.

## 8. Human Review Loop

The agent should guide humans through this loop.

1. Open `coverage.html`.
2. Filter for non-full statuses.
3. Review parent requirement text.
4. Review atom predicate.
5. Review linked child requirements.
6. Review trace rationale.
7. Decide one of:

   - Accept TraceGuard result.
   - Correct parent requirement wording.
   - Correct child requirement wording.
   - Add or correct trace link.
   - Add glossary term or alias.
   - Add formal exclusion or allocation rationale.
   - Mark for safety/architecture review.

8. Rerun TraceGuard.
9. Archive `evidence.json` with the review baseline.

## 9. Requirement Writing Guidance for Agents

When drafting or rewriting requirements, prefer controlled language:

```text
[Condition], the [actor] shall [action] [object] [constraint].
```

Good:

```text
The radar software shall complete software-controlled fault reactions within 100 ms after safety-critical fault detection.
```

Poor:

```text
The radar software shall react quickly to important faults.
```

Avoid vague terms unless intentionally flagged for review:

- fast
- robust
- optimized
- minimized
- sufficient
- adequate
- user-friendly
- as soon as possible
- where appropriate

Use numeric constraints when the parent has numeric constraints.

If the parent says:

```text
within 100 ms
```

Then the child should preserve or strengthen the constraint:

```text
within 100 ms
within 80 ms
```

Avoid unverifiable substitutes:

```text
within the configured timing budget
before the deadline
as soon as possible
```

Those may be useful engineering wording, but they are not mechanically equivalent unless the budget or deadline is explicitly linked and validated.

## 10. Glossary Expansion Guidance

The agent may add terms to `glossary.yaml` when repeated project vocabulary appears.

Use canonical snake_case IDs:

```yaml
terms:
  radar_detection_list:
    type: data_object
    aliases:
      - detection list
      - radar object list
```

Good glossary candidates:

- System elements
- Software components
- Signals
- Data objects
- Diagnostic events
- Safety states
- Operating modes
- Interfaces
- Calibration/configuration concepts

Do not create duplicate aliases across terms unless ambiguity is intentional and should be flagged.

After glossary edits, run:

```bash
py -3.12 -m traceguard.cli validate --project examples/braking_project/traceguard.yaml
```

## 11. Evidence Handling

The agent should preserve deterministic evidence.

Important evidence files:

```text
reports/evidence.json
reports/coverage.html
reports/coverage.csv
reports/coverage.md
```

For assessment or baseline review, the agent should record:

- Project name
- Baseline
- Commands run
- Tool version or commit, if available
- Generated report paths
- Non-full coverage results
- Validation findings
- Human decisions made after review

The agent should avoid modifying generated evidence manually. Regenerate reports from source requirements and trace files instead.

## 12. Failure Handling

If TraceGuard fails, the agent should not continue as if analysis succeeded.

Common failures:

- Duplicate requirement ID
- Unknown requirement ID in trace file
- Unknown atom ID in trace file
- Invalid YAML
- Unsupported requirement format
- Ambiguous glossary alias
- Unsupported unit

The agent should:

1. Quote or summarize the error.
2. Identify the source file.
3. Make a focused correction if safe.
4. Rerun the failed command.
5. Report whether validation now passes.

## 13. Security and Privacy

Requirements may contain proprietary or safety-sensitive information.

The agent must:

- Keep deterministic checks local by default.
- Avoid sending requirement text to external APIs.
- Avoid logging secrets or credentials.
- Avoid adding secrets to reports.
- Treat AI proposal files as input artifacts, not as authority.

## 14. Completion Criteria

An AI-agent-assisted TraceGuard task is complete only when:

- Relevant requirement files are included in the project file.
- Trace files exist and validate.
- Atomizer output is generated when requested.
- `traceguard check` runs successfully.
- Requested reports are generated.
- Non-full statuses and findings are summarized for the human reviewer.
- Code changes, if any, pass:

  ```bash
  py -3.12 -m ruff check .
  py -3.12 -m mypy src
  py -3.12 -m pytest
  ```

The agent should end with clear report paths and the highest-priority review items.

