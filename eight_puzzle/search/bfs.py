"""Busca em Largura (BFS)."""

from __future__ import annotations

from collections import deque

from eight_puzzle.core.node import Node
from eight_puzzle.core.problem import EightPuzzleProblem
from eight_puzzle.search.base import SearchResult, SearchStats, Timer, current_memory_mb


def bfs(problem: EightPuzzleProblem) -> SearchResult:
    timer = Timer()
    root = Node(problem.initial)
    frontier: deque[Node] = deque([root])
    reached: set[tuple[int, ...]] = {root.state}

    stats = SearchStats(
        nodes_generated=1, fringe_size=1, max_fringe_size=1, max_search_depth=0
    )

    while frontier:
        stats.max_fringe_size = max(stats.max_fringe_size, len(frontier))
        node = frontier.popleft()
        stats.nodes_expanded += 1

        if problem.is_goal(node.state):
            stats.fringe_size = len(frontier)
            stats.running_time = timer.elapsed()
            stats.memory_usage_mb = current_memory_mb()
            return SearchResult(node, stats)

        for child in problem.expand(node):
            stats.nodes_generated += 1
            stats.max_search_depth = max(stats.max_search_depth, child.depth)
            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)
                stats.fringe_size = len(frontier)

    stats.running_time = timer.elapsed()
    stats.memory_usage_mb = current_memory_mb()
    stats.fringe_size = 0
    return SearchResult(None, stats)
