import numpy as np
import random

def Manhattan(state, goal):
    distance = 0
    for num in range(1, 9):
        pos1 = np.argwhere(state == num)[0]
        pos2 = np.argwhere(goal == num)[0]
        distance += abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    return distance

def neighbor(state):
    row, col = np.argwhere(state == 0)[0]
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    neighbors = []
    for dr, dc in moves:
        newRow, newCol = row + dr, col + dc
        if 0 <= newRow < state.shape[0] and 0 <= newCol < state.shape[1]:
            newState = state.copy()
            newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row, col]
            neighbors.append(newState)
    return neighbors

def search(start, goal):
    T = 1000
    a = 0.95
    minT = 1e-3
    state = start.copy()
    bestState = state.copy()
    bestCost = Manhattan(state, goal)
    path = [state.copy()]
    steps = 0

    while T > minT:
        steps += 1
        neighbors = neighbor(state)
        nextState = random.choice(neighbors)
        currentCost = Manhattan(state, goal)
        nextCost = Manhattan(nextState, goal)
        deltaE = nextCost - currentCost  # chỉnh hướng đúng

        if deltaE < 0 or random.random() < np.exp(-deltaE / T):
            state = nextState.copy()
            path.append(state.copy())
            if nextCost < bestCost:
                bestCost = nextCost
                bestState = state.copy()

        if np.array_equal(state, goal):
            print("Đã tìm được lời giải!")
            for i, step in enumerate(path):
                print(f"\nBước {i + 1}:\n{step}")
            return steps, path, bestState, len(path)

        T *= a

    print("Không tìm được lời giải. Trạng thái tốt nhất tìm được là:")
    print(bestState)
    return steps, path, bestState, len(path)

if __name__ == "__main__":
    start = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ])
    
    end = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    
    steps, path, bestState, numVisited = search(start, end)