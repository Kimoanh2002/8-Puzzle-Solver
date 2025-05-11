import time
import heapq
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def a_star(initial_state: PuzzleState, goal_state: PuzzleState):
    start_time = time.perf_counter()
    counter = 0
    heap = [(initial_state.manhattan_distance(goal_state), 0, counter, initial_state)]  # (f, g, counter, state)
    parent = {initial_state: None}
    g_score = {initial_state: 0}
    result_path = []
    
    while heap:
        f, g, _, current = heapq.heappop(heap)
        if current == goal_state:
            break
        for neighbor in current.get_neighbors():
            tentative_g = g + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                counter += 1
                h = neighbor.manhattan_distance(goal_state)
                heapq.heappush(heap, (tentative_g + h, tentative_g, counter, neighbor))
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
