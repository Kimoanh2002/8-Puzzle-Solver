from typing import List, Tuple, Optional
import numpy as np

class PuzzleState:
    def __init__(self, state: List[List[int]]):
        """
        Khởi tạo trạng thái puzzle
        :param state: Ma trận 2D biểu diễn trạng thái puzzle
        """
        self.state = np.array(state)
        self.size = len(state)
        self.empty_pos = self._find_empty()
        
    def _find_empty(self) -> Tuple[int, int]:
        """
        Tìm vị trí ô trống (số 0) trong puzzle
        :return: Tuple (row, col) chứa vị trí ô trống
        """
        return tuple(np.argwhere(self.state == 0)[0])
    
    def is_solvable(self) -> bool:
        """
        Kiểm tra xem puzzle có giải được hay không
        :return: True nếu puzzle giải được, False nếu không
        """
        # TODO: Implement solvability check
        return True  # Tạm thời luôn trả về True
    
    def get_neighbors(self) -> List['PuzzleState']:
        """
        Lấy danh sách các trạng thái kề có thể đi được
        :return: List các PuzzleState kề
        """
        neighbors = []
        row, col = self.empty_pos
        
        # Các hướng có thể di chuyển: lên, xuống, trái, phải
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Kiểm tra xem vị trí mới có hợp lệ không
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                # Tạo bản sao của trạng thái hiện tại
                new_state = self.state.copy()
                
                # Hoán đổi vị trí ô trống với ô kề
                new_state[row, col], new_state[new_row, new_col] = new_state[new_row, new_col], new_state[row, col]
                
                # Tạo trạng thái mới và thêm vào danh sách
                neighbors.append(PuzzleState(new_state.tolist()))
        
        return neighbors
    
    def manhattan_distance(self, goal: 'PuzzleState') -> int:
        """
        Tính khoảng cách Manhattan đến trạng thái đích
        :param goal: Trạng thái đích
        :return: Khoảng cách Manhattan
        """
        # TODO: Implement Manhattan distance calculation
        return 0  # Tạm thời trả về 0
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PuzzleState):
            return False
        return np.array_equal(self.state, other.state)
    
    def __hash__(self) -> int:
        return hash(self.state.tobytes())
    
    def __str__(self) -> str:
        """
        Hiển thị trạng thái dưới dạng chuỗi
        :return: Chuỗi biểu diễn trạng thái
        """
        return str(self.state)
