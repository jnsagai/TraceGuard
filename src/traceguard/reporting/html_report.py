from __future__ import annotations

import html
import re
from collections import Counter, defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Template
from markupsafe import Markup

from traceguard.domain.atom import RequirementAtom
from traceguard.domain.coverage import CoverageResult, ValidationFinding
from traceguard.domain.requirement import Requirement
from traceguard.domain.trace import TraceLink


@dataclass(frozen=True)
class ReviewAtom:
    result: CoverageResult
    parent_atom: RequirementAtom | None
    child_requirements: list[Requirement]
    child_atoms: list[RequirementAtom]
    trace_links: list[TraceLink]


@dataclass(frozen=True)
class ReviewParent:
    requirement: Requirement | None
    parent_id: str
    atoms: list[ReviewAtom]


HTML_TEMPLATE = """{% macro atom_table(atom) -%}
<table class="field-table">
  <tr><th>ID</th><td>{{ atom.id }}</td></tr>
  <tr><th>Kind</th><td>{{ atom.kind.value }}</td></tr>
  <tr><th>Status</th><td>{{ atom.atom_status.value }}</td></tr>
  <tr><th>Subject</th><td>{{ atom.subject or "-" }}</td></tr>
  <tr><th>Action</th><td>{{ atom.action or "-" }}</td></tr>
  <tr><th>Object</th><td>{{ atom.object or "-" }}</td></tr>
  <tr><th>Condition</th><td>{{ atom.condition or "-" }}</td></tr>
  <tr><th>Predicate</th><td><code>{{ atom.predicate }}</code></td></tr>
  {% if atom.constraint %}
    <tr><th>Constraint</th><td>
      {{ atom.constraint.parameter }}
      {{ atom.constraint.operator.value }}
      {{ atom.constraint.value }}
      {{ atom.constraint.unit or "" }}
    </td></tr>
    <tr><th>Context</th><td>{{ atom.constraint.context or "-" }}</td></tr>
  {% else %}
    <tr><th>Constraint</th><td>-</td></tr>
  {% endif %}
  <tr>
    <th>Safety</th>
    <td>{{ atom.safety_relevance.value if atom.safety_relevance else "-" }}</td>
  </tr>
</table>
{%- endmacro %}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TraceGuard Review Report - {{ project }}</title>
  <style>
    :root {
      --bg: #f6f8fb;
      --surface: #ffffff;
      --ink: #182230;
      --muted: #5b6878;
      --line: #d9e1ea;
      --accent: #2563eb;
      --full: #0f7b4f;
      --partial: #9a5b00;
      --risk: #b42318;
      --review: #6146b3;
      --info: #475467;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    header {
      background: #101828;
      color: white;
      padding: 24px 32px;
    }
    header h1 { margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }
    header p { margin: 0; color: #cdd5df; max-width: 980px; }
    main { padding: 24px 32px 48px; }
    .toolbar {
      position: sticky;
      top: 0;
      z-index: 5;
      display: grid;
      grid-template-columns: minmax(240px, 1fr) repeat(2, minmax(180px, 240px));
      gap: 12px;
      padding: 12px;
      margin: -24px -8px 20px;
      background: rgba(246, 248, 251, 0.96);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(8px);
    }
    input, select {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 9px 10px;
      color: var(--ink);
      background: white;
    }
    .summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }
    .metric {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }
    .metric strong { display: block; font-size: 24px; margin-bottom: 2px; }
    .metric span { color: var(--muted); }
    section {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      margin: 14px 0;
      overflow: clip;
    }
    .parent-head {
      display: grid;
      grid-template-columns: minmax(130px, 180px) 1fr auto;
      gap: 14px;
      align-items: start;
      padding: 16px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfe;
    }
    .parent-id { font-weight: 700; font-size: 16px; }
    .requirement-text { margin: 0; color: #2c3848; }
    .annotated-text {
      margin: 0;
      color: #2c3848;
      line-height: 1.8;
    }
    .coverage-span {
      border-radius: 4px;
      padding: 2px 4px;
      box-decoration-break: clone;
      -webkit-box-decoration-break: clone;
      cursor: pointer;
    }
    .coverage-span:hover, .atom-chip:hover {
      outline: 2px solid rgba(37, 99, 235, 0.45);
    }
    .evidence-tooltip {
      position: fixed;
      z-index: 20;
      display: none;
      width: max-content;
      min-width: 320px;
      max-width: min(680px, calc(100vw - 32px));
      overflow: visible;
      padding: 10px 12px;
      border: 1px solid #b8c7d9;
      border-radius: 8px;
      background: #ffffff;
      box-shadow: 0 18px 44px rgba(16, 24, 40, 0.22);
      color: var(--ink);
      font-size: 13px;
      pointer-events: none;
    }
    .evidence-tooltip h3 {
      margin: 0 0 6px;
      font-size: 14px;
    }
    .evidence-tooltip p {
      margin: 6px 0;
    }
    .tooltip-verdict {
      font-weight: 700;
      margin: 0 0 6px;
    }
    .tooltip-meta {
      color: var(--muted);
      font-size: 12px;
      margin-top: 8px;
    }
    .coverage-full, .coverage-stronger_than_parent {
      background: #dff7eb;
      border-bottom: 2px solid var(--full);
    }
    .coverage-partial, .coverage-weaker_than_parent,
    .coverage-manual_review_required, .coverage-ambiguous {
      background: #fff1cf;
      border-bottom: 2px solid var(--partial);
    }
    .coverage-missing, .coverage-conflicting, .coverage-unverifiable {
      background: #ffe2dd;
      border-bottom: 2px solid var(--risk);
    }
    .atom-chip-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }
    .atom-chip {
      display: inline-flex;
      gap: 6px;
      align-items: center;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 12px;
      border: 1px solid var(--line);
      background: #fff;
      cursor: pointer;
    }
    .atom.focused-evidence {
      outline: 3px solid rgba(37, 99, 235, 0.55);
      background: #f8fbff;
    }
    .parent-meta { color: var(--muted); font-size: 12px; white-space: nowrap; }
    .atom {
      display: grid;
      grid-template-columns: 180px 1fr;
      gap: 16px;
      padding: 16px;
      border-top: 1px solid var(--line);
    }
    .atom:first-of-type { border-top: 0; }
    .atom-side { display: flex; flex-direction: column; gap: 8px; }
    .atom-id { font-weight: 700; }
    .predicate {
      display: block;
      padding: 8px;
      border-radius: 6px;
      background: #eef4ff;
      color: #173b7a;
      overflow-wrap: anywhere;
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 12px;
    }
    .badge {
      display: inline-flex;
      width: fit-content;
      align-items: center;
      border-radius: 999px;
      padding: 3px 9px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid transparent;
      text-transform: capitalize;
    }
    .status-full, .status-stronger_than_parent { color: var(--full); background: #eaf7f0; }
    .status-partial, .status-weaker_than_parent { color: var(--partial); background: #fff4df; }
    .status-missing, .status-conflicting, .status-unverifiable {
      color: var(--risk);
      background: #fff0ed;
    }
    .status-manual_review_required, .status-ambiguous {
      color: var(--review);
      background: #f2efff;
    }
    .severity-info, .severity-low { color: var(--info); background: #f2f4f7; }
    .severity-medium { color: var(--partial); background: #fff4df; }
    .severity-high, .severity-critical { color: var(--risk); background: #fff0ed; }
    .explanation {
      margin: 0 0 12px;
      padding-left: 12px;
      border-left: 4px solid var(--accent);
    }
    .detail-grid {
      display: grid;
      grid-template-columns: minmax(220px, 1fr) minmax(220px, 1fr);
      gap: 12px;
    }
    .deep-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
      margin-bottom: 12px;
    }
    .field-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    .field-table th, .field-table td {
      border-top: 1px solid #eef2f6;
      padding: 6px 4px;
      text-align: left;
      vertical-align: top;
    }
    .field-table th {
      width: 120px;
      color: var(--muted);
      font-weight: 600;
    }
    .atom-list {
      display: grid;
      gap: 8px;
    }
    .atom-card {
      border: 1px solid #e6edf5;
      border-radius: 6px;
      padding: 10px;
      background: #fbfcfe;
    }
    .checklist {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px;
      margin-top: 12px;
    }
    .check {
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px;
      background: #fff;
      color: #344054;
      font-size: 13px;
    }
    details {
      border: 1px solid var(--line);
      border-radius: 7px;
      background: #fff;
    }
    summary {
      cursor: pointer;
      padding: 10px 12px;
      font-weight: 700;
    }
    .detail-body { padding: 0 12px 12px; }
    .child {
      padding: 10px 0;
      border-top: 1px solid #eef2f6;
    }
    .child:first-child { border-top: 0; }
    .child-id { font-weight: 700; color: #173b7a; }
    .rationale {
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 13px;
    }
    .findings {
      padding: 0 16px 16px;
    }
    .finding {
      display: grid;
      grid-template-columns: 120px 140px 1fr;
      gap: 10px;
      padding: 10px 0;
      border-top: 1px solid var(--line);
    }
    .empty { padding: 16px; color: var(--muted); }
    @media (max-width: 860px) {
      main { padding: 16px; }
      header { padding: 20px 16px; }
      .toolbar, .parent-head, .atom, .detail-grid, .finding {
        grid-template-columns: 1fr;
      }
      .toolbar { margin: -16px -16px 16px; }
      .parent-meta { white-space: normal; }
    }
  </style>
</head>
<body>
  <header>
    <h1>TraceGuard Coverage Review: {{ project }}</h1>
    <p>
      Baseline: {{ baseline or "not specified" }}.
      Deterministic coverage results for human review. AI proposals are not used as final
      authority; every decision below is tied to a rule, atom, trace, and explanation.
    </p>
  </header>
  <main>
    <div class="toolbar">
      <input id="search" type="search" placeholder="Search IDs, requirement text, rule, rationale">
      <select id="statusFilter">
        <option value="">All statuses</option>
        {% for status in statuses %}<option value="{{ status }}">{{ status }}</option>{% endfor %}
      </select>
      <select id="severityFilter">
        <option value="">All severities</option>
        {% for severity in severities %}
          <option value="{{ severity }}">{{ severity }}</option>
        {% endfor %}
      </select>
    </div>

    <div class="summary">
      <div class="metric"><strong>{{ total_results }}</strong><span>Atom decisions</span></div>
      <div class="metric"><strong>{{ parent_count }}</strong><span>Parent requirements</span></div>
      <div class="metric">
        <strong>{{ total_children }}</strong><span>Linked child requirements</span>
      </div>
      <div class="metric">
        <strong>{{ findings|length }}</strong><span>Validation findings</span>
      </div>
      {% for status, count in status_counts.items() %}
        <div class="metric"><strong>{{ count }}</strong><span>{{ status }}</span></div>
      {% endfor %}
    </div>

    <section>
      <div class="parent-head">
        <div class="parent-id">Review Findings</div>
        <p class="requirement-text">
          Issues that need manual attention before accepting the analysis.
        </p>
        <div class="parent-meta">{{ findings|length }} finding(s)</div>
      </div>
      <div class="findings">
        {% for finding in findings %}
          <div class="finding">
            <span class="badge severity-{{ finding.severity.value }}">
              {{ finding.severity.value }}
            </span>
            <strong>{{ finding.code }}</strong>
            <span>{{ finding.message }}</span>
          </div>
        {% else %}
          <div class="empty">No validation findings.</div>
        {% endfor %}
      </div>
    </section>

    {% for parent in parents %}
      <section class="parent">
        <div class="parent-head">
          <div>
            <div class="parent-id">{{ parent.parent_id }}</div>
            {% if parent.requirement %}
              <div class="parent-meta">
                {{ parent.requirement.level.value }} / {{ parent.requirement.type.value }}
              </div>
            {% endif %}
          </div>
          <div>
            <p class="annotated-text">{{ parent.annotated_text }}</p>
            <div class="atom-chip-row">
              {% for atom_chip in parent.atom_chips %}
                <span
                  class="atom-chip coverage-{{ atom_chip.status }}"
                  role="button"
                  tabindex="0"
                  data-atom-ref="{{ atom_chip.atom_id }}"
                >
                  <strong>{{ atom_chip.atom_id }}</strong>
                  <span>{{ atom_chip.status }}</span>
                </span>
              {% endfor %}
            </div>
          </div>
          <div class="parent-meta">{{ parent.atoms|length }} atom decision(s)</div>
        </div>
        {% for atom in parent.atoms %}
          <article
            class="atom"
            data-status="{{ atom.result.status.value }}"
            data-severity="{{ atom.result.severity.value }}"
            data-atom-evidence="{{ atom.result.parent_atom_id }}"
            data-tooltip-id="{{ atom.tooltip_id }}"
          >
            <template id="{{ atom.tooltip_id }}">{{ atom.tooltip_html }}</template>
            <div class="atom-side">
              <span class="atom-id">{{ atom.result.parent_atom_id }}</span>
              <span class="badge status-{{ atom.result.status.value }}">
                {{ atom.result.status.value }}
              </span>
              <span class="badge severity-{{ atom.result.severity.value }}">
                {{ atom.result.severity.value }}
              </span>
              <span class="parent-meta">{{ atom.result.rule_id }} / {{ atom.atom_kind }}</span>
            </div>
            <div>
              <code class="predicate">{{ atom.atom_predicate }}</code>
              <p class="explanation">{{ atom.result.explanation }}</p>
              {% if atom.result.recommended_action %}
                <p><strong>Recommended action:</strong> {{ atom.result.recommended_action }}</p>
              {% endif %}
              <div class="deep-grid">
                <details open>
                  <summary>Parent Atom Details</summary>
                  <div class="detail-body">
                    {% if atom.parent_atom %}
                      {{ atom_table(atom.parent_atom) }}
                    {% else %}
                      <div class="empty">Parent atom details unavailable.</div>
                    {% endif %}
                  </div>
                </details>
                <details>
                  <summary>Child Atom Evidence ({{ atom.child_atoms|length }})</summary>
                  <div class="detail-body">
                    <div class="atom-list">
                      {% for child_atom in atom.child_atoms %}
                        <div class="atom-card">
                          {{ atom_table(child_atom) }}
                        </div>
                      {% else %}
                        <div class="empty">No child atoms available for linked children.</div>
                      {% endfor %}
                    </div>
                  </div>
                </details>
              </div>
              <div class="detail-grid">
                <details open>
                  <summary>
                    Linked Child Requirements ({{ atom.child_requirements|length }})
                  </summary>
                  <div class="detail-body">
                    {% for child in atom.child_requirements %}
                      <div class="child">
                        <div class="child-id">{{ child.id }}</div>
                        <div>{{ child.text }}</div>
                        <div class="parent-meta">
                          {{ child.level.value }} / {{ child.type.value }}
                        </div>
                      </div>
                    {% else %}
                      <div class="empty">No linked child requirement.</div>
                    {% endfor %}
                  </div>
                </details>
                <details>
                  <summary>Trace Evidence ({{ atom.trace_links|length }})</summary>
                  <div class="detail-body">
                    {% for link in atom.trace_links %}
                      <div class="child">
                        <div class="child-id">{{ link.source_id }} -> {{ link.target_id }}</div>
                        <div class="parent-meta">
                          {{ link.link_type.value }} / {{ link.origin.value }} /
                          {{ link.review_status.value }}
                        </div>
                        <p class="rationale">{{ link.rationale or "No rationale supplied." }}</p>
                        <p class="rationale">
                          Covered atoms: {{ ", ".join(link.covered_atom_ids) or "none" }}
                        </p>
                      </div>
                    {% else %}
                      <div class="empty">No trace evidence.</div>
                    {% endfor %}
                  </div>
                </details>
              </div>
              <details>
                <summary>Manual Review Checklist</summary>
                <div class="detail-body">
                  <div class="checklist">
                    <div class="check">Parent atom represents the parent requirement intent.</div>
                    <div class="check">
                      Linked child requirements are in the correct allocation scope.
                    </div>
                    <div class="check">Child atoms preserve or strengthen numeric constraints.</div>
                    <div class="check">Terminology equivalence is supported by the glossary.</div>
                    <div class="check">Trace rationale is specific and reviewable.</div>
                    <div class="check">Any partial/manual-review result has a disposition.</div>
                  </div>
                </div>
              </details>
            </div>
          </article>
        {% endfor %}
      </section>
    {% endfor %}
  </main>
  <div id="evidenceTooltip" class="evidence-tooltip" role="tooltip"></div>
  <script>
    const search = document.getElementById("search");
    const statusFilter = document.getElementById("statusFilter");
    const severityFilter = document.getElementById("severityFilter");
    const parents = [...document.querySelectorAll(".parent")];
    const tooltip = document.getElementById("evidenceTooltip");

    function applyFilters() {
      const query = search.value.trim().toLowerCase();
      const status = statusFilter.value;
      const severity = severityFilter.value;
      for (const parent of parents) {
        let visibleAtoms = 0;
        for (const atom of parent.querySelectorAll(".atom")) {
          const text = `${parent.textContent} ${atom.textContent}`.toLowerCase();
          const matchesQuery = !query || text.includes(query);
          const matchesStatus = !status || atom.dataset.status === status;
          const matchesSeverity = !severity || atom.dataset.severity === severity;
          const visible = matchesQuery && matchesStatus && matchesSeverity;
          atom.style.display = visible ? "" : "none";
          if (visible) visibleAtoms += 1;
        }
        parent.style.display = visibleAtoms > 0 ? "" : "none";
      }
    }

    search.addEventListener("input", applyFilters);
    statusFilter.addEventListener("change", applyFilters);
    severityFilter.addEventListener("change", applyFilters);

    function revealAtomEvidence(atomId) {
      const target = document.querySelector(`[data-atom-evidence="${atomId}"]`);
      if (!target) return;
      for (const details of target.querySelectorAll("details")) {
        details.open = true;
      }
      target.scrollIntoView({ behavior: "smooth", block: "center" });
      target.classList.add("focused-evidence");
      window.setTimeout(() => target.classList.remove("focused-evidence"), 2200);
    }

    document.addEventListener("click", (event) => {
      const trigger = event.target.closest("[data-atom-ref]");
      if (trigger) revealAtomEvidence(trigger.dataset.atomRef);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      const trigger = event.target.closest("[data-atom-ref]");
      if (!trigger) return;
      event.preventDefault();
      revealAtomEvidence(trigger.dataset.atomRef);
    });

    function moveTooltip(event) {
      const margin = 14;
      const rect = tooltip.getBoundingClientRect();
      let left = event.clientX + margin;
      let top = event.clientY + margin;
      if (left + rect.width > window.innerWidth - margin) {
        left = event.clientX - rect.width - margin;
      }
      if (top + rect.height > window.innerHeight - margin) {
        top = window.innerHeight - rect.height - margin;
      }
      tooltip.style.left = `${Math.max(margin, left)}px`;
      tooltip.style.top = `${Math.max(margin, top)}px`;
    }

    function showTooltip(event, atomId) {
      const evidence = document.querySelector(`[data-atom-evidence="${atomId}"]`);
      if (!evidence || !evidence.dataset.tooltipId) return;
      const template = document.getElementById(evidence.dataset.tooltipId);
      if (!template) return;
      tooltip.innerHTML = template.innerHTML;
      tooltip.style.display = "block";
      moveTooltip(event);
    }

    function hideTooltip() {
      tooltip.style.display = "none";
      tooltip.innerHTML = "";
    }

    document.addEventListener("mousemove", (event) => {
      const trigger = event.target.closest("[data-atom-ref]");
      if (!trigger) {
        hideTooltip();
        return;
      }
      showTooltip(event, trigger.dataset.atomRef);
    });

    document.addEventListener("mouseleave", hideTooltip);
  </script>
</body>
</html>
"""


def write_html_report(
    path: Path,
    project: str,
    baseline: str | None,
    results: list[CoverageResult],
    findings: list[ValidationFinding],
    requirements: list[Requirement] | None = None,
    trace_links: list[TraceLink] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_html_report(
        project,
        baseline,
        results,
        findings,
        requirements=requirements,
        trace_links=trace_links,
    )
    path.write_text(rendered, encoding="utf-8")


def render_html_report(
    project: str,
    baseline: str | None,
    results: list[CoverageResult],
    findings: list[ValidationFinding],
    requirements: list[Requirement] | None = None,
    trace_links: list[TraceLink] | None = None,
) -> str:
    requirements_by_id = {requirement.id: requirement for requirement in requirements or []}
    atoms_by_id = {
        atom.id: atom
        for requirement in requirements_by_id.values()
        for atom in requirement.atoms
    }
    links = trace_links or []
    parents = _review_parents(results, requirements_by_id, atoms_by_id, links)
    all_child_ids = {
        child_id
        for result in results
        for child_id in result.child_requirement_ids
    }
    status_counts = Counter(result.status.value for result in results)
    rendered_parents = [
        {
            "parent_id": parent.parent_id,
            "requirement": parent.requirement,
            "annotated_text": _annotated_parent_text(parent),
            "atom_chips": [
                {
                    "atom_id": atom.result.parent_atom_id,
                    "status": atom.result.status.value,
                }
                for atom in parent.atoms
            ],
            "atoms": [
                {
                    "result": atom.result,
                    "parent_atom": atom.parent_atom,
                    "atom_predicate": (
                        atom.parent_atom.predicate
                        if atom.parent_atom
                        else "Atom predicate unavailable."
                    ),
                    "atom_kind": atom.parent_atom.kind.value if atom.parent_atom else "unknown",
                    "child_requirements": atom.child_requirements,
                    "child_atoms": atom.child_atoms,
                    "trace_links": atom.trace_links,
                    "tooltip_id": _html_id(f"tooltip-{atom.result.parent_atom_id}"),
                    "tooltip_html": _tooltip_html(atom),
                    "search_text": _atom_search_text(atom),
                }
                for atom in parent.atoms
            ],
            "search_text": _parent_search_text(parent),
        }
        for parent in parents
    ]
    return Template(HTML_TEMPLATE).render(
        project=project,
        baseline=baseline,
        total_results=len(results),
        parent_count=len(parents),
        total_children=len(all_child_ids),
        status_counts=dict(sorted(status_counts.items())),
        statuses=sorted(status_counts),
        severities=sorted({result.severity.value for result in results}),
        parents=rendered_parents,
        findings=findings,
    )


def _review_parents(
    results: list[CoverageResult],
    requirements_by_id: dict[str, Requirement],
    atoms_by_id: Mapping[str, RequirementAtom],
    trace_links: list[TraceLink],
) -> list[ReviewParent]:
    grouped: dict[str, list[ReviewAtom]] = defaultdict(list)
    for result in sorted(
        results,
        key=lambda item: (item.parent_requirement_id, item.parent_atom_id),
    ):
        parent_atom = atoms_by_id.get(result.parent_atom_id)
        child_requirements = [
            requirements_by_id[child_id]
            for child_id in result.child_requirement_ids
            if child_id in requirements_by_id
        ]
        child_atoms = [
            atoms_by_id[atom_id]
            for atom_id in result.child_atom_ids
            if atom_id in atoms_by_id
        ]
        if not child_atoms:
            child_atoms = [
                child_atom
                for child in child_requirements
                for child_atom in child.atoms
            ]
        relevant_links = [
            link
            for link in trace_links
            if link.source_id == result.parent_requirement_id
            and link.target_id in result.child_requirement_ids
            and result.parent_atom_id in link.covered_atom_ids
        ]
        grouped[result.parent_requirement_id].append(
            ReviewAtom(
                result=result,
                parent_atom=parent_atom,
                child_requirements=child_requirements,
                child_atoms=child_atoms,
                trace_links=relevant_links,
            )
        )
    return [
        ReviewParent(
            requirement=requirements_by_id.get(parent_id),
            parent_id=parent_id,
            atoms=atoms,
        )
        for parent_id, atoms in sorted(grouped.items())
    ]


def _parent_search_text(parent: ReviewParent) -> str:
    text = parent.requirement.text if parent.requirement else ""
    return f"{parent.parent_id} {text}"


def _atom_search_text(atom: ReviewAtom) -> str:
    child_text = " ".join(child.text for child in atom.child_requirements)
    rationale = " ".join(link.rationale or "" for link in atom.trace_links)
    result = atom.result
    return " ".join(
        [
            result.parent_atom_id,
            result.status.value,
            result.severity.value,
            result.rule_id,
            result.explanation,
            result.recommended_action or "",
            atom.parent_atom.predicate if atom.parent_atom else "",
            " ".join(child_atom.predicate for child_atom in atom.child_atoms),
            child_text,
            rationale,
        ]
    )


def _tooltip_html(atom: ReviewAtom) -> Markup:
    result = atom.result
    parent_constraint = _constraint_summary(atom.parent_atom)
    child_constraint = _first_child_constraint_summary(atom.child_atoms)
    child_atom_count = len(atom.child_atoms)
    constraint_note = _constraint_note(parent_constraint, child_constraint)
    next_step = result.recommended_action or "Click for child evidence and trace rationale."
    summary = _coverage_synthesis(result.status.value, child_atom_count, constraint_note)
    return Markup(
        f"<h3>{html.escape(result.parent_atom_id)}</h3>"
        f'<p class="tooltip-verdict">{html.escape(summary)}</p>'
        f"<p>{_child_atom_summary(atom.child_atoms)}</p>"
        f'<p class="tooltip-meta">{html.escape(result.rule_id)} / '
        f'{html.escape(result.severity.value)}. {html.escape(next_step)}</p>'
    )


def _coverage_synthesis(status: str, child_atom_count: int, constraint_note: str) -> str:
    child_text = f"{child_atom_count} mapped child atom(s)"
    if status in {"full", "stronger_than_parent"}:
        verdict = f"Covered by {child_text}."
    elif status == "partial":
        verdict = f"Partially covered by {child_text}."
    elif status == "missing":
        verdict = "No child coverage found."
    elif status == "weaker_than_parent":
        verdict = f"Child coverage is weaker across {child_text}."
    else:
        verdict = f"{status.replace('_', ' ').title()} across {child_text}."
    if constraint_note:
        return f"{verdict} {constraint_note}"
    return verdict


def _child_atom_summary(child_atoms: list[RequirementAtom]) -> Markup:
    if not child_atoms:
        return Markup("No mapped child atom detected.")
    items = [
        f"<strong>{html.escape(child_atom.id)}</strong>: "
        f"{html.escape(_atom_phrase(child_atom))}"
        for child_atom in child_atoms
    ]
    return Markup("<br>".join(items))


def _atom_phrase(atom: RequirementAtom) -> str:
    parts = [part for part in [atom.action, atom.object] if part]
    if parts:
        return " ".join(parts).replace("_", " ")
    return atom.predicate.replace("_", " ")


def _constraint_note(parent_constraint: str, child_constraint: str) -> str:
    if parent_constraint == "none detected":
        return ""
    if child_constraint == "none detected":
        return "Parent has a constraint; child constraint not detected."
    if parent_constraint == child_constraint:
        return f"Constraint matched: {parent_constraint}."
    return f"Parent: {parent_constraint}; child: {child_constraint}."


def _constraint_summary(atom: RequirementAtom | None) -> str:
    if atom is None or atom.constraint is None:
        return "none detected"
    constraint = atom.constraint
    return (
        f"{constraint.parameter} {constraint.operator.value} "
        f"{constraint.value} {constraint.unit or ''}"
    ).strip()


def _first_child_constraint_summary(child_atoms: list[RequirementAtom]) -> str:
    for child_atom in child_atoms:
        summary = _constraint_summary(child_atom)
        if summary != "none detected":
            return summary
    return "none detected"


def _first_rationale(trace_links: list[TraceLink]) -> str:
    for link in trace_links:
        if link.rationale:
            return link.rationale
    return "No trace rationale available."


def _shorten(value: str, limit: int) -> str:
    normalized = re.sub(r"\s+", " ", value).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "..."


def _annotated_parent_text(parent: ReviewParent) -> Markup:
    if parent.requirement is None:
        return Markup("Requirement text unavailable.")
    text = parent.requirement.text
    matches: list[tuple[int, int, str, str]] = []
    for atom in parent.atoms:
        if atom.parent_atom is None:
            continue
        for snippet in _atom_text_snippets(atom.parent_atom):
            match = _find_snippet(text, snippet)
            if match is None:
                continue
            start, end = match
            overlaps_existing = any(
                not (end <= existing_start or start >= existing_end)
                for existing_start, existing_end, _, _ in matches
            )
            if overlaps_existing:
                continue
            matches.append((start, end, atom.result.status.value, atom.result.parent_atom_id))
            break
    if not matches:
        return Markup(html.escape(text))

    parts: list[str] = []
    cursor = 0
    for start, end, status, atom_id in sorted(matches):
        parts.append(html.escape(text[cursor:start]))
        parts.append(
            f'<span class="coverage-span coverage-{html.escape(status)}" '
            f'role="button" tabindex="0" data-atom-ref="{html.escape(atom_id)}">'
            f"{html.escape(text[start:end])}</span>"
        )
        cursor = end
    parts.append(html.escape(text[cursor:]))
    return Markup("".join(parts))


def _atom_text_snippets(atom: RequirementAtom) -> list[str]:
    snippets: list[str] = []
    if atom.constraint and atom.constraint.context:
        snippets.append(atom.constraint.context)
    if atom.object:
        snippets.append(atom.object.replace("_", " "))
    if atom.action and atom.object:
        snippets.append(f"{atom.action.replace('_', ' ')} {atom.object.replace('_', ' ')}")
    if atom.action:
        snippets.append(atom.action.replace("_", " "))
    return [snippet for snippet in snippets if len(snippet.strip()) >= 4]


def _find_snippet(text: str, snippet: str) -> tuple[int, int] | None:
    words = [word for word in re.split(r"\s+", snippet.strip()) if word]
    if not words:
        return None
    pattern = r"\b" + r"[\s,;:/\-]+".join(re.escape(word) for word in words) + r"\b"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return match.start(), match.end()
    return None


def _html_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", value)
