from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    project: str
    domain: str
    chunk_id: str
