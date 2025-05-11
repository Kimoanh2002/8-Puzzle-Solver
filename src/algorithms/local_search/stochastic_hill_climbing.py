import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def stochastic_hill_climbing(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000, restarts=20):
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
            # Lọc các neighbor tốt hơn hiện tại
            better_neighbors = [s for s in neighbors if s.manhattan_distance(goal_state) < current.manhattan_distance(goal_state)]
            if not better_neighbors:
                break
            next_state = random.choice(better_neighbors)
            current = next_state
            path.append(current)
            steps += 1
    return None
