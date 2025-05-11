import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.puzzle import PuzzleState
from src.algorithms.uninformed_search.bfs import bfs
from src.algorithms.uninformed_search.dfs import dfs
from src.algorithms.uninformed_search.ucs import ucs
from src.algorithms.uninformed_search.ids import ids
from src.algorithms.informed_search.greedy_bfs import greedy_bfs
from src.algorithms.informed_search.a_star import a_star
from src.algorithms.informed_search.ida_star import ida_star
from src.algorithms.local_search.hill_climbing import hill_climbing
from src.algorithms.local_search.genetic import genetic_algorithm
from src.algorithms.local_search.beam_search import beam_search
from src.algorithms.local_search.steepest_hill_climbing import steepest_hill_climbing
from src.algorithms.local_search.stochastic_hill_climbing import stochastic_hill_climbing
from src.algorithms.local_search.simulated import simulated_annealing
from src.algorithms.complex_environments.partial_observation import partial_observation_search
from src.algorithms.complex_environments.nondeterminism import nondeterministic_search
from src.algorithms.complex_environments.belief_state import belief_state_search
from src.algorithms.csps.backtracking import backtracking
from src.algorithms.csps.backtracking_fc import backtracking_fc
from src.algorithms.csps.min_conflicts import min_conflicts
from src.algorithms.reinforcement_learning.q_learning import q_learning
from src.algorithms.reinforcement_learning.dqn import dqn
from src.algorithms.reinforcement_learning.sarsa import sarsa
import numpy as np

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("8/15-Puzzle Solver")
        self.window.geometry("440x620")
        
        self.solution_path = []
        self.current_step = 0
        self.is_auto_playing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Label và Entry cho input
        tk.Label(self.window, text="Nhập trạng thái (cách nhau bởi dấu cách):").pack(pady=10)
        self.input_entry = tk.Entry(self.window, width=40)
        self.input_entry.pack(pady=5)
        self.input_entry.insert(0, "1 2 3 4 0 5 6 7 8")
        
        # Combobox cho thuật toán
        tk.Label(self.window, text="Chọn thuật toán:").pack(pady=10)
        self.algo_combo = ttk.Combobox(self.window, values=["BFS", "DFS", "UCS", "IDS", "Greedy BFS", "A*", "IDA*", "Hill Climbing", "Steepest Hill Climbing", "Stochastic Hill Climbing", "Simulated Annealing", "Genetic Algorithm", "Beam Search", "Partial Observation Search", "Nondeterministic Search", "Belief-State Search", "Backtracking", "Backtracking FC", "Min-Conflicts", "Q-Learning", "DQN", "SARSA"])
        self.algo_combo.current(0)
        self.algo_combo.pack(pady=5)
        
        # Frame chứa nút Bắt đầu và Chạy tự động
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        self.start_button = tk.Button(btn_frame, text="Bắt đầu", command=self.on_start)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.auto_button = tk.Button(btn_frame, text="Chạy tự động", command=self.auto_play, state=tk.DISABLED)
        self.auto_button.pack(side=tk.LEFT, padx=5)
        
        # Lưới hiển thị trạng thái puzzle
        self.grid_frame = tk.Frame(self.window, bg="#cce0f7")
        self.grid_frame.pack(pady=10)
        self.grid_buttons = []
        self.create_grid(3)  # Mặc định 3x3
        
        # Nút xem từng bước
        self.step_button = tk.Button(self.window, text="Xem từng bước", command=self.show_next_step, state=tk.DISABLED)
        self.step_button.pack(pady=5)
        
        # Text widget cho kết quả
        tk.Label(self.window, text="Kết quả:").pack(pady=10)
        self.result_text = tk.Text(self.window, height=10, width=40)
        self.result_text.pack(pady=5)
        
    def create_grid(self, size):
        # Xóa lưới cũ nếu có
        for row in self.grid_buttons:
            for btn in row:
                btn.destroy()
        self.grid_buttons = []
        for i in range(size):
            row = []
            for j in range(size):
                btn = tk.Label(self.grid_frame, text="", width=4, height=2, font=("Arial", 28), relief="ridge", bg="#7daee3", fg="#234")
                btn.grid(row=i, column=j, padx=3, pady=3)
                row.append(btn)
            self.grid_buttons.append(row)
        self.window.update()
        
    def update_grid(self, state):
        arr = state.state if hasattr(state, 'state') else state
        size = len(arr)
        if len(self.grid_buttons) != size:
            self.create_grid(size)
        for i in range(size):
            for j in range(size):
                val = arr[i][j] if isinstance(arr[i], (list, np.ndarray)) else arr[i, j]
                if val == 0:
                    self.grid_buttons[i][j]["text"] = ""
                    self.grid_buttons[i][j]["bg"] = "#3576ad"
                else:
                    self.grid_buttons[i][j]["text"] = str(val)
                    self.grid_buttons[i][j]["bg"] = "#7daee3"
        self.window.update()
        
    def on_start(self):
        self.is_auto_playing = False
        input_str = self.input_entry.get().strip()
        try:
            state_list = [int(x) for x in input_str.split()]
        except:
            messagebox.showerror("Lỗi", "Định dạng trạng thái không hợp lệ!")
            return
        n = len(state_list)
        if n not in [9, 16]:
            messagebox.showerror("Lỗi", "Chỉ hỗ trợ 8-puzzle (9 số) hoặc 15-puzzle (16 số)!")
            return
        size = int(n ** 0.5)
        try:
            initial_state = PuzzleState([state_list[i*size:(i+1)*size] for i in range(size)])
            goal_state = PuzzleState([[size * i + j + 1 if size * i + j + 1 < n else 0 for j in range(size)] for i in range(size)])
        except:
            messagebox.showerror("Lỗi", "Không thể khởi tạo trạng thái!")
            return
        self.create_grid(size)
        self.update_grid(initial_state)
        algo = self.algo_combo.get()
        if algo == "BFS":
            result = bfs(initial_state, goal_state)
        elif algo == "DFS":
            result = dfs(initial_state, goal_state)
        elif algo == "UCS":
            result = ucs(initial_state, goal_state)
        elif algo == "IDS":
            result = ids(initial_state, goal_state)
        elif algo == "Greedy BFS":
            result = greedy_bfs(initial_state, goal_state)
        elif algo == "A*":
            result = a_star(initial_state, goal_state)
        elif algo == "IDA*":
            result = ida_star(initial_state, goal_state)
        elif algo == "Hill Climbing":
            result = hill_climbing(initial_state, goal_state)
        elif algo == "Steepest Hill Climbing":
            result = steepest_hill_climbing(initial_state, goal_state)
        elif algo == "Stochastic Hill Climbing":
            result = stochastic_hill_climbing(initial_state, goal_state)
        elif algo == "Simulated Annealing":
            result = simulated_annealing(initial_state, goal_state)
        elif algo == "Genetic Algorithm":
            result = genetic_algorithm(initial_state, goal_state)
        elif algo == "Beam Search":
            result = beam_search(initial_state, goal_state)
        elif algo == "Partial Observation Search":
            result = partial_observation_search(initial_state, goal_state)
        elif algo == "Nondeterministic Search":
            result = nondeterministic_search(initial_state, goal_state)
        elif algo == "Belief-State Search":
            result = belief_state_search(initial_state, goal_state)
        elif algo == "Backtracking":
            result = backtracking(initial_state, goal_state)
        elif algo == "Backtracking FC":
            result = backtracking_fc(initial_state, goal_state)
        elif algo == "Min-Conflicts":
            result = min_conflicts(initial_state, goal_state)
        elif algo == "Q-Learning":
            result = q_learning(initial_state, goal_state)
        elif algo == "DQN":
            result = dqn(initial_state, goal_state)
        elif algo == "SARSA":
            result = sarsa(initial_state, goal_state)
        else:
            result = None
        if result is None:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Không tìm được lời giải!")
            self.step_button["state"] = tk.DISABLED
            self.auto_button["state"] = tk.DISABLED
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, 
                f"Số bước: {result.steps}\n"
                f"Thời gian: {result.elapsed_time:.4f} s\n"
                f"Đường đi: Xem từng bước hoặc Chạy tự động!")
            self.solution_path = result.path
            self.current_step = 0
            self.step_button["state"] = tk.NORMAL
            self.auto_button["state"] = tk.NORMAL
            self.update_grid(self.solution_path[0])
        
    def show_next_step(self):
        if not self.solution_path:
            return
        self.current_step += 1
        if self.current_step >= len(self.solution_path):
            self.current_step = 0
        self.update_grid(self.solution_path[self.current_step])
    
    def auto_play(self):
        if not self.solution_path or self.is_auto_playing:
            return
        self.is_auto_playing = True
        self.auto_step()
    
    def auto_step(self):
        if not self.is_auto_playing:
            return
        self.current_step += 1
        if self.current_step >= len(self.solution_path):
            self.is_auto_playing = False
            return
        self.update_grid(self.solution_path[self.current_step])
        self.window.after(500, self.auto_step)  # 500ms mỗi bước
    
    def run(self):
        self.window.mainloop()
