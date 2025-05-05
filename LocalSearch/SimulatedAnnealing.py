import numpy as np
import random

def neighbor(state):
    row, col =np.argwhere(state == 0)[0]
    moves = [(-1,0), (0,-1), (1,0), (0,1)]
    neighbors = []
    for dr, dc in moves:
        newRow, newCol = row + dr, col + dc
        if 0 <= newRow < state.shape[0] and 0 <= newCol < state.shape[1]:
            newState = state.copy()
            newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row,col]
            neighbors.append(newState)
            
    return neighbors

def Euclidean(state, goal):
    distance=0
    for num in range(1,9):
        pos1=np.argwhere(state==num)
        pos2=np.argwhere(goal == num)
        if pos1.size > 0 and pos2.size > 0:
            distance+= np.linalg.norm(pos1[0]-pos2[0])
    return distance
    
def search (start, end):
    T=10000
    a=0.99
    minT=1e-3
    path=[start]
    state = start.copy()
    steps=0
    visited=set()
    visited.add(state.tobytes())
    bestCost=Euclidean(state,end)
    bestState=state.copy()
    
    while T>minT:
        steps+=1
        neighbors=neighbor(state)
        if not neighbors: 
            break
        nextState=random.choice(neighbors)
        currentCost=Euclidean(state,end)
        nextCost=Euclidean(nextState,end)
        
        # validNeighbors = [s for s in neighbors if s.tobytes() not in visited]
        # if not validNeighbors:
        #     break
        # bestState= min(validNeighbors, key = lambda s: Euclidean(s,end))
        DeltaE=currentCost-nextCost
        if DeltaE>0:
            state=nextState
        else:
            P=np.exp(DeltaE / T) if DeltaE/T>-700 else 0
            if np.random.rand()<P:
                state=nextState
        path.append(state)
        visited.add(state.tobytes())
        if nextCost<bestCost:
            bestCost=nextCost
            bestState=nextState
        T*=a
            
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