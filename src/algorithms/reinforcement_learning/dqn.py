import time
import random
import numpy as np
from collections import deque
from types import SimpleNamespace
import torch
import torch.nn as nn
import torch.optim as optim
from src.utils.puzzle import PuzzleState

# Mạng DQN với output cho từng hành động (chuyển động của từng ô trong Puzzle)
class DQNNet(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=128):
        super().__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)  # Chúng ta có nhiều hành động có thể thực hiện
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Flatten trạng thái Puzzle (3x3 thành 1D)
def flatten_state(state: PuzzleState):
    return torch.tensor(state.state.flatten(), dtype=torch.float32)

def dqn(
    initial_state: PuzzleState,
    goal_state: PuzzleState,
    max_episodes=500,          # Số episode
    max_steps=100,             # Giới hạn bước mỗi episode
    gamma=0.9,                 # Discount factor
    epsilon=0.5,               # Tỉ lệ khám phá
    buffer_size=1000,          # Kích thước Replay Buffer
    batch_size=32,             # Kích thước batch huấn luyện
    lr=1e-3,                   # Learning rate
    epsilon_min=0.05,
    epsilon_decay=0.995
):
    # Khởi tạo các yếu tố DQN
    start_time = time.perf_counter()
    state_size = 9  # 3x3 puzzle
    action_size = 4  # Giới hạn số hành động (lên, xuống, trái, phải)
    device = torch.device('cpu')
    
    # Mạng DQN
    net = DQNNet(state_size, action_size).to(device)
    target_net = DQNNet(state_size, action_size).to(device)
    target_net.load_state_dict(net.state_dict())  # Khởi tạo target_net giống net ban đầu
    optimizer = optim.Adam(net.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    replay_buffer = deque(maxlen=buffer_size)

    best_path = None
    for episode in range(max_episodes):
        state = initial_state
        path = [state]
        for step in range(max_steps):
            if state == goal_state:
                if best_path is None or len(path) < len(best_path):
                    best_path = list(path)
                break

            neighbors = state.get_neighbors()  # Trả về danh sách các trạng thái kế tiếp
            if not neighbors:
                break
            # Epsilon-greedy để chọn hành động
            if random.random() < epsilon:
                next_state = random.choice(neighbors)
            else:
                # Chọn neighbor có giá trị Q lớn nhất
                q_vals = []
                for n in neighbors:
                    with torch.no_grad():
                        q_val = net(flatten_state(n).unsqueeze(0).to(device)).max().item()
                    q_vals.append(q_val)
                max_q = max(q_vals)
                best = [n for n, qv in zip(neighbors, q_vals) if qv == max_q]
                next_state = random.choice(best)
            # Reward shaping mạnh: thưởng khi đạt goal, phạt theo Manhattan distance
            if next_state == goal_state:
                reward = 10
            else:
                reward = -next_state.manhattan_distance(goal_state)
            # Thêm vào replay buffer
            replay_buffer.append((flatten_state(state), flatten_state(next_state), reward, next_state == goal_state))
            state = next_state
            path.append(state)
            # Huấn luyện DQN
            if len(replay_buffer) >= batch_size:
                batch = random.sample(replay_buffer, batch_size)
                states, next_states, rewards, dones = zip(*batch)
                states = torch.stack(states).to(device)
                next_states = torch.stack(next_states).to(device)
                rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1).to(device)
                dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1).to(device)
                # Q-values từ mạng hiện tại
                q_values = net(states).max(1)[0].unsqueeze(1)
                with torch.no_grad():
                    next_q_values = target_net(next_states).max(1)[0].unsqueeze(1)
                # Tính toán Q-values target
                targets = rewards + gamma * next_q_values * (1 - dones)
                loss = loss_fn(q_values, targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        # Cập nhật mạng target mỗi vài episode
        if episode % 10 == 0:
            target_net.load_state_dict(net.state_dict())
        # Giảm dần epsilon để khai thác nhiều hơn
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay
    # Trả về kết quả tốt nhất
    if best_path is not None:
        elapsed_time = time.perf_counter() - start_time
        return SimpleNamespace(
            steps=len(best_path) - 1,
            path=best_path,
            elapsed_time=elapsed_time
        )
    return None
