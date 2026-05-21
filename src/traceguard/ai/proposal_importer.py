from __future__ import annotations

import json
from pathlib import Path

from traceguard.ai.schema import AIProposal


def load_ai_proposal(path: Path) -> AIProposal:
    return AIProposal.model_validate(json.loads(path.read_text(encoding="utf-8")))

