from pathlib import Path

from traceguard.checker import run_check
from traceguard.importers.project_loader import load_project, load_requirements
from traceguard.reporting.html_report import render_html_report
from traceguard.rules.trace_rules import load_trace_links


def test_html_report_contains_review_context() -> None:
    project_file = Path("examples/braking_project/traceguard.yaml")
    resolved = load_project(project_file)
    requirements = load_requirements(resolved)
    links = load_trace_links(resolved.traces)
    results, findings, _ = run_check(project_file)

    report = render_html_report(
        resolved.name,
        resolved.baseline,
        results,
        findings,
        requirements=requirements,
        trace_links=links,
    )

    assert "TraceGuard Coverage Review: braking_example" in report
    assert "Linked Child Requirements" in report
    assert "Trace Evidence" in report
    assert "ROC-SWR-027-01" in report
    assert "Review Findings" in report
