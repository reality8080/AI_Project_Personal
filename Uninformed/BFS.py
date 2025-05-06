import numpy as np
import collections
import timeit
# import queue
from collections import deque
import heapq
# import itertools

# counter=itertools.count()
#BFS dùng manhattan


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



def searchBFS(start,end):
    i=0
    Queue=collections.deque()
    visited=set()
    startTuple=tuple(start.flatten())
    endTuple=tuple(end.flatten())

    Queue.append([startTuple,[]])
    # visited.add(startTuple)

    while Queue:
        stateTuple, action=Queue.popleft()

        if stateTuple==endTuple:
            return i, action
        if stateTuple in visited:
            continue
        visited.add(stateTuple)
        i+=1
        visited.add(stateTuple)
        for nextState,move in actionHq(np.array(stateTuple).reshape((3,3))):
            nextTuple=tuple(nextState.flatten())
            if nextTuple not in visited:
                Queue.append([nextTuple,action+[move]])
    return None, None

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

if __name__=='__main__':
    start=np.array([
        [2,6,5],
        [0,8,7],
        [4,3,1]
    ])
    end=np.array([
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ])
    nodes, actions = searchBFS(start, end)
    if actions:
        print(f"✅ Found solution with {len(actions)} steps. Nodes explored: {nodes}")
        path = reconstruct_path(start, actions)
        for step in path:
            print(step, "\n")
    else:
        print("❌ No solution found.")
    # _Heapq