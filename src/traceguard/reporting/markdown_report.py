from __future__ import annotations

from collections import Counter
from pathlib import Path

from traceguard.domain.coverage import CoverageResult, ValidationFinding


def render_markdown_report(
    project: str,
    baseline: str | None,
    results: list[CoverageResult],
    findings: list[ValidationFinding],
) -> str:
    counts = Counter(result.status.value for result in results)
    lines = [f"# Coverage Report: {project}", ""]
    if baseline:
        lines.extend([f"Baseline: {baseline}", ""])
    lines.extend(["## Summary", ""])
    for status, count in sorted(counts.items()):
        lines.append(f"- {status}: {count}")
    if not counts:
        lines.append("- no coverage results")
    lines.extend(["", "## Atom Coverage", ""])
    lines.append("| Parent | Atom | Status | Children | Rule | Severity | Explanation |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for result in sorted(results, key=lambda r: (r.parent_requirement_id, r.parent_atom_id)):
        lines.append(
            "| "
            + " | ".join(
                [
                    result.parent_requirement_id,
                    result.parent_atom_id,
                    result.status.value,
                    ", ".join(result.child_requirement_ids) or "-",
                    result.rule_id,
                    result.severity.value,
                    result.explanation.replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Findings", ""])
    if findings:
        for finding in findings:
            lines.append(f"- {finding.severity.value}: {finding.code} - {finding.message}")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def write_markdown_report(
    path: Path,
    project: str,
    baseline: str | None,
    results: list[CoverageResult],
    findings: list[ValidationFinding],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(project, baseline, results, findings), encoding="utf-8")

