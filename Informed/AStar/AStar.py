import numpy as np
import heapq
import timeit

def manhattan(state, end):
    return sum(abs(r1-r2)+abs(c1-c2)
               for num in range(1,9)
               for r1,c1 in [np.argwhere(state==num)[0]]
               for r2,c2 in [np.argwhere(end==num)[0]])

def nextAction(state):
    # Tim vi tri cua so 0
    row,col=np.argwhere(state==0)[0]
    # To hop duong di ke tiep
    moves=[(-1,0),(0,-1),(1,0),(0,1)]
    for dr,dc in moves:
        newRow,newCol=dr+row,dc+col
        if(0<=newRow<3) and (0<=newCol<3):
            newState=state.copy()
            newState[row,col],newState[newRow,newCol]=newState[newRow,newCol],newState[row,col]
            yield newState
a=0            
def AStar(start:np.array,end:np.array):
    global a
    priorityQueue=[]
    visited={}
    startTuple=tuple(start.flatten())
    endTuple=tuple(end.flatten())
    i=0
    heapq.heappush(priorityQueue,(0,0,startTuple,[startTuple]))
    while priorityQueue:
        
        _,cost,u,path=heapq.heappop(priorityQueue)
        
        if u in visited:
            if visited[u]<=cost:
                continue
        
        visited[u]=int(cost)
        
        if u == endTuple:
            return i,path
        i+=1
        for nextState in nextAction(np.array(u).reshape((3,3))):
            nextTuple=tuple(nextState.flatten())
            if nextTuple not in visited or cost+1<visited[nextTuple]:
                    h=manhattan(nextState,end)
                    heapq.heappush(priorityQueue,(cost+1+h,cost+1,nextTuple,path+[nextTuple]))
                    a=a+1
    return None
    

if __name__ == "__main__":
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
    
    print(timeit.timeit(lambda:AStar(start,end),number=5))
    path=AStar(start,end)
    if path:
        for step in path:
            print(np.array(step).reshape((3,3)))
            print()
    print(a)