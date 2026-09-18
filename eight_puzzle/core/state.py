"""Representação imutável do estado do 8-Puzzle."""

from __future__ import annotations

GOAL_STATE: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 0)
BOARD_SIZE = 3


def tuple_to_matrix(state: tuple[int, ...]) -> list[list[int]]:
    """Converte tupla de 9 elementos para matriz 3x3 (útil para impressão)."""
    return [list(state[i * 3 : (i + 1) * 3]) for i in range(3)]


def matrix_to_tuple(matrix: list[list[int]]) -> tuple[int, ...]:
    """Converte matriz 3x3 para tupla."""
    return tuple(v for row in matrix for v in row)


def is_solvable(state: tuple[int, ...]) -> bool:
    """Verifica solubilidade via contagem de inversões (grade ímpar)."""
    inv = 0
    nums = [x for x in state if x != 0]
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                inv += 1
    return inv % 2 == 0
