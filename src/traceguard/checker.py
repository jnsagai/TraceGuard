from __future__ import annotations

from pathlib import Path

from traceguard.domain.coverage import CoverageResult, ValidationFinding
from traceguard.importers.project_loader import load_project, load_requirements
from traceguard.parser.glossary import Glossary
from traceguard.reporting.evidence_json import write_evidence_json
from traceguard.rules.atom_coverage_rules import run_atom_coverage
from traceguard.rules.terminology_rules import validate_glossary
from traceguard.rules.trace_rules import load_trace_links, validate_trace_links
from traceguard.rules.verification_rules import validate_verifiability


def run_check(project_file: Path) -> tuple[list[CoverageResult], list[ValidationFinding], Path]:
    project = load_project(project_file)
    requirements = load_requirements(project)
    links = load_trace_links(project.traces)
    glossary = Glossary.from_yaml(project.glossary) if project.glossary else Glossary.empty()
    findings = [
        *validate_glossary(glossary),
        *validate_trace_links(requirements, links),
        *validate_verifiability(requirements),
    ]
    results = run_atom_coverage(requirements, links)
    output = project.reports_dir / "evidence.json"
    write_evidence_json(output, project.name, project.baseline, results, findings)
    return results, findings, output

