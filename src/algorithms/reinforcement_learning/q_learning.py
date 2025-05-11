import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace
from collections import defaultdict

def q_learning(initial_state: PuzzleState, goal_state: PuzzleState, max_episodes=5000, max_steps=100, alpha=0.1, gamma=0.9, epsilon=0.2):
    start_time = time.perf_counter()
    Q = defaultdict(lambda: defaultdict(float))  # Q[state][action] = value
    actions = lambda state: state.get_neighbors()
    best_path = None
    for episode in range(max_episodes):
        state = initial_state
        path = [state]
        for step in range(max_steps):
            if state == goal_state:
                if best_path is None or len(path) < len(best_path):
                    best_path = list(path)
                break
            neighbors = actions(state)
            if not neighbors:
                break
            # Epsilon-greedy
            if random.random() < epsilon:
                next_state = random.choice(neighbors)
            else:
                # Chọn neighbor có Q-value lớn nhất (hoặc random nếu chưa có)
                q_vals = [Q[state][n] for n in neighbors]
                max_q = max(q_vals)
                best = [n for n, qv in zip(neighbors, q_vals) if qv == max_q]
                next_state = random.choice(best)
            # Reward: -1 cho mỗi bước, 0 nếu đến goal
            reward = 0 if next_state == goal_state else -1
            # Q-learning update
            next_neighbors = actions(next_state)
            max_next_q = max([Q[next_state][n] for n in next_neighbors], default=0)
            Q[state][next_state] += alpha * (reward + gamma * max_next_q - Q[state][next_state])
            state = next_state
            path.append(state)
    if best_path is not None:
        elapsed_time = time.perf_counter() - start_time
        return SimpleNamespace(
            steps=len(best_path) - 1,
            path=best_path,
            elapsed_time=elapsed_time
        )
    return None
