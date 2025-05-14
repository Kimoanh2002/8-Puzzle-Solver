import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def hill_climbing(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000):
    current = initial_state
    path = [current]
    nodes_explored = 0
    visited_states = set()
    depth = 0
    max_memory = 0
    while depth < max_steps:
        nodes_explored += 1
        state_tuple = tuple(map(tuple, current.board))
        if state_tuple in visited_states:
            break
        visited_states.add(state_tuple)
        max_memory = max(max_memory, len(visited_states))
        if current == goal_state:
            return path, nodes_explored, len(path), max_memory
        best_child = None
        best_h = current.manhattan_distance(goal_state)
        for neighbor in current.get_neighbors():
            h_child = neighbor.manhattan_distance(goal_state)
            if h_child < best_h:
                best_h = h_child
                best_child = neighbor
        if best_child is None:
            break
        current = best_child
        path.append(current)
        depth += 1
    return None
