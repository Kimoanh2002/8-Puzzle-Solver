import time
import random
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace
import copy
import numpy as np

def genetic_algorithm(initial_state: PuzzleState, goal_state: PuzzleState, population_size=100, generations=500, mutation_rate=0.1, tournament_size=5, max_path_length=50):
    if not initial_state.is_solvable():
        return SimpleNamespace(
            solved=False,
            steps=None,
            path=None,
            elapsed_time=0.0
        )

    def fitness(path):
        # Fitness càng nhỏ càng tốt (khoảng cách Manhattan của trạng thái cuối)
        return path[-1].manhattan_distance(goal_state) + len(path)  # Ưu tiên path ngắn hơn nếu cùng heuristic

    def random_path():
        # Sinh path ngẫu nhiên từ initial_state
        state = copy.deepcopy(initial_state)
        path = [state]
        for _ in range(random.randint(10, max_path_length)):
            neighbors = state.get_neighbors()
            next_state = random.choice(neighbors)
            if next_state in path:
                break  # tránh lặp vô hạn
            path.append(next_state)
            state = next_state
            if state == goal_state:
                break
        return path

    def crossover(path1, path2):
        # Lai ghép hai path tại điểm cắt ngẫu nhiên
        cut1 = random.randint(1, len(path1)-1) if len(path1) > 1 else 1
        cut2 = random.randint(1, len(path2)-1) if len(path2) > 1 else 1
        new_path = path1[:cut1]
        state = new_path[-1]
        for s in path2[cut2:]:
            if s in new_path:
                break
            # chỉ thêm neighbor hợp lệ
            if s in state.get_neighbors():
                new_path.append(s)
                state = s
            else:
                break
            if state == goal_state:
                break
        return new_path

    def mutate(path):
        # Đột biến: thêm một bước đi hợp lệ vào cuối path
        state = path[-1]
        neighbors = [n for n in state.get_neighbors() if n not in path]
        if neighbors:
            path = path + [random.choice(neighbors)]
        return path

    # Khởi tạo quần thể
    population = [random_path() for _ in range(population_size)]
    start_time = time.perf_counter()
    for gen in range(generations):
        # Đánh giá fitness
        population.sort(key=fitness)
        best_path = population[0]
        if best_path[-1] == goal_state:
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                solved=True,
                steps=len(best_path)-1,
                path=best_path,
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
    elapsed_time = time.perf_counter() - start_time
    return SimpleNamespace(
        solved=False,
        steps=None,
        path=None,
        elapsed_time=elapsed_time
    )
