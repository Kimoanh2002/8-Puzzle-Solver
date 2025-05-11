import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def dls(current, goal_state, depth, parent, visited):
    if current == goal_state:
        return True
    if depth == 0:
        return False
    visited.add(current)
    for neighbor in current.get_neighbors():
        if neighbor not in visited:
            parent[neighbor] = current
            found = dls(neighbor, goal_state, depth - 1, parent, visited)
            if found:
                return True
    return False

def ids(initial_state: PuzzleState, goal_state: PuzzleState, max_depth=50):
    start_time = time.perf_counter()
    for depth in range(max_depth + 1):
        parent = {initial_state: None}
        visited = set()
        found = dls(initial_state, goal_state, depth, parent, visited)
        if found:
            # Truy vết đường đi
            result_path = []
            node = goal_state
            while node is not None:
                result_path.append(node)
                node = parent.get(node)
            result_path.reverse()
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                steps=len(result_path) - 1,
                path=result_path,
                elapsed_time=elapsed_time
            )
    return None
