import numpy as np
import heapq

def isGoal(state,end):
    return np.array_equal(state, end)

def manhattan(state,end):
    return sum(
        abs(r1-r2)+abs(c1-c2)
        for num in range(1,9)
        for r1,c1 in [np.argwhere(state==num)[0]]
        for r2,c2 in [np.argwhere(end==num)[0]]
    )

def hybridAStar_AND_OR(start:np.ndarray,end:np.ndarray):
    n=0
    priority=[(manhattan(start,end),0,1,0,start,[])]
    visited=set()
    counter=1
    
    while priority:
        f,g,prob,_,state,path=heapq.heappop(priority)
        stateTuple=tuple(map(tuple,state))
        
        if isGoal(state,end):
            return n,path+[state]
        if stateTuple in visited:
            continue
        n+=1
        visited.add(stateTuple)
        
        children=generateChildren(state)
        
        if isComplexState(state,children):
            result,resultProb =Astar(state,path,visited.copy(),end)
            if result:
                return path+result,prob*resultProb
        else:
            for child, childProb in children:
                childTuple=tuple(map(tuple,child))
                if childTuple not in visited:
                    gChild=g+moveCost(state,child)/childProb
                    hChild=manhattan(child,end)
                    fChild=gChild+hChild
                    heapq.heappush(priority,(fChild,gChild,prob*childProb,counter,child,path+[state]))
                    counter+=1
                    
    return 0,None    

def Astar(state, path, visited, end, prob):
    stateTuple = tuple(map(tuple, state))
    if isGoal(state, end):
        return [state], 1.0  # Đạt mục tiêu

    if stateTuple in visited:
        return None, 0  # Đã thăm

    visited.add(stateTuple)  # Đánh dấu trạng thái đã thăm
    children = generateChildren(state)

    bestPath = None
    bestProb = 0

    for child, childProb in children:
        result, resultProb = andNode(child, end, visited, path + [state], prob)
        if result:
            totalProb = childProb * resultProb
            if totalProb > bestProb:
                bestPath = [state] + result
                bestProb = totalProb

    return bestPath, bestProb

def andNode(state, end, visited, path, prob):
    return Astar(state, path, visited.copy(), end, prob)
def generateChildren(state):
    children = []
    row, col = np.argwhere(state == 0)[0]
    moves = [
        ((-1, 0), 0.25),  # Di chuyển lên
        ((1, 0), 0.25),   # Di chuyển xuống
        ((0, -1), 0.25),  # Di chuyển sang trái
        ((0, 1), 0.25)    # Di chuyển sang phải
    ]

    jumps = [
        ((-2, 0), 0.05),  # Nhảy 2 ô lên
        ((2, 0), 0.05),   # Nhảy 2 ô xuống
        ((0, -2), 0.05),  # Nhảy 2 ô sang trái
        ((0, 2), 0.05)    # Nhảy 2 ô sang phải
    ]

    for (dr, dc), prob in moves + jumps:
        newRow, newCol = row + dr, col + dc
        if 0 <= newRow < 3 and 0 <= newCol < 3:
            newState = np.copy(state)
            newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row, col]
            children.append((newState, prob))

    return children

def isComplexState(state, children):
     return len(children) > 5 or sum(prob for _, prob in children) < 0.5

def moveCost(state,child):
    r1,c1 = np.argwhere(state==0)[0]
    r2,c2 = np.argwhere(child==0)[0]
    return abs(r1-r2)+abs(c1-c2)

if __name__=="__main__":
    # start=np.array([
    #     [2,6,5],
    #     [0,8,7],
    #     [4,3,1]
    # ])
    
    start=np.array([
        [2,8,3],
        [7,0,4],
        [1,6,5]
    ])
    
    end=np.array([
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ])
    
    spaceState, path = hybridAStar_AND_OR(start, end)
    
    if path:
        for i, state in enumerate(path):
            print(f"Step {i}:")
            print(state)
            print()
    else:
        print("No solution found")