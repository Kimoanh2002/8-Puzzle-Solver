import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def belief_state_search(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000):
    start_time = time.perf_counter()
    belief = {initial_state}
    visited = set()
    came_from = {initial_state: None}
    steps = 0

    while steps < max_steps:
        # Nếu tất cả belief đều là goal thì thành công
        if any(state == goal_state for state in belief):
            # Truy ngược path
            for state in belief:
                if state == goal_state:
                    final_state = state
                    break
            path = []
            while final_state:
                path.append(final_state)
                final_state = came_from[final_state]
            path.reverse()
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                steps=len(path) - 1,
                path=path,
                elapsed_time=elapsed_time
            )

        new_belief = set()
        for state in belief:
            for neighbor in state.get_neighbors():
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = state
                    new_belief.add(neighbor)

        if not new_belief:
            break

        belief = new_belief
        steps += 1

    return None
