import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace
import copy
import numpy as np

def genetic_algorithm(initial_state: PuzzleState, goal_state: PuzzleState, population_size=100, generations=500, mutation_rate=0.1, tournament_size=5):
    def fitness(state):
        # Fitness càng nhỏ càng tốt (khoảng cách Manhattan)
        return state.manhattan_distance(goal_state)

    def random_state():
        # Sinh trạng thái ngẫu nhiên bằng cách thực hiện nhiều bước đi hợp lệ từ initial_state
        state = copy.deepcopy(initial_state)
        for _ in range(random.randint(10, 50)):
            neighbors = state.get_neighbors()
            state = random.choice(neighbors)
        return state

    def crossover(parent1, parent2):
        # Lai ghép: chọn ngẫu nhiên một nửa hàng từ mỗi cha mẹ
        size = parent1.size
        child_state = parent1.state.copy()
        row_split = random.randint(1, size-1)
        child_state[:row_split, :] = parent1.state[:row_split, :]
        child_state[row_split:, :] = parent2.state[row_split:, :]
        # Đảm bảo hợp lệ: nếu trùng số, sửa lại bằng số còn thiếu
        flat = child_state.flatten()
        unique, counts = np.unique(flat, return_counts=True)
        missing = set(range(size*size)) - set(flat)
        for val, count in zip(unique, counts):
            if count > 1:
                idxs = np.where(flat == val)[0][1:]
                for idx in idxs:
                    flat[idx] = missing.pop()
        child_state = flat.reshape((size, size))
        return PuzzleState(child_state.tolist())

    def mutate(state):
        # Đột biến: thực hiện một bước đi hợp lệ ngẫu nhiên
        neighbors = state.get_neighbors()
        if neighbors:
            return random.choice(neighbors)
        return state

    # Khởi tạo quần thể
    population = [random_state() for _ in range(population_size)]
    best_path = None
    best_fitness = float('inf')
    start_time = time.perf_counter()
    for gen in range(generations):
        # Đánh giá fitness
        population.sort(key=fitness)
        if fitness(population[0]) < best_fitness:
            best_fitness = fitness(population[0])
            best_path = [population[0]]
        if population[0] == goal_state:
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                steps=0,
                path=[population[0]],
                elapsed_time=elapsed_time
            )
        # Chọn lọc (tournament selection)
        new_population = []
        while len(new_population) < population_size:
            tournament = random.sample(population, tournament_size)
            parent1 = min(tournament, key=fitness)
            tournament = random.sample(population, tournament_size)
            parent2 = min(tournament, key=fitness)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    # Nếu không tìm được lời giải
    return None
