from typing import List
import numpy as np
from .puzzle import PuzzleState

def validate_input(state_list: List[int]) -> bool:
    """
    Kiểm tra tính hợp lệ của input puzzle
    :param state_list: Danh sách các số từ 0-8 (cho 8-puzzle) hoặc 0-15 (cho 15-puzzle)
    :return: True nếu input hợp lệ, False nếu không
    """
    # Kiểm tra độ dài input
    n = len(state_list)
    if n not in [9, 16]:  # 8-puzzle hoặc 15-puzzle
        return False
    
    # Kiểm tra các số từ 0 đến n-1
    expected_numbers = set(range(n))
    if set(state_list) != expected_numbers:
        return False
    
    # Kiểm tra số lần xuất hiện của mỗi số
    if len(set(state_list)) != n:
        return False
    
    # Chuyển đổi thành ma trận 2D
    size = int(np.sqrt(n))
    state_matrix = np.array(state_list).reshape(size, size)
    
    # Tạo PuzzleState và kiểm tra tính giải được
    puzzle_state = PuzzleState(state_matrix.tolist())
    return puzzle_state.is_solvable() 