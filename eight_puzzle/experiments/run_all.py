"""Benchmark unificado: roda BFS, DFS, IDS, Greedy e A*."""

from __future__ import annotations

import argparse

from eight_puzzle.core.problem import EightPuzzleProblem
from eight_puzzle.core.state import is_solvable
from eight_puzzle.search import astar, bfs, dfs, greedy, ids
from eight_puzzle.utils import print_solution, print_stats

DEFAULT_INITIAL = (1, 3, 6, 5, 0, 2, 4, 7, 8)
DEFAULT_GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Casos documentados em eight_puzzle.py
BENCHMARK_CASES: dict[str, tuple[int, ...]] = {
    "facil": (1, 3, 6, 5, 0, 2, 4, 7, 8),
    "medio": (7, 4, 0, 1, 2, 5, 6, 8, 3),
    "dificil": (0, 5, 1, 6, 4, 3, 8, 2, 7),
    "extremo": (8, 7, 6, 5, 4, 3, 2, 1, 0),
}


def parse_state(s: str) -> tuple[int, ...]:
    parts = s.replace(" ", ",").split(",")
    nums = tuple(int(x) for x in parts if x.strip() != "")
    if len(nums) != 9:
        raise ValueError("Estado deve ter 9 números separados por vírgula")
    return nums


def run_case(initial: tuple[int, ...], goal: tuple[int, ...] = DEFAULT_GOAL) -> None:
    if not is_solvable(initial):
        print(f"Aviso: estado {initial} pode ser insolúvel (inversões ímpares).")
    problem = EightPuzzleProblem(initial, goal)

    algos = [
        ("BFS", lambda p: bfs(p)),
        ("DFS (limite=50)", lambda p: dfs(p, limit=50)),
        ("IDS (max_depth=50)", lambda p: ids(p, max_depth=50)),
        ("Gulosa (Manhattan)", lambda p: greedy(p)),
        ("A* (Manhattan)", lambda p: astar(p)),
    ]

    for name, fn in algos:
        print(f"\n{'='*10} {name} {'='*10}")
        result = fn(problem)
        print_solution(result.solution)
        print_stats(result.stats)


def main() -> None:
    parser = argparse.ArgumentParser(description="8-Puzzle solver benchmark")
    parser.add_argument("--initial", type=str, help="Estado inicial: '1,3,6,5,0,2,4,7,8'")
    parser.add_argument("--case", type=str, choices=list(BENCHMARK_CASES.keys()), help="Caso pré-definido")
    args = parser.parse_args()

    if args.case:
        run_case(BENCHMARK_CASES[args.case])
    elif args.initial:
        run_case(parse_state(args.initial))
    else:
        run_case(DEFAULT_INITIAL)


if __name__ == "__main__":
    main()
