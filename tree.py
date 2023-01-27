from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    name: str | None
    children: List["Node"]
