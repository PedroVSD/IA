"""Busca por Aprofundamento Iterativo (IDS) via DFS limitada."""

from __future__ import annotations

from eight_puzzle.core.problem import EightPuzzleProblem
from eight_puzzle.search.base import SearchResult, SearchStats, Timer, current_memory_mb
from eight_puzzle.search.dfs import dfs


def ids(problem: EightPuzzleProblem, max_depth: int = 100) -> SearchResult:
    timer = Timer()
    total_generated = 0
    total_expanded = 0
    max_fringe = 0
    max_depth_reached = 0

    last_stats: SearchStats | None = None
    for depth in range(max_depth + 1):
        result = dfs(problem, limit=depth)
        last_stats = result.stats
        total_generated += result.stats.nodes_generated
        total_expanded += result.stats.nodes_expanded
        max_fringe = max(max_fringe, result.stats.max_fringe_size)
        max_depth_reached = max(max_depth_reached, result.stats.max_search_depth)

        if result.solution is not None:
            stats = SearchStats(
                nodes_generated=total_generated,
                nodes_expanded=total_expanded,
                fringe_size=result.stats.fringe_size,
                max_fringe_size=max_fringe,
                max_search_depth=max_depth_reached,
                running_time=timer.elapsed(),
                memory_usage_mb=current_memory_mb(),
            )
            return SearchResult(result.solution, stats)

    stats = SearchStats(
        nodes_generated=total_generated,
        nodes_expanded=total_expanded,
        fringe_size=0,
        max_fringe_size=max_fringe,
        max_search_depth=max_depth_reached,
        running_time=timer.elapsed(),
        memory_usage_mb=current_memory_mb(),
    )
    return SearchResult(None, stats)
