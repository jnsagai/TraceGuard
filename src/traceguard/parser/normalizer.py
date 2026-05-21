from __future__ import annotations

import re


def canonicalize(text: str) -> str:
    normalized = text.strip().lower()
    normalized = re.sub(r"[^a-z0-9/%<>=.]+", "_", normalized)
    return re.sub(r"_+", "_", normalized).strip("_")


def display_clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())

