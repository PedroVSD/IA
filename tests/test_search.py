from eight_puzzle.core.problem import EightPuzzleProblem
from eight_puzzle.heuristics import manhattan
from eight_puzzle.search import astar, bfs, dfs, greedy, ids


def test_bfs_optimal_simple():
    problem = EightPuzzleProblem((1, 2, 3, 4, 5, 6, 0, 7, 8))
    r = bfs(problem)
    assert r.solution is not None
    assert r.solution.path_cost == 2
    assert r.solution.depth == 2

def test_astar_equals_bfs_optimal():
    initial = (1, 3, 6, 5, 0, 2, 4, 7, 8)
    p = EightPuzzleProblem(initial)
    r_bfs = bfs(p)
    r_astar = astar(p)
    assert r_bfs.solution is not None and r_astar.solution is not None
    assert r_bfs.solution.path_cost == r_astar.solution.path_cost

def test_manhattan_heuristic():
    assert manhattan((1, 2, 3, 4, 5, 6, 7, 8, 0)) == 0
    assert manhattan((1, 2, 3, 4, 5, 6, 0, 7, 8)) == 2

def test_dfs_finds_solution_with_limit():
    p = EightPuzzleProblem((1, 2, 3, 4, 5, 6, 0, 7, 8))
    r = dfs(p, limit=10)
    assert r.solution is not None

def test_greedy_finds_solution():
    p = EightPuzzleProblem((1, 3, 6, 5, 0, 2, 4, 7, 8))
    r = greedy(p)
    assert r.solution is not None

def test_ids_finds_optimal():
    p = EightPuzzleProblem((1, 2, 3, 4, 5, 6, 0, 7, 8))
    r = ids(p, max_depth=10)
    assert r.solution is not None
    assert r.solution.path_cost == 2
