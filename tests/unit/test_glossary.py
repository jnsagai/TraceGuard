from pathlib import Path

from traceguard.parser.glossary import Glossary


def test_glossary_resolves_exact_and_alias(tmp_path: Path) -> None:
    path = tmp_path / "glossary.yaml"
    path.write_text(
        """
terms:
  vehicle_motion_controller:
    type: system_element
    aliases:
      - VMC
""",
        encoding="utf-8",
    )

    glossary = Glossary.from_yaml(path)

    assert glossary.resolve("vehicle_motion_controller").canonical == "vehicle_motion_controller"
    assert glossary.resolve("VMC").canonical == "vehicle_motion_controller"


def test_glossary_detects_unknown_and_ambiguous_alias(tmp_path: Path) -> None:
    path = tmp_path / "glossary.yaml"
    path.write_text(
        """
terms:
  alpha:
    type: system
    aliases: [shared]
  beta:
    type: system
    aliases: [shared]
""",
        encoding="utf-8",
    )

    glossary = Glossary.from_yaml(path)

    assert glossary.resolve("missing").status == "unknown"
    assert glossary.resolve("shared").status == "ambiguous"
    assert glossary.validate_no_ambiguous_aliases() == ["shared"]

