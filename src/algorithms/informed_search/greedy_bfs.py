import time
import heapq
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def greedy_bfs(initial_state: PuzzleState, goal_state: PuzzleState):
    start_time = time.perf_counter()
    counter = 0
    heap = [(initial_state.manhattan_distance(goal_state), counter, initial_state)]  # (heuristic, counter, state)
    parent = {initial_state: None}
    visited = set()
    result_path = []
    
    while heap:
        _, _, current = heapq.heappop(heap)
        if current == goal_state:
            break
        visited.add(current)
        for neighbor in current.get_neighbors():
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                counter += 1
                h = neighbor.manhattan_distance(goal_state)
                heapq.heappush(heap, (h, counter, neighbor))
    else:
        return None
    # Truy vết đường đi
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
