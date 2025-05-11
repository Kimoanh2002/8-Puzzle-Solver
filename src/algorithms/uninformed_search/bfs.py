import time
from collections import deque
from typing import Optional, Dict, List
from src.utils.puzzle import PuzzleState

class SolutionResult:
    def __init__(self, steps: int, path: List[PuzzleState], elapsed_time: float):
        self.steps = steps
        self.path = path
        self.elapsed_time = elapsed_time

def bfs(initial_state: PuzzleState, goal_state: PuzzleState) -> Optional[SolutionResult]:
    start_time = time.time()
    queue = deque([initial_state])
    parent: Dict[PuzzleState, Optional[PuzzleState]] = {initial_state: None}
    visited = set([initial_state])
    found = False
    
    while queue:
        current = queue.popleft()
        if current == goal_state:
            found = True
            break
        for neighbor in current.get_neighbors():
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    elapsed_time = time.time() - start_time
    if not found:
        return None
    # Truy vết đường đi
    path = []
    node = goal_state
    while node is not None:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    return SolutionResult(steps=len(path)-1, path=path, elapsed_time=elapsed_time)
