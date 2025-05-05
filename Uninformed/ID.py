import numpy as np
# import collections
import timeit
# import queue
from collections import deque
import heapq
# import itertools

# counter=itertools.count()
#BFS dùng manhattan


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

def ID(start,end):
    cost=10000   
    startTuple=tuple(start.flatten())
    endTuple=tuple(end.flatten())
    i=0
    while True:
        stack=deque([(0,startTuple,[startTuple])])
        visited=set()
        while stack:
            c,stateTuple, path=stack.pop()
            if stateTuple==endTuple:
                return i, path
            if c <cost:
                if stateTuple not in visited:
                    i+=1
                    visited.add(stateTuple)
                    for nextState in actionHq(np.array(stateTuple).reshape((3,3))):
                        nextTuple=tuple(nextState.flatten())
                        if nextTuple not in visited:
                            stack.appendleft((c+1,nextTuple,path+[nextTuple]))
        cost+=10000

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
    print(timeit.timeit(lambda: ID(start,end),number=5))