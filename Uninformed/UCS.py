import numpy as np
import collections
import timeit
# import queue
from collections import deque
import heapq
# import itertools

# counter=itertools.count()
#BFS dùng manhattan

# def manhattan(state, end):
#     return sum(abs(r1-r2)+abs(c1-c2)
#                 for num in range(1,9)
#                 for r1,c1 in [np.argwhere(state==num)[0]]
#                 for r2,c2 in [np.argwhere(end==num)[0]]
#     )

def actionHq(state):
    # next=[]
    row,col=np.argwhere(state==0)[0]
    
    moves=[
        (-1,0,),
        (0,-1,),
        (1,0,),
        (0,1,)
    ]

    for dr,dc in moves:
        newRow=dr+row
        newCol=dc+col
        if (0<=newRow<3) and (0<=newCol<3):
            newState=state.copy()
            newState[row,col], newState[newRow,newCol]=newState[newRow,newCol],newState[row,col]
            # next.append((newState, move))
            yield newState
    # return next

def searchBFS_Heapq(start,end):
    priorityQueue=[]
    visited={}
    startTuple=tuple(start.flatten())
    endTuple=tuple(end.flatten())

    heapq.heappush(priorityQueue,(0, startTuple,[startTuple]))
    i=0
    while priorityQueue:
        cost,stateTuple,path=heapq.heappop(priorityQueue)

        if stateTuple in visited:
            if visited[stateTuple] <= cost:
                continue

        visited[stateTuple]=int(cost)

        if stateTuple==endTuple:
            return i,path
        i+=1
        for nextState in actionHq(np.array(stateTuple).reshape((3,3))):
            nextTuple=tuple(nextState.flatten())
            if nextTuple not in visited or cost+1<visited[nextTuple]:
                # h=manhattan(nextState,end)
                heapq.heappush(priorityQueue,(cost+1,nextTuple, path+[nextTuple]))
    return None, None

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
    print(timeit.timeit(lambda: searchBFS_Heapq(start,end),number=5))
    # _Heapq