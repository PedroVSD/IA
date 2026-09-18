"""Definição formal do problema 8-Puzzle."""

from __future__ import annotations

from eight_puzzle.core.node import Node
from eight_puzzle.core.state import GOAL_STATE


class EightPuzzleProblem:
    """Problema de busca: estado inicial -> estado objetivo."""

    def __init__(
        self,
        initial: tuple[int, ...] | list[int],
        goal: tuple[int, ...] | list[int] = GOAL_STATE,
    ) -> None:
        self.initial = tuple(initial)
        self.goal = tuple(goal)
        if len(self.initial) != 9 or len(self.goal) != 9:
            raise ValueError("Estado deve ter 9 posições")

    def is_goal(self, state: tuple[int, ...]) -> bool:
        return state == self.goal

    def actions(self, state: tuple[int, ...]) -> list[str]:
        idx = state.index(0)
        row, col = divmod(idx, 3)
        moves: list[str] = []
        if row > 0:
            moves.append("up")
        if row < 2:
            moves.append("down")
        if col > 0:
            moves.append("left")
        if col < 2:
            moves.append("right")
        return moves

    def result(self, state: tuple[int, ...], action: str) -> tuple[int, ...]:
        idx = state.index(0)
        swap = idx
        if action == "up":
            swap = idx - 3
        elif action == "down":
            swap = idx + 3
        elif action == "left":
            swap = idx - 1
        elif action == "right":
            swap = idx + 1
        else:
            raise ValueError(f"Ação inválida: {action}")
        lst = list(state)
        lst[idx], lst[swap] = lst[swap], lst[idx]
        return tuple(lst)

    def action_cost(
        self, state: tuple[int, ...], action: str, result: tuple[int, ...]
    ) -> int:
        return 1

    def expand(self, node: Node) -> list[Node]:
        children: list[Node] = []
        for action in self.actions(node.state):
            s_prime = self.result(node.state, action)
            cost = node.path_cost + self.action_cost(node.state, action, s_prime)
            children.append(
                Node(
                    state=s_prime,
                    parent=node,
                    action=action,
                    path_cost=cost,
                    depth=node.depth + 1,
                )
            )
        return children
