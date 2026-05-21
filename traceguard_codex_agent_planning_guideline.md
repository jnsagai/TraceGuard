# AGENTS.md — Deterministic Requirements Derivation Coverage Checker

## Purpose

This file gives Codex durable project guidance for building a tool that checks natural-language requirements derivation coverage using a deterministic, auditable core.

The tool is intended to be used together with AI-based requirements writing tools, but the AI must not be the final authority for coverage, consistency, or compliance. AI may propose requirements, trace links, atomization, rationales, and missing derivations. The deterministic engine must validate, reject, or flag those proposals according to explicit rules.

Working project name: **TraceGuard**.

---

# 1. Product Mission

Build a software tool that verifies whether lower-level natural-language requirements sufficiently derive from, refine, decompose, allocate, or constrain higher-level requirements.

The tool shall support safety-critical and process-assessed engineering contexts, especially:

- Automotive requirements engineering
- ASPICE-style traceability and consistency reviews
- ISO 26262-oriented software/system safety requirements derivation
- AI-assisted requirements authoring workflows
- Reviewable evidence generation for assessors, safety managers, systems engineers, software architects, and quality managers

The core value proposition is:

> AI writes or proposes requirements. TraceGuard deterministically checks derivation coverage and produces auditable evidence.

---

# 2. Fundamental Engineering Principle

The tool must not attempt to “understand” unconstrained natural language in a free-form probabilistic way.

Instead, it must transform requirements into a canonical structured representation and apply deterministic checks.

The pipeline is:

```text
Natural-language requirements
        ↓
Import and normalization
        ↓
Controlled parsing / atomization
        ↓
Canonical requirement model
        ↓
Traceability graph
        ↓
Deterministic rule engine
        ↓
Coverage report and review evidence
```

AI may assist with:

```text
- drafting child requirements
- proposing parent-child links
- proposing covered requirement atoms
- proposing rationales
- proposing missing derived requirements
- suggesting requirement rewrites
```

But the deterministic engine must decide:

```text
- covered
- partially covered
- not covered
- conflicting
- weaker than parent
- over-specified
- unverifiable
- ambiguous
- requires human review
```

---

# 3. Non-Negotiable Design Rules

## 3.1 AI is advisory only

Do not implement AI-based scoring as the final coverage decision.

Bad:

```text
LLM says “coverage is complete” → accepted
```

Good:

```text
LLM proposes coverage claim → deterministic rule engine validates the claim → accepted/rejected/flagged
```

## 3.2 Coverage is checked at atom level, not whole-requirement level

A parent requirement may contain multiple obligations.

Example:

```text
SYS-REQ-001:
The braking system shall detect pedal actuation within 10 ms and transmit the braking request to the vehicle motion controller with ASIL-B integrity.
```

This contains at least five atoms:

```text
A1: detect pedal actuation
A2: detection latency <= 10 ms
A3: transmit braking request
A4: destination is vehicle motion controller
A5: ASIL-B integrity
```

The parent requirement is fully covered only when all required atoms are covered, allocated, justified, or formally excluded.

## 3.3 Use explicit project terminology

Do not infer arbitrary synonyms.

Allowed equivalence must come from the project glossary or ontology.

Example:

```yaml
vehicle_motion_controller:
  aliases:
    - VMC
    - motion controller
  type: system_element
```

If a synonym is not defined, flag it for human review.

## 3.4 Numeric and logical constraints must be mechanically checked

Examples:

```text
Parent: latency <= 10 ms
Child:  latency <= 5 ms
Result: covered, stronger than parent
```

```text
Parent: latency <= 10 ms
Child:  latency <= 20 ms
Result: weaker than parent / conflict
```

```text
Parent: latency <= 10 ms
Child:  latency shall be minimized
Result: unverifiable / insufficient coverage
```

## 3.5 The tool must explain every result

Every coverage decision must include:

```text
- parent requirement ID
- parent atom ID
- linked child requirement ID(s)
- matched child atom ID(s)
- rule ID
- deterministic reasoning
- final status
- recommended action
```

No unexplained “AI confidence” decision is acceptable.

---

# 4. Target Users

The product shall support these roles:

```text
- Requirements Engineer
- Systems Engineer
- Software Architect
- Safety Manager
- Functional Safety Assessor
- ASPICE Assessor
- Quality Manager
- Technical Authority
- AI Requirements Authoring Tool Owner
```

---

# 5. Primary Use Cases

## UC-001 — Check derivation from stakeholder/system requirements to software requirements

Input:

```text
Stakeholder or system requirements
Software requirements
Existing trace links
```

Output:

```text
Coverage matrix
Missing derivations
Weak derivations
Constraint conflicts
Unverifiable child requirements
Evidence report
```

## UC-002 — Validate AI-generated requirements

Input:

```text
Parent requirements
AI-generated child requirements
AI-proposed trace links
AI-proposed rationales
```

Output:

```text
Accepted links
Rejected links
Flagged links
Missing coverage
Human-review tasks
```

## UC-003 — Review safety-related requirement decomposition

Input:

```text
System safety requirements
Technical safety requirements
Software safety requirements
Architecture allocation data
ASIL attributes
Safety mechanism requirements
```

Output:

```text
ASIL propagation issues
Missing safety mechanisms
Unallocated safety constraints
Uncovered timing/diagnostic/integrity atoms
```

## UC-004 — Generate assessment-ready evidence

Input:

```text
Requirements baseline
Traceability graph
Coverage results
Review decisions
```

Output:

```text
HTML report
Markdown report
CSV coverage matrix
JSON evidence package
Review log
```

---

# 6. Recommended Technical Stack

Prefer a Python-first implementation for the MVP.

## 6.1 Core language

```text
Python 3.12+
```

Rationale:

```text
- strong text processing ecosystem
- easy CLI/API prototyping
- good testing libraries
- mature data validation via Pydantic
- easy integration with Z3 for constraint solving
- easy export to Markdown/HTML/CSV/JSON
```

## 6.2 Core libraries

Suggested dependencies:

```text
pydantic
typer
rich
networkx
pyyaml
pandas
z3-solver
jinja2
pytest
hypothesis
ruff
mypy
```

Optional later:

```text
fastapi
sqlmodel
sqlite-utils
spacy
textual
streamlit
reqif parsing library or custom ReqIF XML parser
```

## 6.3 Storage

MVP:

```text
YAML/JSON project files
SQLite database
CSV/Markdown report exports
```

Later:

```text
PostgreSQL
Graph database
Requirements management tool API connectors
```

---

# 7. Target Repository Structure

Create the repository using this layout:

```text
traceguard/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── src/
│   └── traceguard/
│       ├── __init__.py
│       ├── cli.py
│       ├── domain/
│       │   ├── requirement.py
│       │   ├── atom.py
│       │   ├── constraint.py
│       │   ├── trace.py
│       │   ├── coverage.py
│       │   └── project.py
│       ├── importers/
│       │   ├── markdown_importer.py
│       │   ├── csv_importer.py
│       │   ├── excel_importer.py
│       │   └── reqif_importer.py
│       ├── parser/
│       │   ├── controlled_language.py
│       │   ├── atomizer.py
│       │   ├── glossary.py
│       │   └── normalizer.py
│       ├── rules/
│       │   ├── base.py
│       │   ├── trace_rules.py
│       │   ├── atom_coverage_rules.py
│       │   ├── constraint_rules.py
│       │   ├── terminology_rules.py
│       │   ├── verification_rules.py
│       │   └── safety_rules.py
│       ├── graph/
│       │   ├── trace_graph.py
│       │   └── queries.py
│       ├── reporting/
│       │   ├── html_report.py
│       │   ├── markdown_report.py
│       │   ├── csv_report.py
│       │   └── evidence_json.py
│       ├── ai/
│       │   ├── schema.py
│       │   ├── proposal_importer.py
│       │   └── proposal_validator.py
│       └── examples/
│           ├── braking_project/
│           └── door_lock_project/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── property/
│   └── golden/
├── docs/
│   ├── product_requirements.md
│   ├── coverage_semantics.md
│   ├── rule_catalog.md
│   ├── data_model.md
│   ├── cli_usage.md
│   ├── ai_integration.md
│   └── safety_assessment_positioning.md
└── examples/
    ├── requirements.md
    ├── traces.yaml
    ├── glossary.yaml
    └── expected_report.md
```

---

# 8. Canonical Data Model

## 8.1 Requirement

Implement the requirement model using Pydantic.

```python
class Requirement(BaseModel):
    id: str
    level: RequirementLevel
    type: RequirementType
    text: str
    source: str | None = None
    version: str | None = None
    status: RequirementStatus = RequirementStatus.DRAFT
    attributes: dict[str, Any] = Field(default_factory=dict)
    atoms: list[RequirementAtom] = Field(default_factory=list)
    parent_links: list[TraceLink] = Field(default_factory=list)
    verification: VerificationInfo | None = None
```

## 8.2 Requirement atom

```python
class RequirementAtom(BaseModel):
    id: str
    parent_requirement_id: str
    kind: AtomKind
    subject: str | None = None
    action: str | None = None
    object: str | None = None
    condition: str | None = None
    constraint: Constraint | None = None
    predicate: str
    safety_relevance: SafetyRelevance | None = None
```

Suggested atom kinds:

```text
function
interface
timing_constraint
range_constraint
accuracy_constraint
capacity_constraint
safety_integrity
diagnostic
fault_reaction
availability
security
usability
environmental
verification
allocation
```

## 8.3 Constraint

```python
class Constraint(BaseModel):
    type: ConstraintType
    parameter: str
    operator: ComparisonOperator
    value: float | int | str
    unit: str | None = None
    context: str | None = None
```

Supported operators:

```text
==
!=
<
<=
>
>=
in
not_in
between
contains
```

## 8.4 Trace link

```python
class TraceLink(BaseModel):
    source_id: str
    target_id: str
    link_type: TraceLinkType
    covered_atom_ids: list[str] = Field(default_factory=list)
    rationale: str | None = None
    author: str | None = None
    origin: TraceOrigin = TraceOrigin.MANUAL
    review_status: ReviewStatus = ReviewStatus.UNREVIEWED
```

Trace origins:

```text
manual
imported
ai_proposed
tool_generated
approved_by_review
```

Trace link types:

```text
derives
refines
decomposes
allocates
satisfies
verifies
constrains
assumes
mitigates
duplicates
conflicts
self_derived
```

## 8.5 Coverage result

```python
class CoverageResult(BaseModel):
    parent_requirement_id: str
    parent_atom_id: str
    status: CoverageStatus
    child_requirement_ids: list[str]
    child_atom_ids: list[str]
    rule_id: str
    explanation: str
    recommended_action: str | None = None
    severity: Severity
```

Coverage status values:

```text
full
partial
missing
conflicting
weaker_than_parent
stronger_than_parent
over_specified
ambiguous
unverifiable
not_applicable
manual_review_required
```

---

# 9. Controlled Natural Language Rules

The MVP shall strongly prefer requirements written in controlled language.

Supported pattern:

```text
[Condition], the [actor] shall [action] [object] [constraint].
```

Examples:

```text
When the ignition is ON, the Brake Input SWC shall sample the brake pedal position every 5 ms.
The braking system shall detect pedal actuation within 10 ms.
The system shall transmit the brake request to the Vehicle Motion Controller.
The software shall store diagnostic trouble code DTC_BRAKE_SENSOR_FAILURE within 100 ms after fault confirmation.
```

Avoid accepting vague wording as valid coverage:

```text
fast
robust
optimized
minimized
user-friendly
as soon as possible
where appropriate
sufficient
adequate
high performance
```

Flag vague terms as:

```text
unverifiable
ambiguous
manual_review_required
```

---

# 10. Atomization Strategy

## 10.1 MVP atomization

Start with rule-based atomization.

The atomizer shall:

```text
- split compound requirements using "and", "or", "with", "within", "after", "before"
- extract modal verbs: shall, should, may, must
- extract actor
- extract action
- extract object
- extract condition
- extract numeric constraints
- extract units
- extract safety attributes such as ASIL, SIL, DAL when present
```

## 10.2 Example

Input:

```text
The braking system shall detect pedal actuation within 10 ms and transmit the brake request to the Vehicle Motion Controller.
```

Output:

```json
{
  "requirement_id": "SYS-REQ-001",
  "atoms": [
    {
      "id": "SYS-REQ-001.A1",
      "kind": "function",
      "predicate": "detect(braking_system, pedal_actuation)"
    },
    {
      "id": "SYS-REQ-001.A2",
      "kind": "timing_constraint",
      "predicate": "latency(detect_pedal_actuation) <= 10 ms"
    },
    {
      "id": "SYS-REQ-001.A3",
      "kind": "interface",
      "predicate": "transmit(braking_system, brake_request, vehicle_motion_controller)"
    }
  ]
}
```

## 10.3 Important limitation

Do not pretend atomization is perfect.

Each atom shall have a confidence-independent status:

```text
auto_accepted
needs_review
rejected
manual
```

AI may propose atomization, but deterministic validation must check:

```text
- syntax
- allowed terminology
- known units
- allowed action verbs
- valid constraint format
```

---

# 11. Glossary and Ontology

Create a project glossary file:

```yaml
terms:
  braking_system:
    type: system
    aliases:
      - brake system

  brake_input_swc:
    type: software_component
    aliases:
      - Brake Input SWC

  vehicle_motion_controller:
    type: system_element
    aliases:
      - VMC
      - motion controller

  brake_request:
    type: signal
    aliases:
      - braking request
```

The tool shall use the glossary to determine deterministic equivalence.

Rules:

```text
- Exact ID match is accepted.
- Alias match is accepted only if defined in glossary.
- Unknown synonym is flagged.
- Homonym or ambiguous alias is rejected or requires review.
```

---

# 12. Coverage Semantics

## 12.1 Full coverage

A parent atom is fully covered when one or more child atoms satisfy the parent atom according to deterministic rules.

Example:

```text
Parent atom:
latency(detect_pedal_actuation) <= 10 ms

Child atom:
latency(sample_brake_pedal_signal) <= 5 ms

Result:
full coverage if the trace rationale or allocation model establishes that sampling supports detection.
```

## 12.2 Partial coverage

A parent atom is partially covered when some but not all required semantic elements are covered.

Example:

```text
Parent:
transmit brake request to VMC with ASIL-B integrity

Child:
transmit brake request to VMC

Missing:
ASIL-B integrity
```

## 12.3 Missing coverage

A parent atom is missing when no child atom, allocation, or approved rationale covers it.

## 12.4 Conflict

A conflict exists when a child requirement contradicts the parent.

Example:

```text
Parent:
system shall enable feature only when vehicle speed < 5 km/h

Child:
software shall enable feature when vehicle speed <= 10 km/h
```

## 12.5 Weaker than parent

A child constraint is weaker when it allows behavior that violates the parent.

Example:

```text
Parent:
latency <= 10 ms

Child:
latency <= 20 ms
```

## 12.6 Stronger than parent

A child constraint is stronger when it is stricter but still compatible.

Example:

```text
Parent:
latency <= 10 ms

Child:
latency <= 5 ms
```

The tool should mark this as:

```text
full_coverage_stronger
```

and optionally require architectural feasibility review.

## 12.7 Over-specified

A child requirement is over-specified when it introduces design details not justified by the parent, architecture, safety concept, or approved self-derived rationale.

Example:

```text
Parent:
The system shall detect pedal actuation.

Child:
The software shall detect pedal actuation using ADC channel 7 with a 2nd order Butterworth filter.
```

This may be valid, but only if linked to an architecture/design decision.

---

# 13. Deterministic Rule Catalog

Each rule shall have:

```text
- rule ID
- name
- purpose
- input data
- algorithm
- output status
- severity
- example pass
- example fail
```

## R-TRACE-001 — Parent link required

Every non-top-level requirement must have at least one parent link unless it is explicitly marked as approved self-derived.

Failure:

```text
invalid_self_derived_requirement
```

## R-TRACE-002 — Parent shall have child coverage or allocation

Every parent requirement shall have at least one of:

```text
- child derivation link
- allocation link
- verification-only rationale
- approved non-derivation rationale
```

## R-ATOM-001 — Parent atom coverage required

Every parent atom shall be covered, allocated, or justified.

## R-ATOM-002 — Compound requirement split required

If a requirement contains multiple obligations, it shall be atomized into separate atoms.

## R-CONSTRAINT-001 — Numeric upper-bound preservation

For parent and child constraints using `<=`:

```python
if child.value <= parent.value:
    result = "covered_stronger_or_equal"
else:
    result = "weaker_than_parent"
```

## R-CONSTRAINT-002 — Numeric lower-bound preservation

For parent and child constraints using `>=`:

```python
if child.value >= parent.value:
    result = "covered_stronger_or_equal"
else:
    result = "weaker_than_parent"
```

## R-CONSTRAINT-003 — Unit compatibility

Constraints may be compared only if units are compatible.

Examples:

```text
ms ↔ s: compatible after conversion
km/h ↔ m/s: compatible after conversion
ms ↔ °C: incompatible
```

## R-TERM-001 — Unknown term

Every domain-significant noun phrase shall be known in the glossary or explicitly marked as external.

## R-TERM-002 — Alias must be approved

Synonyms are accepted only when declared as aliases in the glossary.

## R-VERIF-001 — Unverifiable wording

Flag unverifiable terms such as:

```text
fast
robust
optimized
user-friendly
adequate
sufficient
as soon as possible
where appropriate
minimize
maximize
```

unless associated with a measurable criterion.

## R-SAFETY-001 — ASIL propagation

If a parent safety requirement contains ASIL information, the child coverage shall preserve, decompose, allocate, or justify that integrity constraint.

## R-SAFETY-002 — Safety mechanism coverage

If a parent atom refers to fault detection, fault reaction, diagnostic coverage, safe state, degradation, or monitoring, at least one child atom shall cover the mechanism or explicitly allocate it.

---

# 14. Constraint Checking Algorithms

## 14.1 Simple interval logic

Implement first.

Supported examples:

```text
x <= a
x < a
x >= a
x > a
a <= x <= b
x in {a,b,c}
```

## 14.2 Unit normalization

Create unit conversion functions.

Required MVP units:

```text
time: ns, us, ms, s
speed: m/s, km/h
distance: mm, cm, m, km
temperature: °C, K
frequency: Hz, kHz
percentage: %
voltage: mV, V
current: mA, A
```

## 14.3 Later SMT solving

Later use Z3 for compound logical constraints.

Example:

```text
Parent:
enable only if speed < 5 km/h and gear == PARK

Child:
enable if speed < 3 km/h and gear == PARK

Result:
child implies parent → safe/stronger
```

---

# 15. AI Proposal Integration

The AI interface shall consume structured proposal files, not free text.

Example:

```json
{
  "proposal_id": "AI-PROP-001",
  "generated_by": "external_ai_writer",
  "requirements": [
    {
      "id": "SW-REQ-010",
      "text": "The Brake Input SWC shall sample the brake pedal signal every 5 ms.",
      "parent_links": [
        {
          "parent_id": "SYS-REQ-001",
          "covered_atoms": [
            "SYS-REQ-001.A1",
            "SYS-REQ-001.A2"
          ],
          "derivation_type": "functional_decomposition",
          "rationale": "Sampling every 5 ms supports detection within 10 ms."
        }
      ]
    }
  ]
}
```

Validation rules:

```text
- referenced parent exists
- referenced atom exists
- child requirement exists
- derivation type is allowed
- covered atom kind is compatible with child atom kind
- rationale is present for non-obvious coverage
- numeric constraint is compatible
- glossary terms are valid
```

AI proposals must result in one of:

```text
accepted
rejected
accepted_with_warning
manual_review_required
```

---

# 16. CLI Requirements

Implement a CLI named:

```bash
traceguard
```

Required commands:

```bash
traceguard init
traceguard validate
traceguard atomize
traceguard check
traceguard report
traceguard explain
traceguard import
traceguard export
```

## 16.1 `traceguard init`

Creates a project skeleton:

```text
traceguard.yaml
requirements/
traces/
glossary.yaml
reports/
```

## 16.2 `traceguard validate`

Validates input files:

```bash
traceguard validate --project traceguard.yaml
```

Checks:

```text
- duplicate IDs
- invalid YAML/JSON
- invalid trace links
- unknown glossary terms
- invalid units
```

## 16.3 `traceguard atomize`

Atomizes requirements:

```bash
traceguard atomize --input requirements/system.md --output build/system_atoms.json
```

## 16.4 `traceguard check`

Runs coverage checks:

```bash
traceguard check --project traceguard.yaml
```

## 16.5 `traceguard report`

Generates reports:

```bash
traceguard report --project traceguard.yaml --format html
traceguard report --project traceguard.yaml --format markdown
traceguard report --project traceguard.yaml --format csv
traceguard report --project traceguard.yaml --format json
```

## 16.6 `traceguard explain`

Explains one result:

```bash
traceguard explain --parent SYS-REQ-001 --atom SYS-REQ-001.A5
```

---

# 17. Input Formats

## 17.1 Markdown

Support a simple Markdown format:

```markdown
# System Requirements

## SYS-REQ-001

Level: system
Type: functional
ASIL: B

The braking system shall detect pedal actuation within 10 ms and transmit the braking request to the Vehicle Motion Controller.
```

## 17.2 CSV

Columns:

```text
id, level, type, text, asil, status, source
```

## 17.3 YAML traces

```yaml
links:
  - source_id: SYS-REQ-001
    target_id: SW-REQ-010
    link_type: decomposes
    covered_atom_ids:
      - SYS-REQ-001.A1
      - SYS-REQ-001.A2
    rationale: Sampling every 5 ms supports detection within 10 ms.
```

## 17.4 ReqIF

ReqIF support can be implemented after the MVP.

For MVP, create an abstraction:

```python
class RequirementImporter(Protocol):
    def import_requirements(self, path: Path) -> list[Requirement]:
        ...
```

Then add ReqIF later without changing the core engine.

---

# 18. Reporting Requirements

## 18.1 Markdown report

The Markdown report shall include:

```text
- project metadata
- coverage summary
- parent requirement table
- atom-level coverage matrix
- missing atoms
- conflicting atoms
- unverifiable requirements
- self-derived requirements
- AI-proposed links requiring review
- recommended actions
```

## 18.2 HTML report

The HTML report shall include:

```text
- filterable table
- severity badges
- expandable explanations
- trace graph summary
- downloadable JSON evidence
```

## 18.3 CSV report

CSV columns:

```text
parent_id
parent_atom_id
parent_atom_text
status
child_ids
child_atom_ids
rule_id
severity
explanation
recommended_action
```

## 18.4 JSON evidence

The JSON evidence file shall be deterministic and stable enough for review diffing.

```json
{
  "project": "braking_example",
  "baseline": "2026-01-01",
  "results": [
    {
      "parent_requirement_id": "SYS-REQ-001",
      "parent_atom_id": "SYS-REQ-001.A5",
      "status": "missing",
      "rule_id": "R-ATOM-001",
      "explanation": "No child atom covers ASIL-B integrity.",
      "severity": "high"
    }
  ]
}
```

---

# 19. Testing Strategy

The implementation must be test-first.

## 19.1 Unit tests

Test each component:

```text
- requirement parser
- glossary resolver
- atomizer
- unit converter
- numeric constraint checker
- trace validator
- rule engine
- report generator
```

## 19.2 Golden tests

Create example projects with expected outputs.

Examples:

```text
tests/golden/braking_project/
tests/golden/door_lock_project/
tests/golden/invalid_trace_project/
```

Each golden test shall verify:

```text
input requirements + traces + glossary → expected coverage report
```

## 19.3 Property-based tests

Use Hypothesis for constraint logic.

Examples:

```text
For upper-bound constraints:
if child_limit <= parent_limit, then child is stronger or equal.

For lower-bound constraints:
if child_limit >= parent_limit, then child is stronger or equal.
```

## 19.4 Regression tests

Every bug fix shall add a regression test.

## 19.5 Mutation-resistance expectation

Where possible, tests shall assert not just status but also:

```text
- rule ID
- explanation content
- impacted requirement ID
- impacted atom ID
```

---

# 20. Quality Gates

Codex must run these before considering work complete:

```bash
ruff check .
mypy src
pytest
```

If a feature affects reports, Codex must also run:

```bash
pytest tests/golden
```

Do not mark work complete if tests fail.

---

# 21. Definition of Done

A task is done only when:

```text
- implementation exists
- tests exist
- tests pass
- CLI behavior is documented
- example input exists where relevant
- report output is deterministic
- error messages are understandable
- no uncontrolled AI decision is introduced
```

For feature work:

```text
- add or update docs
- add at least one positive test
- add at least one negative test
- add golden example if feature affects coverage/report output
```

---

# 22. MVP Milestones

## Milestone 0 — Repo bootstrap

Deliver:

```text
- Python package skeleton
- pyproject.toml
- CLI placeholder
- README
- basic test infrastructure
- ruff/mypy/pytest config
```

## Milestone 1 — Domain model

Deliver:

```text
- Requirement model
- Atom model
- Constraint model
- TraceLink model
- CoverageResult model
- serialization/deserialization tests
```

## Milestone 2 — Markdown/CSV import

Deliver:

```text
- import requirements from Markdown
- import requirements from CSV
- validate unique IDs
- report malformed input
```

## Milestone 3 — Glossary and terminology resolver

Deliver:

```text
- glossary YAML loader
- alias resolver
- unknown-term warnings
- ambiguous-alias detection
```

## Milestone 4 — Atomizer MVP

Deliver:

```text
- detect simple shall statements
- split compound requirements
- extract numeric constraints
- extract units
- create atom IDs deterministically
```

## Milestone 5 — Trace graph

Deliver:

```text
- load trace links from YAML
- validate links
- build graph
- query parent/child relationships
```

## Milestone 6 — Rule engine

Deliver:

```text
- rule base class
- trace rules
- atom coverage rules
- numeric constraint rules
- terminology rules
- verification wording rules
```

## Milestone 7 — Reports

Deliver:

```text
- Markdown report
- CSV report
- JSON evidence report
- golden tests
```

## Milestone 8 — AI proposal validator

Deliver:

```text
- import AI proposal JSON
- validate AI-proposed links
- accept/reject/manual-review statuses
- no AI dependency in deterministic core
```

## Milestone 9 — HTML report

Deliver:

```text
- static HTML report
- severity filtering
- expandable explanations
```

## Milestone 10 — ReqIF import

Deliver:

```text
- parse ReqIF XML
- map ReqIF objects to Requirement model
- map ReqIF relations to TraceLink model
```

---

# 23. Codex Operating Instructions

When working on this repository, Codex shall:

```text
1. Read this AGENTS.md first.
2. Preserve the deterministic-core principle.
3. Prefer small, reviewable commits.
4. Add tests with every behavioral change.
5. Avoid large rewrites unless explicitly requested.
6. Keep the CLI stable.
7. Keep report output deterministic.
8. Never add AI as a final judge of requirement coverage.
9. Never silently ignore malformed requirements or trace links.
10. Prefer explicit manual-review status over uncertain automatic acceptance.
```

---

# 24. Codex Task Prompts

Use the following prompts as individual Codex tasks.

## Task 1 — Bootstrap repository

```text
Create a Python 3.12 package named traceguard using the repository layout described in AGENTS.md. Configure pyproject.toml with ruff, mypy, pytest, typer, pydantic, pyyaml, pandas, networkx, z3-solver, rich, and jinja2. Add a minimal CLI with `traceguard --help`. Add initial tests proving the package imports and the CLI runs.
```

## Task 2 — Implement domain model

```text
Implement the core Pydantic domain models described in AGENTS.md: Requirement, RequirementAtom, Constraint, TraceLink, CoverageResult, Project. Include enums for requirement level, requirement type, atom kind, trace link type, coverage status, severity, review status, and trace origin. Add serialization/deserialization tests.
```

## Task 3 — Implement glossary resolver

```text
Implement the glossary YAML loader and deterministic terminology resolver. It shall support canonical terms, aliases, term types, unknown-term detection, and ambiguous-alias detection. Add tests for exact matches, alias matches, unknown terms, and ambiguous aliases.
```

## Task 4 — Implement constraint parser and unit converter

```text
Implement parsing for numeric constraints such as `within 10 ms`, `<= 10 ms`, `less than 5 km/h`, `between 3 and 5 V`, and `every 5 ms`. Add unit normalization for time, speed, distance, temperature, frequency, percentage, voltage, and current. Add unit tests and property-based tests for upper-bound and lower-bound comparison.
```

## Task 5 — Implement atomizer MVP

```text
Implement a rule-based atomizer for controlled natural-language requirements. It shall split compound `shall` statements, extract actor/action/object/condition/constraints, generate stable atom IDs, and flag ambiguous or unverifiable wording. Add golden examples for braking and door-lock requirements.
```

## Task 6 — Implement trace link loader

```text
Implement YAML trace-link loading and validation. The validator shall detect missing source requirements, missing target requirements, invalid covered atom IDs, invalid link types, and empty rationales where rationale is required. Add tests for valid and invalid trace files.
```

## Task 7 — Implement trace graph

```text
Implement a trace graph using networkx. It shall support queries for parents, children, uncovered parents, self-derived requirements, and trace paths between requirements. Add tests using a small SYS→SW example.
```

## Task 8 — Implement deterministic rule engine

```text
Implement the rule engine and the first rule set: R-TRACE-001, R-TRACE-002, R-ATOM-001, R-CONSTRAINT-001, R-CONSTRAINT-002, R-CONSTRAINT-003, R-TERM-001, R-TERM-002, R-VERIF-001, R-SAFETY-001. Each rule shall return CoverageResult or ValidationFinding objects with rule ID, status, severity, explanation, and recommended action.
```

## Task 9 — Implement CLI check flow

```text
Implement `traceguard check --project traceguard.yaml`. It shall load requirements, traces, glossary, atomize requirements if needed, build the trace graph, run deterministic rules, and write JSON evidence to the build or reports directory. Add integration tests.
```

## Task 10 — Implement Markdown and CSV reports

```text
Implement `traceguard report --format markdown` and `traceguard report --format csv`. Reports shall include coverage summary, atom-level coverage, missing atoms, conflicts, unverifiable requirements, and recommended actions. Add golden tests to verify deterministic output.
```

## Task 11 — Implement AI proposal validator

```text
Implement AI proposal import from JSON. The validator shall check that proposed requirements, parent links, covered atoms, derivation types, and rationales are valid. It shall classify each proposal as accepted, rejected, accepted_with_warning, or manual_review_required. Do not call any AI model. This is a deterministic validator for AI-generated artifacts.
```

## Task 12 — Add HTML report

```text
Implement a static HTML report using Jinja2. The report shall include filterable status/severity sections, expandable explanations, and links between parent and child requirements. Keep output deterministic and covered by golden tests.
```

## Task 13 — Add example braking project

```text
Create a complete example project for braking requirements. Include system requirements, software requirements, glossary, trace links, AI proposal example, and expected reports. The example shall demonstrate full coverage, partial coverage, missing ASIL integrity coverage, weaker latency constraint, and unverifiable wording.
```

## Task 14 — Add documentation

```text
Create documentation pages under docs/: product_requirements.md, coverage_semantics.md, rule_catalog.md, data_model.md, cli_usage.md, ai_integration.md, and safety_assessment_positioning.md. The documentation shall emphasize that AI is advisory only and the final checks are deterministic.
```

---

# 25. Example Project

## 25.1 System requirements

```markdown
## SYS-REQ-001

Level: system
Type: functional
ASIL: B

The braking system shall detect pedal actuation within 10 ms and transmit the braking request to the Vehicle Motion Controller with ASIL-B integrity.
```

## 25.2 Software requirements

```markdown
## SW-REQ-010

Level: software
Type: functional
ASIL: B

The Brake Input SWC shall sample the brake pedal signal every 5 ms.

## SW-REQ-011

Level: software
Type: interface
ASIL: B

The Brake Request SWC shall publish the brake request to the Vehicle Motion Controller.

## SW-REQ-012

Level: software
Type: safety
ASIL: B

The brake request signal shall be protected using an approved end-to-end communication protection mechanism.
```

## 25.3 Trace links

```yaml
links:
  - source_id: SYS-REQ-001
    target_id: SW-REQ-010
    link_type: decomposes
    covered_atom_ids:
      - SYS-REQ-001.A1
      - SYS-REQ-001.A2
    rationale: Sampling every 5 ms supports detection within 10 ms.

  - source_id: SYS-REQ-001
    target_id: SW-REQ-011
    link_type: decomposes
    covered_atom_ids:
      - SYS-REQ-001.A3
      - SYS-REQ-001.A4
    rationale: The software publishes the brake request to the required destination.

  - source_id: SYS-REQ-001
    target_id: SW-REQ-012
    link_type: decomposes
    covered_atom_ids:
      - SYS-REQ-001.A5
    rationale: E2E protection is used to support ASIL-B integrity for the brake request.
```

---

# 26. Expected Coverage Report Example

```text
Coverage Report: braking_example

Parent: SYS-REQ-001
Status: FULL

Atoms:
- SYS-REQ-001.A1 detect pedal actuation
  Status: FULL
  Covered by: SW-REQ-010
  Rule: R-ATOM-001

- SYS-REQ-001.A2 latency <= 10 ms
  Status: FULL_STRONGER_OR_EQUAL
  Covered by: SW-REQ-010
  Rule: R-CONSTRAINT-001
  Explanation: Child sampling period 5 ms is stronger than parent latency constraint 10 ms, subject to accepted allocation rationale.

- SYS-REQ-001.A3 transmit brake request
  Status: FULL
  Covered by: SW-REQ-011

- SYS-REQ-001.A4 destination Vehicle Motion Controller
  Status: FULL
  Covered by: SW-REQ-011

- SYS-REQ-001.A5 ASIL-B integrity
  Status: FULL
  Covered by: SW-REQ-012
```

---

# 27. Error Handling Policy

The tool must fail clearly.

Do not silently continue when:

```text
- requirement IDs are duplicated
- trace links reference unknown requirements
- trace links reference unknown atoms
- glossary has ambiguous aliases
- units are incompatible
- project file is malformed
```

Use structured errors:

```json
{
  "code": "UNKNOWN_REQUIREMENT_ID",
  "message": "Trace link references unknown requirement SW-REQ-999.",
  "file": "traces/system_to_sw.yaml",
  "line": 12,
  "severity": "error"
}
```

---

# 28. Security and Privacy

The tool may process proprietary requirements.

Rules:

```text
- Do not send project requirements to external APIs unless an explicit integration is implemented and enabled.
- Local deterministic checks shall be the default.
- AI proposal import shall work from files generated elsewhere.
- Do not log full requirement text at debug level unless explicitly enabled.
- Do not include secrets in reports.
```

---

# 29. Future Extensions

Possible future features:

```text
- ReqIF import/export
- DOORS Next connector
- Polarion connector
- Jama connector
- Jira integration
- ASPICE evidence package
- ISO 26262 safety case evidence package
- SysML model allocation import
- Architecture model import
- Z3-based logical implication checking
- Web UI
- Review workflow with approvals
- Baseline comparison
- Requirements quality scoring
- Duplicate/conflict detection
- LLM-assisted rewrite suggestions
```

Any future AI feature must preserve the rule:

```text
AI may propose. Deterministic engine decides.
```

---

# 30. Recommended README Positioning

Use this summary in the README:

```markdown
# TraceGuard

TraceGuard is a deterministic requirements derivation coverage checker for AI-assisted requirements engineering.

It helps engineering teams verify whether lower-level requirements sufficiently derive from higher-level requirements by atomizing requirements, validating trace links, checking numeric/logical constraints, and producing auditable coverage evidence.

TraceGuard is designed for safety-critical and process-assessed environments where AI-generated requirements must be reviewable, explainable, and independently checked.

Core principle:

> AI proposes. Deterministic rules decide.
```

---

# 31. References for Codex Usage

For Codex project guidance, keep this repository-level `AGENTS.md` discoverable at the Git root. Use task-specific prompts for individual implementation steps.

Do not rely only on a long chat history. Durable project instructions belong in repository files.

