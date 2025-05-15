import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace
from heapq import heappush, heappop

def state_to_tuple(state: PuzzleState):
    return tuple(tuple(row) for row in state.state)

def partial_observation_search(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000):
    start_time = time.perf_counter()
    
    current_belief = [(initial_state, [initial_state])]
    visited = set()
    steps = 0

    while steps < max_steps:
        for state, path in current_belief:
            if state == goal_state:
                elapsed_time = time.perf_counter() - start_time
                return SimpleNamespace(
                    steps=len(path) - 1,
                    path=path,
                    elapsed_time=elapsed_time
                )

        new_belief = []
        for state, path in current_belief:
            for neighbor in state.get_neighbors():
                state_hash = state_to_tuple(neighbor)
                if state_hash not in visited:
                    visited.add(state_hash)
                    new_belief.append((neighbor, path + [neighbor]))

        if not new_belief:
            break

        new_belief.sort(key=lambda x: x[0].manhattan_distance(goal_state))
        current_belief = [new_belief[0]]
        steps += 1

    return None