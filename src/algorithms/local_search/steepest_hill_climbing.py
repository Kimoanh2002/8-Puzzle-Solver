import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def steepest_hill_climbing(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000, restarts=20):
    for _ in range(restarts):
        current = initial_state
        path = [current]
        steps = 0
        while steps < max_steps:
            if current == goal_state:
                elapsed_time = time.perf_counter()
                return SimpleNamespace(
                    steps=len(path) - 1,
                    path=path,
                    elapsed_time=elapsed_time
                )
            neighbors = current.get_neighbors()
            if not neighbors:
                break
            # Chọn neighbor có heuristic tốt nhất (nếu có nhiều, chọn đầu tiên)
            min_h = min(s.manhattan_distance(goal_state) for s in neighbors)
            best_neighbors = [s for s in neighbors if s.manhattan_distance(goal_state) == min_h]
            if min_h >= current.manhattan_distance(goal_state):
                break
            next_state = best_neighbors[0]
            current = next_state
            path.append(current)
            steps += 1
    return None
