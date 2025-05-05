import heapq
import time
from copy import deepcopy
# from itertools import permutations
import random
# import multiprocessing as mp
# from functools import partial

# Hàm tính số lần nghịch đảo
def inversion_count(state):
    flat = [state[i][j] for i in range(3) for j in range(3) if state[i][j] != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions

# Hàm kiểm tra tính khả thi
def is_solvable(state, goal):
    state_inversions = inversion_count(state)
    goal_inversions = inversion_count(goal)
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                state_blank_row, state_blank_col = i, j
            if goal[i][j] == 0:
                goal_blank_row, goal_blank_col = i, j
    blank_taxicab = abs(state_blank_row - goal_blank_row) + abs(state_blank_col - goal_blank_col)
    return (state_inversions % 2 + blank_taxicab % 2) % 2 == (goal_inversions % 2)

# Hàm tính heuristic (Manhattan Distance + Linear Conflict)
def heuristic(state, goal):
    distance = 0
    # Manhattan Distance
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                continue
            for m in range(3):
                for n in range(3):
                    if goal[m][n] == state[i][j]:
                        distance += abs(i - m) + abs(j - n)
    
    # Linear Conflict
    conflict = 0
    for i in range(3):
        row_conflict = []
        for j in range(3):
            if state[i][j] == 0:
                continue
            for m in range(3):
                if goal[i][m] == state[i][j]:
                    row_conflict.append((state[i][j], j, m))
        for k in range(len(row_conflict)):
            for l in range(k + 1, len(row_conflict)):
                val1, pos1, goal_pos1 = row_conflict[k]
                val2, pos2, goal_pos2 = row_conflict[l]
                if pos1 < pos2 and goal_pos1 > goal_pos2:
                    conflict += 2
        col_conflict = []
        for j in range(3):
            if state[j][i] == 0:
                continue
            for m in range(3):
                if goal[m][i] == state[j][i]:
                    col_conflict.append((state[j][i], j, m))
        for k in range(len(col_conflict)):
            for l in range(k + 1, len(col_conflict)):
                val1, pos1, goal_pos1 = col_conflict[k]
                val2, pos2, goal_pos2 = col_conflict[l]
                if pos1 < pos2 and goal_pos1 > goal_pos2:
                    conflict += 2
    
    return distance + conflict

# Hàm lấy các trạng thái kế tiếp
def get_neighbors(state):
    neighbors = []
    x, y = None, None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j
                break
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = deepcopy(state)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

# Hàm in trạng thái
def print_state(state):
    for row in state:
        print(row)
    print()

# Thuật toán A*
def a_star(start, goal, max_nodes=10000):
    open_list = [(0, 0, start, [start])]
    closed_list = set()
    nodes_explored = 0
    
    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        nodes_explored += 1
        if nodes_explored > max_nodes:
            return None, None, nodes_explored
        
        current_tuple = tuple(tuple(row) for row in current)
        if current_tuple in closed_list:
            continue
        
        if current == goal:
            return path, g, nodes_explored
        
        closed_list.add(current_tuple)
        
        for neighbor in get_neighbors(current):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple in closed_list:
                continue
            g_new = g + 1
            h_new = heuristic(neighbor, goal)
            f_new = g_new + h_new
            heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))
    
    return None, None, nodes_explored

# Hàm giải CSP với sampling
def solve_csp(partial_state, unknown_positions, goal_state, max_states=50, sample_size=1000):
    used_values = set()
    for i in range(3):
        for j in range(3):
            if partial_state[i][j] != '?':
                used_values.add(partial_state[i][j])
    
    all_values = {0, 1, 2, 3, 4, 5, 6, 7, 8}
    available_values = list(all_values - used_values)
    
    possible_states = []
    for _ in range(sample_size):
        perm = random.sample(available_values, len(unknown_positions))
        new_state = deepcopy(partial_state)
        for idx, (i, j) in enumerate(unknown_positions):
            new_state[i][j] = perm[idx]
        if is_solvable(new_state, goal_state):
            possible_states.append((heuristic(new_state, goal_state), new_state))
    
    # Sort by heuristic and limit to max_states
    possible_states.sort()
    return [state for _, state in possible_states[:max_states]]

# Hàm chạy A* cho một trạng thái (dùng cho song song hóa)
def run_a_star(state, goal, max_nodes=10000):
    path, cost, nodes = a_star(state, goal, max_nodes)
    return path, cost, nodes

# Hàm chính
# Hàm chính (không dùng multiprocessing)
def solve_partial_8puzzle(partial_state, goal_state, max_csp_states=50, max_nodes_per_state=10000):
    start_time = time.time()
    
    # Tìm các vị trí không biết
    unknown_positions = []
    for i in range(3):
        for j in range(3):
            if partial_state[i][j] == '?':
                unknown_positions.append((i, j))
    
    # Giải CSP để tìm trạng thái ban đầu khả thi
    possible_states = solve_csp(partial_state, unknown_positions, goal_state, max_csp_states)
    # print(f"Số trạng thái ban đầu khả thi: {len(possible_states)}")
    
    # Chạy A* tuần tự
    best_path = None
    best_cost = float('inf')
    total_nodes_explored = 0
    
    for state in possible_states:
        path, cost, nodes = a_star(state, goal_state, max_nodes_per_state)
        total_nodes_explored += nodes
        if path and (cost is not None) and cost < best_cost:
            best_cost = cost
            best_path = path
    
    end_time = time.time()
    
    # In kết quả
    if best_path:
        # print("Đã tìm thấy lời giải!")
        # print(f"Thời gian chạy: {end_time - start_time:.4f} giây")
        # print(f"Tổng số node đã khám phá: {total_nodes_explored}")
        # print(f"Độ dài đường đi: {best_cost}")
        # print("Đường đi:")
        # for state in best_path:
        #     print_state(state)
        return best_path, end_time - start_time, total_nodes_explored
    else:
        print("Không tìm thấy lời giải!")
        print(f"Thời gian chạy: {end_time - start_time:.4f} giây")
        print(f"Tổng số node đã khám phá: {total_nodes_explored}")

# Chạy chương trình
if __name__ == '__main__':
    partial_state = [
        [2, '?', '?'],
        ['?', 8, '?'],
        ['?', '?', 1]
    ]
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    solve_partial_8puzzle(partial_state, goal_state)