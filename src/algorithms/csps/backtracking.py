import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def backtracking(initial_state: PuzzleState, goal_state: PuzzleState, max_depth=50):
    start_time = time.perf_counter()
    visited = set()
    path = []
    def dfs(state, depth):
        if state == goal_state:
            return True
        if depth > max_depth:
            return False
        visited.add(state)
        for neighbor in state.get_neighbors():
            if neighbor not in visited:
                path.append(neighbor)
                if dfs(neighbor, depth + 1):
                    return True
                path.pop()
        visited.remove(state)
        return False
    path.append(initial_state)
    found = dfs(initial_state, 0)
    if found:
        elapsed_time = time.perf_counter() - start_time
        return SimpleNamespace(
            steps=len(path) - 1,
            path=path,
            elapsed_time=elapsed_time
        )
    return None
