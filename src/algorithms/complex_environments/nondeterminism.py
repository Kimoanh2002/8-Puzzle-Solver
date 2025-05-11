import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def nondeterministic_search(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000, action_noise=0.5):
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
        # Giả lập nondeterminism: mỗi hành động có thể đi đến 1 trong nhiều neighbor (random noise)
        if random.random() < action_noise:
            # Chọn ngẫu nhiên bất kỳ neighbor nào (hành động không như ý)
            next_state = random.choice(neighbors)
        else:
            # Chọn neighbor tốt nhất (theo heuristic)
            min_h = min(s.manhattan_distance(goal_state) for s in neighbors)
            best_neighbors = [s for s in neighbors if s.manhattan_distance(goal_state) == min_h]
            next_state = random.choice(best_neighbors)
        current = next_state
        path.append(current)
        steps += 1
    return None
