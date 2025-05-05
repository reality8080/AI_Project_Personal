import numpy as np
import heapq
import abc
import timeit


class IManhattan(abc.ABC):
    @abc.abstractmethod
    def manhattan(self,state,end):
       pass

class IAction:
    @abc.abstractmethod
    def action(self,state):
       pass

class AStarManhattan(IManhattan):
    def manhattan(self, state, end):
        return sum(abs(r1 - r2) + abs(c1 - c2)
                   for num in range(1, 9)
                   for r1, c1 in [np.argwhere(state == num)[0]]
                   for r2, c2 in [np.argwhere(end == num)[0]])
class AStarAction(IAction):
    def action(self, state):
        row, col = np.argwhere(state == 0)[0]
        moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        for dr, dc in moves:
            newRow, newCol = dr + row, dc + col
            if (0 <= newRow < 3) and (0 <= newCol < 3):
                newState = state.copy()
                newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row, col]
                yield newState
                
class AStar:
    def __init__(self, h:IManhattan,action: IAction):
        self.h=h
        self.action=action
        self.priorityQueue=[]
        self.visited={}

class AStarMethod(AStar):
    def __init__(self, h:IManhattan, action:IAction):
        super().__init__(h, action)
    def search(self,start,end):
        startTuple=tuple(start.flatten())
        endTuple=tuple(end.flatten())
        heapq.heappush(self.priorityQueue,(0,0,startTuple,[startTuple]))
        # parentMap={startTuple:None}
        
        while self.priorityQueue:
            _,cost,u,path=heapq.heappop(self.priorityQueue)
# Kiem tra xem co trong danh sach va chi phi cu thap hon chi phi hien tai
# Chi phi hien tai thap hon thi them vao visited[u], toi uu hon
            if u in self.visited:
                if self.visited[u]<=cost:
                    continue
            self.visited[u]=int(cost)
            # parentMap[u]=parent
            if u==endTuple:
                return path
            
            for nextState in self.action.action(np.array(u).reshape((3,3))):
                nextTuple=tuple(nextState.flatten())
                if nextTuple not in self.visited or cost+1<self.visited[nextTuple]:
                    h=self.h.manhattan(nextState,end)
                    heapq.heappush(self.priorityQueue,(cost+1+h,cost+1,nextTuple,path+[nextTuple]))
        return None

if __name__=='__main__':
    start = np.array([
        [2, 6, 5],
        [0, 8, 7],
        [4, 3, 1]
    ])
    end = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    Astar=AStarMethod(AStarManhattan(),AStarAction())
    print(timeit.timeit(lambda: Astar.search(start,end),number=5))   
    # path=Astar.search(start,end) 
    # if path:
    #     for step in path:
    #         print(np.array(step).reshape((3,3)))
    #         print()
