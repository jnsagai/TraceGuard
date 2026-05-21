from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class Project(BaseModel):
    name: str
    baseline: str | None = None
    requirements: list[str] = Field(default_factory=list)
    traces: list[str] = Field(default_factory=list)
    glossary: str | None = None
    reports_dir: str = "reports"
    build_dir: str = "build"

    def resolve_paths(self, project_file: Path) -> ResolvedProject:
        root = project_file.parent
        return ResolvedProject(
            config_path=project_file,
            name=self.name,
            baseline=self.baseline,
            requirements=[root / p for p in self.requirements],
            traces=[root / p for p in self.traces],
            glossary=(root / self.glossary) if self.glossary else None,
            reports_dir=root / self.reports_dir,
            build_dir=root / self.build_dir,
        )


class ResolvedProject(BaseModel):
    config_path: Path
    name: str
    baseline: str | None
    requirements: list[Path]
    traces: list[Path]
    glossary: Path | None
    reports_dir: Path
    build_dir: Path

