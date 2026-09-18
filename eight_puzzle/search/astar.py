"""A* (f = g + h)."""

from __future__ import annotations

import heapq
from itertools import count

from eight_puzzle.core.node import Node
from eight_puzzle.core.problem import EightPuzzleProblem
from eight_puzzle.heuristics import manhattan
from eight_puzzle.search.base import SearchResult, SearchStats, Timer, current_memory_mb


def astar(
    problem: EightPuzzleProblem,
    heuristic=manhattan,
) -> SearchResult:
    timer = Timer()
    counter = count()
    root = Node(problem.initial)

    frontier: list[tuple[int, int, Node]] = []
    heapq.heappush(frontier, (root.path_cost + heuristic(root.state), next(counter), root))
    # melhor g conhecido por estado
    best_g: dict[tuple[int, ...], int] = {root.state: 0}

    stats = SearchStats(
        nodes_generated=1, fringe_size=1, max_fringe_size=1, max_search_depth=0
    )

    while frontier:
        _, _, node = heapq.heappop(frontier)
        stats.nodes_expanded += 1

        # Se há entrada desatualizada com g pior, ignora (opcional)
        if node.path_cost > best_g.get(node.state, float("inf")):
            continue

        if problem.is_goal(node.state):
            stats.fringe_size = len(frontier)
            stats.running_time = timer.elapsed()
            stats.memory_usage_mb = current_memory_mb()
            return SearchResult(node, stats)

        for child in problem.expand(node):
            stats.nodes_generated += 1
            stats.max_search_depth = max(stats.max_search_depth, child.depth)
            if child.state not in best_g or child.path_cost < best_g[child.state]:
                best_g[child.state] = child.path_cost
                f = child.path_cost + heuristic(child.state)
                heapq.heappush(frontier, (f, next(counter), child))
                stats.fringe_size = len(frontier)
                stats.max_fringe_size = max(stats.max_fringe_size, stats.fringe_size)

    stats.running_time = timer.elapsed()
    stats.memory_usage_mb = current_memory_mb()
    return SearchResult(None, stats)
