import numpy as np
from collections import deque

# def is_solvable(start, end):
#     start_flat = start.flatten()
#     end_flat = end.flatten()
#     # Đếm số hoán vị (inversions) của start và end (bỏ qua số 0)
#     inv_start = sum(1 for i in range(8) for j in range(i+1, 9) if start_flat[i] != 0 and start_flat[j] != 0 and start_flat[i] > start_flat[j])
#     inv_end = sum(1 for i in range(8) for j in range(i+1, 9) if end_flat[i] != 0 and end_flat[j] != 0 and end_flat[i] > end_flat[j])
#     # Với lưới 3x3, tổng số hoán vị của start và end phải cùng chẵn/lẻ
#     return (inv_start % 2) == (inv_end % 2)

def actionHq(state: np.ndarray):
    row, col = np.argwhere(state == 0)[0]
    next_states = []
    moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]

    for dr, dc, move in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = state.copy()
            new_state[row, col], new_state[new_row, new_col] = new_state[new_row, new_col], new_state[row, col]
            next_states.append((new_state, move))
    return next_states

def DFS(start: np.ndarray, end: np.ndarray):
    # if not is_solvable(start, end):
    #     return 0, None  # Không có lời giải
    
    stack = deque()
    visited = set()
    start_tuple = tuple(start.flatten())
    end_tuple = tuple(end.flatten())
    nodes_explored = 0

    # Lưu: (trạng thái, danh sách hành động)
    stack.append((start_tuple, []))

    while stack:
        state_tuple, actions = stack.pop()
        nodes_explored += 1

        if state_tuple == end_tuple:
            return nodes_explored, actions
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        current_state = np.array(state_tuple).reshape(3, 3)
        for next_state, move in actionHq(current_state):
            next_tuple = tuple(next_state.flatten())
            if next_tuple not in visited:
                # visited.add(next_tuple)
                stack.append((next_tuple, actions + [move]))
    
    return nodes_explored, None

def reconstruct_path(start, actions):
    """Tái tạo đường đi từ danh sách hành động."""
    path = [start]
    current = start.copy()
    for move in actions:
        row, col = np.argwhere(current == 0)[0]
        if move == "Up":
            new_row, new_col = row - 1, col
        elif move == "Down":
            new_row, new_col = row + 1, col
        elif move == "Left":
            new_row, new_col = row, col - 1
        elif move == "Right":
            new_row, new_col = row, col + 1
        current[row, col], current[new_row, new_col] = current[new_row, new_col], current[row, col]
        path.append(current.copy())
    return path

if __name__ == '__main__':
    start = np.array([
        [8, 1, 3],
        [0, 2, 4],
        [7, 6, 5]
    ])
    # board=start.copy()
    end=np.array([
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
    ])
    
    nodes, actions = DFS(start, end)
    if actions:
        print(f"✅ Found solution with {len(actions)} steps. Nodes explored: {nodes}")
        path = reconstruct_path(start, actions)
        for step in path:
            print(step, "\n")
    else:
        print("❌ No solution found.")