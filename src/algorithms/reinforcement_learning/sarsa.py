import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace
from collections import defaultdict

def sarsa(initial_state: PuzzleState, goal_state: PuzzleState, max_episodes=1000, max_steps=100, alpha=0.1, gamma=0.9, epsilon=0.2):
    start_time = time.perf_counter()
    Q = defaultdict(lambda: defaultdict(float))  # Q[state][action] = value
    actions = lambda state: state.get_neighbors()
    best_path = None
    for episode in range(max_episodes):
        state = initial_state
        path = [state]
        neighbors = actions(state)
        if not neighbors:
            continue
        # Chọn hành động đầu tiên
        if random.random() < epsilon:
            next_state = random.choice(neighbors)
        else:
            q_vals = [Q[state][n] for n in neighbors]
            max_q = max(q_vals)
            best = [n for n, qv in zip(neighbors, q_vals) if qv == max_q]
            next_state = random.choice(best)
        for step in range(max_steps):
            if state == goal_state:
                if best_path is None or len(path) < len(best_path):
                    best_path = list(path)
                break
            reward = 0 if next_state == goal_state else -1
            next_neighbors = actions(next_state)
            if not next_neighbors:
                Q[state][next_state] += alpha * (reward - Q[state][next_state])
                break
            # Chọn hành động tiếp theo
            if random.random() < epsilon:
                next_next_state = random.choice(next_neighbors)
            else:
                q_vals = [Q[next_state][n] for n in next_neighbors]
                max_q = max(q_vals)
                best = [n for n, qv in zip(next_neighbors, q_vals) if qv == max_q]
                next_next_state = random.choice(best)
            # SARSA update
            Q[state][next_state] += alpha * (reward + gamma * Q[next_state][next_next_state] - Q[state][next_state])
            state = next_state
            next_state = next_next_state
            path.append(state)
    if best_path is not None:
        elapsed_time = time.perf_counter() - start_time
        return SimpleNamespace(
            steps=len(best_path) - 1,
            path=best_path,
            elapsed_time=elapsed_time
        )
    return None
