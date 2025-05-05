import numpy as np

def neighbor(state):
    """ Tạo danh sách các trạng thái hàng xóm """
    row, col = np.argwhere(state == 0)[0]
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    neighbors = []

    for dr, dc in moves:
        newRow, newCol = row + dr, col + dc
        if 0 <= newRow < 3 and 0 <= newCol < 3:
            newState = state.copy()
            newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row, col]
            neighbors.append(newState)

    return neighbors

def Euclidean(state, goal):
    """ Tính tổng khoảng cách Euclidean """
    return sum(np.linalg.norm(np.argwhere(state == num)[0] - np.argwhere(goal == num)[0]) for num in range(1, 9))

def search(start, end):
    """ Thuật toán Hill Climbing dốc nhất """
    path = [start]
    state = start.copy()
    steps = 0

    while True:
        steps += 1
        neighbors = neighbor(state)
        if not neighbors:
            break  # Không còn hướng đi

        # Chọn trạng thái có giá trị heuristic tốt nhất
        best_state = min(neighbors, key=lambda s: Euclidean(s, end))

        # Nếu không có cải thiện, dừng lại
        if Euclidean(best_state, end) >= Euclidean(state, end):
            break

        state = best_state
        path.append(state)

    return steps, path

if __name__ == "__main__":
    start = np.array([
        [2, 6, 5],
        [0, 8, 7],
        [3, 1, 4]
    ])
    end = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])

    steps, path = search(start, end)
    print(f"Số bước: {steps}")

    for step in path:
        print(step, "\n")
