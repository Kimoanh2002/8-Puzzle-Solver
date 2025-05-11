import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def min_conflicts(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000):
    start_time = time.perf_counter()
    current = initial_state
    path = [current]
    steps = 0
    while steps < max_steps:
        if current == goal_state:
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                steps=len(path) - 1,
                path=path,
                elapsed_time=elapsed_time
            )
        neighbors = current.get_neighbors()
        if not neighbors:
            break
        # Chọn neighbor có ít xung đột nhất (ở đây dùng manhattan_distance làm xung đột)
        min_conf = min(s.manhattan_distance(goal_state) for s in neighbors)
        best_neighbors = [s for s in neighbors if s.manhattan_distance(goal_state) == min_conf]
        next_state = random.choice(best_neighbors)
        current = next_state
        path.append(current)
        steps += 1
    return None
