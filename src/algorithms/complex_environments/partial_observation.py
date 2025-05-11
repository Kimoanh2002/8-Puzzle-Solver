import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

# Giả lập: agent chỉ biết vị trí ô trống và các ô xung quanh
# Belief state là tập các trạng thái có thể xảy ra dựa trên quan sát

def partial_observation_search(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000):
    start_time = time.perf_counter()
    current_belief = {initial_state}
    path = [initial_state]
    steps = 0
    while steps < max_steps:
        # Nếu tất cả belief đều là goal thì thành công
        if all(state == goal_state for state in current_belief):
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                steps=len(path) - 1,
                path=path,
                elapsed_time=elapsed_time
            )
        # Sinh tập belief mới dựa trên quan sát (giả lập: chỉ biết các trạng thái kề)
        new_belief = set()
        for state in current_belief:
            neighbors = state.get_neighbors()
            for n in neighbors:
                new_belief.add(n)
        # Chọn một trạng thái bất kỳ từ belief mới để đi tiếp (giả lập agent chọn ngẫu nhiên)
        if not new_belief:
            break
        chosen = next(iter(new_belief))
        path.append(chosen)
        current_belief = {chosen}
        steps += 1
    return None
