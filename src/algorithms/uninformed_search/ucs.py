import time
import heapq
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def ucs(initial_state: PuzzleState, goal_state: PuzzleState):
    if initial_state == goal_state:
        return SimpleNamespace(
            steps=0,
            path=[initial_state],
            elapsed_time=0.0
        )
    start_time = time.perf_counter()
    counter = 0
    heap = [(0, counter, initial_state)]  # (cost, counter, state)
    parent = {initial_state: None}
    cost_so_far = {initial_state: 0}
    result_path = []
    
    while heap:
        current_cost, _, current = heapq.heappop(heap)
        if current == goal_state:
            break
        for neighbor in current.get_neighbors():
            new_cost = current_cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                counter += 1
                heapq.heappush(heap, (new_cost, counter, neighbor))
    else:
        print("[UCS DEBUG] Không tìm thấy lời giải!")
        return None

    # Kiểm tra goal_state có trong parent không
    if goal_state not in parent:
        print("[UCS DEBUG] goal_state không nằm trong parent! Không thể truy vết đường đi.")
        print(f"[UCS DEBUG] Số lượng parent: {len(parent)}")
        print(f"[UCS DEBUG] goal_state: {goal_state}")
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
