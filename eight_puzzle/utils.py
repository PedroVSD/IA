"""Utilitários de impressão e formatação."""

from __future__ import annotations

from typing import Optional

from eight_puzzle.core.node import Node
from eight_puzzle.search.base import SearchStats


def format_state(state: tuple[int, ...]) -> str:
    rows = []
    for i in range(0, 9, 3):
        rows.append(" ".join(str(x) if x != 0 else "_" for x in state[i : i + 3]))
    return "\n".join(rows)


def print_state(state: tuple[int, ...]) -> None:
    print(format_state(state))
    print()


def print_solution(node: Optional[Node]) -> None:
    if node is None:
        print("Falha na busca.")
        return
    path = node.path()
    print(f"Solução encontrada em {len(path) - 1} passos:")
    for n in path:
        marker = f" <- {n.action}" if n.action else " (inicial)"
        print(f"{marker}")
        print_state(n.state)


def print_stats(stats: SearchStats) -> None:
    d = stats.to_dict()
    print(f"Tempo: {d['running_time']:.4f}s")
    print(f"Nós gerados: {d['nodes_generated']}")
    print(f"Nós expandidos: {d['nodes_expanded']}")
    print(f"Fronteira final: {d['fringe_size']}")
    print(f"Fronteira máxima: {d['max_fringe_size']}")
    print(f"Profundidade máxima: {d['max_search_depth']}")
    print(f"Uso de memória: {d['memory_usage_mb']:.2f} MB")


def path_actions(node: Optional[Node]) -> list[str]:
    if node is None:
        return []
    return node.actions()
