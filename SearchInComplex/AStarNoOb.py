import numpy as np
import heapq

def manhattan(state,end):
    return np.sum(
        abs(r1-r2)+abs(c1-c2)
               for num in range(1,9)
               for r1,c1 in [np.argwhere(state==num)[0]]
               for r2,c2 in [np.argwhere(end==num)[0]]
    )
    

# Timf kieems trong mooi truowngf ko quan sat ducowj, cos nieemf tin
# Tifm kieems trong  mooi truownfg thaays truocws 1 phaanf
# Timf kieems trong mooi truowngf cos casc ranfg buoocj

def randomArray():
    board=np.arange(9)
    np.random.shuffle(board)
    boardRan=board.reshape(3,3)
    return boardRan

def BeliefList(amout:int):
    list=[]
    for _ in range(amout):
        list.append(randomArray())
    return list

# def nextAction(state):
#     row,col = np.argwhere(state==0)[0]
#     moves = [(-1,0),(0,-1),(1,0),(0,1)]
#     for dr,dc in moves:
#         newRow,newCol=dr+row, dc+col
#         if(0<=newRow<3 and 0<=newCol<3):
#             newState=np.copy(state)
#             newState[row,col],newState[newRow,newCol]=newState[newRow,newCol],newState[row,col]
#             yield newState
# Hàm lấy giao chế độ
def nextAction(listState):
    listAction=set()
    moves=[(-1,0,'Left'),(0,-1,"Down"),(1,0,"Right"),(0,1,"Up")]
    for x in listState:
        row,col = np.argwhere(x==0)[0]
        for dr,dc, move in moves:
            newRow,newCol=row+dr,col+dc
            if (0<=newRow<3 and 0<=newCol<3) and move not in listAction:
                listAction.add(move)
            if len(listAction)>=4:
                return listAction
    return listAction
   
def movesAction(state:np.ndarray,move):
    list1=[]
    if move =='Left':
        dr,dc=-1,0
    elif move=='Right':
        dr,dc=1,0
    elif move=='Up':
        dr,dc=0,-1
    elif move=='Down':
        dr,dc=0,1
    for U in state:
        row,col = np.argwhere(U==0)[0]
        newRow,newCol=row+dr,col+dc
        UState=np.copy(U)
        if (0<=newRow<3 and 0<=newCol<3):
            UState[row,col],UState[newRow,newCol]=UState[newRow,newCol],UState[row,col]
            if not any(np.array_equal(UState, s) for s in list1):
                list1.append(UState)
        else:
            list1.append(UState)
    return list1
        
def belief_to_tuple(belief):
    return tuple(tuple(state.flatten()) for state in belief)
    
def belief_heuristic(belief,end):
    return max(manhattan(state, end) for state in belief) 
            
def AStarNoOb(listStart:np.ndarray,end:np.ndarray):
    priorityQ=[]
    visited=set()
    count=0
    startBeliefTuple=belief_to_tuple(listStart)
    
    heapq.heappush(priorityQ,(0+belief_heuristic(listStart,end),0,startBeliefTuple,[startBeliefTuple]))
    
    while priorityQ:
        _,cost,uTuple,path=heapq.heappop(priorityQ)
        u=[np.array(state).reshape(3,3) for state in uTuple]
        if all(np.array_equal(state,end) for state in u):
            return path,count
        if uTuple in visited:
            continue
        visited.add(uTuple)
        count+=1
            
        nextActions=nextAction(u)
        for action in nextActions:
            newBelief = movesAction(u, action)
            if newBelief:
                newBeliefTuple = belief_to_tuple(newBelief)
                if newBeliefTuple not in visited:
                    new_cost = cost + 1
                    h = belief_heuristic(newBelief,end)
                    heapq.heappush(priorityQ, (new_cost + h, new_cost, newBeliefTuple, path + [newBeliefTuple]))
    return None,count

if __name__ == "__main__":
    
    listStart=BeliefList(100)
    end=np.array([
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ])
    
    path=AStarNoOb(listStart,end)