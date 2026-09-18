"""Estruturas comuns de resultado/estatísticas."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Optional

import psutil

from eight_puzzle.core.node import Node


@dataclass
class SearchStats:
    nodes_generated: int = 0
    nodes_expanded: int = 0
    fringe_size: int = 0
    max_fringe_size: int = 0
    max_search_depth: int = 0
    running_time: float = 0.0
    memory_usage_mb: float = 0.0

    def to_dict(self) -> dict:
        return {
            "nodes_generated": self.nodes_generated,
            "nodes_expanded": self.nodes_expanded,
            "fringe_size": self.fringe_size,
            "max_fringe_size": self.max_fringe_size,
            "max_search_depth": self.max_search_depth,
            "running_time": self.running_time,
            "memory_usage_mb": self.memory_usage_mb,
        }


@dataclass
class SearchResult:
    solution: Optional[Node]
    stats: SearchStats


class Timer:
    def __init__(self) -> None:
        self._start = time.time()

    def elapsed(self) -> float:
        return time.time() - self._start


def current_memory_mb() -> float:
    return psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
