from pathlib import Path

from traceguard.checker import run_check
from traceguard.domain.coverage import CoverageStatus


def test_check_flow_writes_evidence() -> None:
    project = Path("examples/braking_project/traceguard.yaml")

    results, findings, output = run_check(project)

    assert output.exists()
    assert {result.status for result in results} >= {
        CoverageStatus.FULL,
        CoverageStatus.PARTIAL,
        CoverageStatus.STRONGER_THAN_PARENT,
    }
    assert any(finding.code == "R-VERIF-001" for finding in findings)

