"""Busca em Profundidade (DFS) iterativa com limite."""

from __future__ import annotations

from eight_puzzle.core.node import Node
from eight_puzzle.core.problem import EightPuzzleProblem
from eight_puzzle.search.base import SearchResult, SearchStats, Timer, current_memory_mb


def dfs(problem: EightPuzzleProblem, limit: int | None = 100) -> SearchResult:
    timer = Timer()
    root = Node(problem.initial)
    stack: list[Node] = [root]
    reached: set[tuple[int, ...]] = {root.state}

    stats = SearchStats(
        nodes_generated=1, fringe_size=1, max_fringe_size=1, max_search_depth=0
    )

    while stack:
        stats.max_fringe_size = max(stats.max_fringe_size, len(stack))
        node = stack.pop()
        stats.nodes_expanded += 1

        if problem.is_goal(node.state):
            stats.fringe_size = len(stack)
            stats.running_time = timer.elapsed()
            stats.memory_usage_mb = current_memory_mb()
            return SearchResult(node, stats)

        if limit is None or node.depth < limit:
            for child in reversed(problem.expand(node)):
                stats.nodes_generated += 1
                stats.max_search_depth = max(stats.max_search_depth, child.depth)
                if child.state not in reached:
                    reached.add(child.state)
                    stack.append(child)
                    stats.fringe_size = len(stack)

    stats.running_time = timer.elapsed()
    stats.memory_usage_mb = current_memory_mb()
    stats.fringe_size = 0
    return SearchResult(None, stats)
