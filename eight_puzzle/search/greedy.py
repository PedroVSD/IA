"""Busca Gulosa (Best-First com h=Manhattan)."""

from __future__ import annotations

import heapq
from itertools import count

from eight_puzzle.core.problem import EightPuzzleProblem
from eight_puzzle.heuristics import manhattan
from eight_puzzle.search.base import SearchResult, SearchStats, Timer, current_memory_mb
from eight_puzzle.core.node import Node


def greedy(
    problem: EightPuzzleProblem,
    heuristic=manhattan,
) -> SearchResult:
    timer = Timer()
    counter = count()
    root = Node(problem.initial)

    frontier: list[tuple[int, int, Node]] = []
    heapq.heappush(frontier, (heuristic(root.state), next(counter), root))
    reached: set[tuple[int, ...]] = {root.state}

    stats = SearchStats(
        nodes_generated=1, fringe_size=1, max_fringe_size=1, max_search_depth=0
    )

    while frontier:
        _, _, node = heapq.heappop(frontier)
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
                heapq.heappush(frontier, (heuristic(child.state), next(counter), child))
                stats.fringe_size = len(frontier)
                stats.max_fringe_size = max(stats.max_fringe_size, stats.fringe_size)

    stats.running_time = timer.elapsed()
    stats.memory_usage_mb = current_memory_mb()
    return SearchResult(None, stats)
