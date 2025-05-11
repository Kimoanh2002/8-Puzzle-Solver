import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def beam_search(initial_state: PuzzleState, goal_state: PuzzleState, beam_width=3, max_steps=1000):
    start_time = time.perf_counter()
    current_beam = [(initial_state, [initial_state])]
    steps = 0
    visited = set()
    while steps < max_steps and current_beam:
        next_beam = []
        for state, path in current_beam:
            if state == goal_state:
                elapsed_time = time.perf_counter() - start_time
                return SimpleNamespace(
                    steps=len(path) - 1,
                    path=path,
                    elapsed_time=elapsed_time
                )
            visited.add(state)
            for neighbor in state.get_neighbors():
                if neighbor not in visited:
                    next_beam.append((neighbor, path + [neighbor]))
        # Sắp xếp theo heuristic (Manhattan distance)
        next_beam.sort(key=lambda x: x[0].manhattan_distance(goal_state))
        # Giữ lại beam_width trạng thái tốt nhất
        current_beam = next_beam[:beam_width]
        steps += 1
    return None
