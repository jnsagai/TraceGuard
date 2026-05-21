from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
import yaml
from rich.console import Console

from traceguard.checker import run_check
from traceguard.importers.project_loader import load_project, load_requirements
from traceguard.parser.atomizer import atomize_requirement
from traceguard.reporting.csv_report import write_csv_report
from traceguard.reporting.evidence_json import write_evidence_json
from traceguard.reporting.html_report import write_html_report
from traceguard.reporting.markdown_report import write_markdown_report
from traceguard.rules.trace_rules import load_trace_links, validate_trace_links

app = typer.Typer(help="Deterministic requirements derivation coverage checker.")
console = Console()


@app.command()
def init(path: Annotated[Path, typer.Argument(help="Project directory")] = Path(".")) -> None:
    """Create a TraceGuard project skeleton."""
    path.mkdir(parents=True, exist_ok=True)
    for directory in ("requirements", "traces", "reports", "build"):
        (path / directory).mkdir(exist_ok=True)
    config = {
        "name": path.resolve().name,
        "baseline": "draft",
        "requirements": ["requirements/system.md"],
        "traces": ["traces/system_to_sw.yaml"],
        "glossary": "glossary.yaml",
        "reports_dir": "reports",
        "build_dir": "build",
    }
    (path / "traceguard.yaml").write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    (path / "glossary.yaml").write_text("terms: {}\n", encoding="utf-8")
    (path / "requirements" / "system.md").write_text("# Requirements\n", encoding="utf-8")
    (path / "traces" / "system_to_sw.yaml").write_text("links: []\n", encoding="utf-8")
    console.print(f"Created TraceGuard project at {path}")


@app.command()
def validate(project: Annotated[Path, typer.Option("--project")] = Path("traceguard.yaml")) -> None:
    """Validate project inputs."""
    resolved = load_project(project)
    requirements = load_requirements(resolved)
    links = load_trace_links(resolved.traces)
    findings = validate_trace_links(requirements, links)
    if findings:
        for finding in findings:
            console.print(f"[red]{finding.code}[/red] {finding.message}")
        raise typer.Exit(1)
    console.print("Validation passed.")


@app.command()
def atomize(
    input: Annotated[Path, typer.Option("--input")],
    output: Annotated[Path, typer.Option("--output")],
) -> None:
    """Atomize requirements from a Markdown or CSV input file."""
    from traceguard.importers.project_loader import _load_requirements_file

    requirements = _load_requirements_file(input)
    payload = []
    for requirement in requirements:
        atoms = atomize_requirement(requirement)
        payload.append(
            {
                "requirement_id": requirement.id,
                "atoms": [atom.model_dump(mode="json") for atom in atoms],
            }
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    console.print(f"Wrote atoms to {output}")


@app.command()
def check(project: Annotated[Path, typer.Option("--project")] = Path("traceguard.yaml")) -> None:
    """Run deterministic coverage checks."""
    results, findings, output = run_check(project)
    console.print(f"Wrote evidence to {output}")
    console.print(f"Coverage results: {len(results)}; findings: {len(findings)}")


@app.command()
def report(
    project: Annotated[Path, typer.Option("--project")] = Path("traceguard.yaml"),
    format: Annotated[str, typer.Option("--format")] = "markdown",
) -> None:
    """Generate a Markdown, CSV, JSON, or HTML report."""
    resolved = load_project(project)
    results, findings, _ = run_check(project)
    if format == "markdown":
        output = resolved.reports_dir / "coverage.md"
        write_markdown_report(output, resolved.name, resolved.baseline, results, findings)
    elif format == "csv":
        output = resolved.reports_dir / "coverage.csv"
        write_csv_report(output, results)
    elif format == "json":
        output = resolved.reports_dir / "evidence.json"
        write_evidence_json(output, resolved.name, resolved.baseline, results, findings)
    elif format == "html":
        output = resolved.reports_dir / "coverage.html"
        requirements = load_requirements(resolved)
        links = load_trace_links(resolved.traces)
        write_html_report(
            output,
            resolved.name,
            resolved.baseline,
            results,
            findings,
            requirements=requirements,
            trace_links=links,
        )
    else:
        raise typer.BadParameter("format must be markdown, csv, json, or html")
    console.print(f"Wrote {format} report to {output}")


@app.command()
def explain(
    parent: Annotated[str, typer.Option("--parent")],
    atom: Annotated[str, typer.Option("--atom")],
    project: Annotated[Path, typer.Option("--project")] = Path("traceguard.yaml"),
) -> None:
    """Explain one coverage result."""
    results, _, _ = run_check(project)
    for result in results:
        if result.parent_requirement_id == parent and result.parent_atom_id == atom:
            console.print(result.model_dump_json(indent=2))
            return
    console.print(f"No result for {parent} {atom}")
    raise typer.Exit(1)


@app.command(name="import")
def import_command() -> None:
    """Placeholder for future tool imports."""
    console.print("Import connectors are planned after the MVP.")


@app.command(name="export")
def export_command() -> None:
    """Placeholder for future tool exports."""
    console.print("Export connectors are planned after the MVP.")


if __name__ == "__main__":
    app()
