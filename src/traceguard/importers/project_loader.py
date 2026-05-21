from __future__ import annotations

from pathlib import Path

import yaml

from traceguard.domain.project import Project, ResolvedProject
from traceguard.domain.requirement import Requirement
from traceguard.importers.csv_importer import import_csv_requirements
from traceguard.importers.markdown_importer import import_markdown_requirements
from traceguard.parser.atomizer import atomize_requirement


def load_project(path: Path) -> ResolvedProject:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return Project.model_validate(data).resolve_paths(path)


def load_requirements(project: ResolvedProject, *, atomize: bool = True) -> list[Requirement]:
    requirements: list[Requirement] = []
    seen: set[str] = set()
    for path in project.requirements:
        imported = _load_requirements_file(path)
        for requirement in imported:
            if requirement.id in seen:
                raise ValueError(f"Duplicate requirement ID: {requirement.id}")
            seen.add(requirement.id)
            if atomize and not requirement.atoms:
                requirement.atoms = atomize_requirement(requirement)
            requirements.append(requirement)
    return requirements


def _load_requirements_file(path: Path) -> list[Requirement]:
    if path.suffix.lower() in {".md", ".markdown"}:
        return import_markdown_requirements(path)
    if path.suffix.lower() == ".csv":
        return import_csv_requirements(path)
    raise ValueError(f"Unsupported requirements file type: {path}")

