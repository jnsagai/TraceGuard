from pathlib import Path

from traceguard.checker import run_check
from traceguard.importers.project_loader import load_project
from traceguard.reporting.markdown_report import render_markdown_report


def test_markdown_report_is_deterministic() -> None:
    project_file = Path("examples/braking_project/traceguard.yaml")
    resolved = load_project(project_file)
    results, findings, _ = run_check(project_file)

    report = render_markdown_report(resolved.name, resolved.baseline, results, findings)

    assert "# Coverage Report: braking_example" in report
    assert "| SYS-REQ-001 | SYS-REQ-001.A1 | stronger_than_parent |" in report
    assert "R-VERIF-001" in report

