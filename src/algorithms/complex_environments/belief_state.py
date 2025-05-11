import time
from src.utils.puzzle import PuzzleState
from types import SimpleNamespace

def belief_state_search(initial_state: PuzzleState, goal_state: PuzzleState, max_steps=1000):
    start_time = time.perf_counter()
    belief = {initial_state}
    path = [initial_state]
    steps = 0
    while steps < max_steps:
        # Nếu tất cả belief đều là goal thì thành công
        if all(state == goal_state for state in belief):
            elapsed_time = time.perf_counter() - start_time
            return SimpleNamespace(
                steps=len(path) - 1,
                path=path,
                elapsed_time=elapsed_time
            )
        # Mở rộng belief: tập hợp tất cả neighbor của mọi trạng thái trong belief
        new_belief = set()
        for state in belief:
            neighbors = state.get_neighbors()
            for n in neighbors:
                new_belief.add(n)
        if not new_belief:
            break
        # Chọn một trạng thái bất kỳ từ belief mới để đi tiếp (giả lập agent chọn ngẫu nhiên)
        chosen = next(iter(new_belief))
        path.append(chosen)
        belief = {chosen}
        steps += 1
    return None
