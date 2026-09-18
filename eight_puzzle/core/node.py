"""Node dataclass para árvore de busca."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    state: tuple[int, ...]
    parent: Optional[Node] = field(default=None, repr=False)
    action: Optional[str] = None
    path_cost: int = 0
    depth: int = 0

    def path(self) -> list[Node]:
        """Reconstrói caminho da raiz até este nó."""
        node: Optional[Node] = self
        result: list[Node] = []
        while node is not None:
            result.append(node)
            node = node.parent
        result.reverse()
        return result

    def actions(self) -> list[str]:
        """Sequência de ações da raiz até aqui."""
        return [n.action for n in self.path()[1:] if n.action is not None]
