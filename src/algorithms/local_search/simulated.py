import time
import random
import math
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def simulated_annealing(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000, T_start=1.0, T_end=1e-3, alpha=0.995):
    start_time = time.perf_counter()
    current = initial_state
    path = [current]
    T = T_start
    steps = 0
    while steps < max_steps and T > T_end:
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
        next_state = random.choice(neighbors)
        delta = next_state.manhattan_distance(goal_state) - current.manhattan_distance(goal_state)
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = next_state
            path.append(current)
        T *= alpha
        steps += 1
    return None
