import numpy as np
import random
from heapq import heappush, heappop

# Trạng thái mục tiêu
GOALSTATE = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
GOALSTATETUPLE = tuple(GOALSTATE.flatten())

# Khởi tạo Q-Table và tham số
qTable = {}
actions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Lên, trái, xuống, phải
actionToIdx = {action: idx for idx, action in enumerate(actions)}
alpha = 0.1
gamma = 0.9
epsilon = 0.1
episodes = 100000
maxSteps = 100

def manhattan(state: np.ndarray, end: np.ndarray = GOALSTATE):
    """Tính tổng khoảng cách Manhattan."""
    return sum(abs(r1 - r2) + abs(c1 - c2)
               for num in range(1, 9)
               for (r1, c1), (r2, c2) in zip(np.argwhere(state == num), np.argwhere(end == num)))

def stateToTuple(state: np.ndarray):
    """Chuyển trạng thái thành tuple."""
    return tuple(state.flatten())

def move(state: np.ndarray, action):
    """Thực hiện hành động, trả về trạng thái mới hoặc None nếu không hợp lệ."""
    newState = state.copy()
    blankRow, blankCol = np.argwhere(newState == 0)[0]
    newRow, newCol = blankRow + action[0], blankCol + action[1]
    
    if 0 <= newRow < 3 and 0 <= newCol < 3:
        newState[blankRow, blankCol], newState[newRow, newCol] = newState[newRow, newCol], newState[blankRow, blankCol]
        return newState
    return None

def getReward(nextState: np.ndarray):
    """Tính phần thưởng."""
    if nextState is None:
        return -10
    if np.array_equal(nextState, GOALSTATE):
        return 100
    return -1 - manhattan(nextState, GOALSTATE) / 10

def solve_with_astar(state: np.ndarray):
    """Tìm đường đi bằng A* với heuristic Manhattan."""
    open_list = [(manhattan(state), state.tobytes(), state.tolist(), [])]
    closed_set = set()
    g_scores = {state.tobytes(): 0}  # Lưu chi phí thực tế (g)
    
    while open_list:
        f_score, state_bytes, state, path = heappop(open_list)
        state = np.array(state)
        
        if np.array_equal(state, GOALSTATE):
            return [(np.array(s)) for s in path]  # Trả về danh sách (trạng thái, hành động)
        
        if state_bytes in closed_set:
            continue
        closed_set.add(state_bytes)
        
        for action in actions:
            next_state = move(state, action)
            if next_state is not None:
                next_state_bytes = next_state.tobytes()
                g_score = g_scores[state_bytes] + 1  # Chi phí thực tế tăng 1
                
                if next_state_bytes not in g_scores or g_score < g_scores[next_state_bytes]:
                    g_scores[next_state_bytes] = g_score
                    f_score = g_score + manhattan(next_state)  # f = g + h
                    heappush(open_list, (f_score, next_state_bytes, next_state.tolist(), path + [next_state.tolist()]))
                    # , action
    
    return []  # Không tìm được đường đi

def trainAstar(initial_state: np.ndarray = None):
    """Huấn luyện Q-Table với hướng dẫn từ heuristic Manhattan."""
    for episode in range(episodes):
        # Kết hợp trạng thái ngẫu nhiên và trạng thái đầu cố định
        if initial_state is not None and episode % 2 == 0:
            state = initial_state.copy()
        else:
            state = np.random.permutation(9).reshape(3, 3)
        
        for step in range(maxSteps):
            stateTuple = stateToTuple(state)
            if stateTuple not in qTable:
                qTable[stateTuple] = [0] * 4
            
            if random.uniform(0, 1) < epsilon:
                actionScore = []
                for action in actions:
                    nextState = move(state, action)
                    if nextState is not None:
                        actionScore.append((action, -manhattan(nextState, GOALSTATE)))
                if actionScore:
                    action = max(actionScore, key=lambda x: x[1])[0]
                else:
                    action = random.choice(actions)
            else:
                action = actions[np.argmax(qTable[stateTuple])]
            
            nextState = move(state, action)
            reward = getReward(nextState)
            if nextState is None:
                continue
            
            nextStateTuple = stateToTuple(nextState)
            if nextStateTuple not in qTable:
                qTable[nextStateTuple] = [0] * 4
                
            actionIdx = actionToIdx[action]
            qValue = qTable[stateTuple][actionIdx]
            next_max = max(qTable[nextStateTuple])
            qTable[stateTuple][actionIdx] = qValue + alpha * (reward + gamma * next_max - qValue)   
                     
            state = nextState
            if stateToTuple(state) == GOALSTATETUPLE:
                break
        if episode % 1000 == 0:
            print(f"Episode {episode} completed")
            
def solve(initialState: np.ndarray,qTable):
    """Giải bài toán từ trạng thái ban đầu, dùng Q-Table hoặc A*."""
    state = initialState.copy()
    steps = []
    while not np.array_equal(state, GOALSTATE):
        stateTuple = stateToTuple(state)
        if stateTuple not in qTable:
            print("Trạng thái chưa được huấn luyện trong qTable, chuyển sang A*...")
            astar_steps = solve_with_astar(state)
            if not astar_steps:
                print("Không tìm được đường đi!")
                return len(qTable),steps
            steps.extend(astar_steps)
            break  # Thoát sau khi dùng A*
        
        actionIdx = np.argmax(qTable[stateTuple])
        action = actions[actionIdx]
        nextState = move(state, action)
        if nextState is None:
            print("Hành động không hợp lệ, chuyển sang A*...")
            astar_steps = solve_with_astar(state)
            if not astar_steps:
                print("Không tìm được đường đi!")
                return len(qTable),steps
            steps.extend(astar_steps)
            break
        
        state = nextState
        steps.append(state.copy())
        # , action
    
    return len(qTable),steps

# Trạng thái đầu
# initial_state = np.array([        
#         [2,6,5],
#         [0,8,7],
#         [4,3,1]])

# Huấn luyện với trạng thái đầu cố định
# trainAstar(initial_state)

# # Giải bài toán
# steps = solve(initial_state)

# # In kết quả
# print("\nTrạng thái ban đầu:")
# print(initial_state)
# print("\nCác bước giải:")
# for i, (state, action) in enumerate(steps):
#     print(f"Bước {i+1}: Hành động {action}")
#     print(state)