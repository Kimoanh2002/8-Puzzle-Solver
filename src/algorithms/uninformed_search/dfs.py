import time
from collections import deque
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def dfs(initial_state: PuzzleState, goal_state: PuzzleState, max_depth=50):
    start_time = time.perf_counter()
    stack = [(initial_state, 0)]
    parent = {initial_state: None}
    visited = set()
    found = False
    result_path = []
    
    while stack:
        current, depth = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if current == goal_state:
            found = True
            break
        if depth < max_depth:
            for neighbor in current.get_neighbors():
                if neighbor not in visited and neighbor not in parent:
                    parent[neighbor] = current
                    stack.append((neighbor, depth + 1))
    
    elapsed_time = time.perf_counter() - start_time
    if not found:
        return None
    # Truy vết đường đi
    node = goal_state
    while node is not None:
        result_path.append(node)
        node = parent[node]
    result_path.reverse()
    return SimpleNamespace(
        steps=len(result_path) - 1,
        path=result_path,
        elapsed_time=elapsed_time
    )
