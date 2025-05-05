import heapq
import numpy as np
import timeit
import math
import random

def neighbor(state):
    row, col = np.argwhere(state==0)[0]
    moves = [(-1,0,), (0,-1,), (1,0,), (0,1,)]
    neighbors=list()
    
    for dr,dc in moves:
        newRow = dr + row
        newCol = dc + col
        if (0<=newRow<3) and (0<=newCol<3):
            newState = state.copy()
            newState[row,col], newState[newRow,newCol] = newState[newRow,newCol],newState[row,col]
            neighbors.append(newState)
    return neighbors

def Euclidean(state,goal):
    return sum(math.sqrt(math.pow((r1-r2),2)+math.pow((c1-c2),2))
                for num in range(1,9)
                for r1,c1 in [np.argwhere(state==num)[0]]
                for r2,c2 in [np.argwhere(goal==num)[0]])
def search(start,end):
    path=[start]
    stateTuple=tuple(start.flatten())
    endTuple=tuple(end.flatten())
    i=0
    while True:
        i+=1
        nes=neighbor(np.array(stateTuple).reshape((3,3)))
        if not nes:
            break
        # priorityQueue =[]
        # for nextState in nes:
        #     nextTuple=tuple(nextState.flatten())
        #     h=Euclidean(nextState,end)
        #     heapq.heappush(priorityQueue,(h,nextTuple))
       
        nextState=random.choice(nes)
        if Euclidean(nextState,end) >=Euclidean(np.array(stateTuple).reshape((3,3)),end):
            break
        stateTuple=tuple(nextState.flatten())
        path.append(stateTuple)
    return i, path
                
                
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
