import heapq
import numpy as np
import timeit
import math

def neighbor(state):
    row, col = np.argwhere(state==0)[0]
    moves = [(-1,0), (0,-1), (1,0), (0,1)]
    neighbors=[]
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
def search(start,end,K):
    priorityQueue=[]
    visitedCost={}
    startTuple=tuple(start.flatten())
    endTuple=tuple(end.flatten())
    heapq.heappush(priorityQueue,(0, startTuple,[startTuple]))
    i=0
    while priorityQueue:
        cost,stateTuple,path=heapq.heappop(priorityQueue)
        i+=1
        
        if(stateTuple in visitedCost):
            if visitedCost[stateTuple]<=cost:
                continue
        visitedCost[stateTuple]=int(cost)
        if stateTuple==endTuple:
            return i,path
        nextStates=[]
        for nextState in neighbor(np.array(stateTuple).reshape((3,3))):
            nextTuple=tuple(nextState.flatten())
            if nextTuple not in visitedCost or cost+1<visitedCost[nextTuple]:
                h=Euclidean(nextState,end)
                heapq.heappush(nextStates,(cost+h,nextTuple, path+[nextTuple]))
        priorityQueue=heapq.nsmallest(K,nextStates)
    return i,None
        
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
    i,path=search(start,end,10)
    print(timeit.timeit(lambda:search(start,end, 10),number=100))
    print(i)
    if path:
        for step in path:
            print(np.array(step).reshape((3,3)),end="\n")
