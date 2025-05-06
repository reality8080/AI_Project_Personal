import numpy as np

def neighbor(state):
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
    return sum(np.linalg.norm(np.argwhere(state == num)[0] - np.argwhere(goal == num)[0]) for num in range(1, 9))

def search(start, end):
    path = [start]
    state = start.copy()
    visited = set([tuple(start.flatten())])
    spaceState = 1
    max_steps = 1000

    while spaceState < max_steps:
        neighbors = neighbor(state)
        if not neighbors:
            break

        # Chọn trạng thái đầu tiên cải thiện heuristic
        current_heuristic = Euclidean(state, end)
        best_state = None
        for neighbor_state in neighbors:
            neighbor_tuple = tuple(neighbor_state.flatten())
            if neighbor_tuple not in visited and Euclidean(neighbor_state, end) < current_heuristic:
                best_state = neighbor_state
                break

        # Nếu không có cải thiện, dừng
        if best_state is None:
            break

        state = best_state
        path.append(state)
        visited.add(tuple(state.flatten()))
        spaceState += 1

        if np.array_equal(state, end):
            print("Đạt trạng thái mục tiêu!")
            break

    return spaceState, path

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
