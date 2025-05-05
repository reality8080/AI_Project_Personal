import numpy as np
# import collections
import timeit
# import queue
from collections import deque
# import heapq
# import itertools

# counter=itertools.count()
#BFS dùng manhattan


def actionHq(state):
    # next=[]
    row,col=np.argwhere(state==0)[0]
    
    nextState=[]
    
    moves=[
        (-1,0,"Up"),
        (0,-1,"Down"),
        (1,0,"Left"),
        (0,1,"Right")
    ]

    for dr,dc,Moves in moves:
        newRow=dr+row
        newCol=dc+col
        if (0<=newRow<3) and (0<=newCol<3):
            newState=state.copy()
            newState[row,col], newState[newRow,newCol]=newState[newRow,newCol],newState[row,col]
            nextState.append((newState,Moves))
    return nextState

def DFS(start,end,maxDepth):
    stack=deque()
    visited=set()
    startTuple=tuple(start.flatten())
    endTuple=tuple(end.flatten())
    nodesExplored = 0
    
    stack.append((start,[],0))
    visited.add(startTuple)
    while stack:
        state, path,depth=stack.pop()
        nodesExplored+=1
        
        if tuple(state.flatten()) == endTuple:
            return nodesExplored, path,None
        
        if depth>=maxDepth:
            continue
        
        # if stateTuple not in visited:
        #     i+=1
        #     visited.add(stateTuple)
        for nextState,move in actionHq(state):
            nextTuple=tuple(nextState.flatten())
            if nextTuple not in visited:
                visited.add(nextTuple)
                stack.append((nextTuple,path+[nextTuple],depth+1))
    return nodesExplored, None

# def ID(start,end):
#     cost=0
#     stack=deque()
#     visited=set()
#     startTuple=tuple(start.flatten())
#     endTuple=tuple(end.flatten())

#     stack.append((0,startTuple,[startTuple]))
#     while stack:
#         c,stateTuple, path=stack.pop()

#         if c>cost:
#             c=0
#             stack.clear()
#             stack.append((c,startTuple,[startTuple]))
#             cost+=1
#         if stateTuple==endTuple:
#             return path
        
#         if stateTuple not in visited:
#             visited.add(stateTuple)
#             for nextState in actionHq(np.array(stateTuple).reshape((3,3))):
#                 nextTuple=tuple(nextState.flatten())
#                 if nextTuple not in visited:
#                     stack.appendleft((cost+1,nextTuple,path+[nextTuple]))
#     return None



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
    print(timeit.timeit(lambda: DFS(start,end),number=5))