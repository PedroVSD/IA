"""Heurísticas para busca informada."""

from __future__ import annotations

from eight_puzzle.core.node import Node


def manhattan(state: tuple[int, ...]) -> int:
    """Distância de Manhattan (admissível e consistente)."""
    dist = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        r, c = divmod(idx, 3)
        gr, gc = divmod(val - 1, 3)
        dist += abs(r - gr) + abs(c - gc)
    return dist


def misplaced_tiles(state: tuple[int, ...], goal: tuple[int, ...] | None = None) -> int:
    from eight_puzzle.core.state import GOAL_STATE

    g = goal or GOAL_STATE
    return sum(1 for a, b in zip(state, g) if a != 0 and a != b)


def h(node: Node) -> int:
    """Atalho compatível com código legado: h(node) -> manhattan."""
    return manhattan(node.state)
