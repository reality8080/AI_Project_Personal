import numpy as np
import random
import timeit

def manhattan_distance(state, goal):
    distance = 0
    for num in range(1, 9):  # Bỏ qua 0 (ô trống)
        row_s, col_s = np.argwhere(state == num)[0]
        row_g, col_g = np.argwhere(goal == num)[0]
        distance += abs(row_s - row_g) + abs(col_s - col_g)
    return distance


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

def search(start, goal, max_steps=1000, no_improve_limit=100):
    current = start.copy()
    current_score = manhattan_distance(current, goal)
    path = [current]
    no_improve = 0

    for step in range(max_steps):
        neighbors = neighbor(current)
        if not neighbors:
            break

        # Chọn ngẫu nhiên 1 neighbor
        candidate = random.choice(neighbors)
        candidate_score = manhattan_distance(candidate, goal)

        if candidate_score < current_score:
            current = candidate
            current_score = candidate_score
            path.append(current)
            no_improve = 0  # Reset bộ đếm không cải thiện
        else:
            no_improve += 1

        if np.array_equal(current, goal):
            break
        if no_improve >= no_improve_limit:
            break  # Không cải thiện quá lâu => thoát

    return len(path),path

                
if __name__=="__main__":
    start=np.array([
        [2,6,5],
        [0,8,7],
        [3,1,4]
    ])
    end=np.array([
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ])
    i,path=search(start,end)
    print(timeit.timeit(lambda:search(start,end),number=100))
    print(i)
    if path:
        for step in path:
            print(np.array(step).reshape((3,3)))
