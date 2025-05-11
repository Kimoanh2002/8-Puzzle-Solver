import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def ida_star(initial_state: PuzzleState, goal_state: PuzzleState, max_depth=100):
    start_time = time.perf_counter()
    threshold = initial_state.manhattan_distance(goal_state)
    path = [initial_state]
    parent = {initial_state: None}
    
    def search(node, g, threshold, parent, visited):
        f = g + node.manhattan_distance(goal_state)
        if f > threshold:
            return f, None
        if node == goal_state:
            return True, path.copy()
        min_threshold = float('inf')
        visited.add(node)
        for neighbor in node.get_neighbors():
            if neighbor not in visited:
                parent[neighbor] = node
                path.append(neighbor)
                t, result_path = search(neighbor, g + 1, threshold, parent, visited)
                if t is True:
                    return True, result_path
                if t < min_threshold:
                    min_threshold = t
                path.pop()
        visited.remove(node)
        return min_threshold, None
    
    for _ in range(max_depth):
        visited = set()
        t, result_path = search(initial_state, 0, threshold, parent, visited)
        if t is True:
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                steps=len(result_path) - 1,
                path=result_path,
                elapsed_time=elapsed_time
            )
        if t == float('inf'):
            break
        threshold = t
    return None
