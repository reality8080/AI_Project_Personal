from copy import deepcopy
import random
import time
import numpy as np

# Danh sách lưu lại toàn bộ trạng thái bảng sau mỗi bước
board_states = []

def isValid(assignment, var, value):
    # if value == 0:
    #     return True
    return value not in assignment.values()

def selectUnassigned(assignment, domains):
    unassigned = [var for var in domains if var not in assignment]
    return min(unassigned, key=lambda x: len(domains[x]))

def orderDomainValues(var, domains, assignment):
    values = domains[var]
    valueConstraints = []
    
    for val in values:
        if val == 0:
            continue
        conflict = 0
        for otherVar in domains:
            if otherVar != var and otherVar not in assignment:
                if val in domains[otherVar]:
                    conflict += 1
        valueConstraints.append((val, conflict))
    return [val for val, _ in sorted(valueConstraints, key=lambda x: x[1])]

def forwardCheck(domains, var, value):
    if value==0:
        return deepcopy(domains)
    newDomains = deepcopy(domains)
    for neighbor in newDomains:
        if neighbor != var and value in newDomains[neighbor]:
            newDomains[neighbor].remove(value)
            if not newDomains[neighbor]:
                return None    
    return newDomains    

def cspBacktracking(assignment, domains):
    if len(assignment) == len(domains):
        return assignment
    
    var = selectUnassigned(assignment, domains)
    for value in orderDomainValues(var, domains, assignment):
        if isValid(assignment, var, value):
            assignment[var] = value
            board_states.append(deepcopy(assignment))  #  Lưu trạng thái bảng

            newDomains = forwardCheck(domains, var, value)
            if newDomains is not None:
                result = cspBacktracking(assignment, newDomains)
                if result is not None:
                    return result

            del assignment[var]
            board_states.pop()  #  Nếu quay lui, xóa trạng thái không còn hợp lệ
    return None

def print_board(state):
    # In ra trạng thái dạng bảng 3x3
    board = np.zeros(9, dtype=int).astype(str)
    for i in state:
        board[i] = str(state[i])
    for i in range(0, 9, 3):
        print(' '.join(board[i:i+3]))
    return board

count=0
def solve_csp_8puzzle():
    global count
    count+=1
    variables = list(range(9))  # 9 ô trong bảng 3x3
    allValues = list(range(9))  # Các giá trị từ 1 đến 8
    domains = {var: allValues for var in variables}  # mỗi ô có miền 0-8

    assignment = dict()
    
    zeroPosition=random.choice(variables)
    assignment[zeroPosition] = 0  # Giả sử ô đầu tiên là ô trống
    
    for var in variables:
        if var != zeroPosition:
            domains[var]=[v for v in allValues if v != 0]
    domains[zeroPosition]=[0]
    board_states.append(deepcopy(assignment))  # Lưu trạng thái ban đầu
    result = cspBacktracking(assignment, domains)
    if result:
        # print("Kết quả cuối cùng:")
        # print_board(result)
        path=[]
        # print("Toàn bộ các bước điền giá trị (trạng thái bảng):")
        for idx, state in enumerate(board_states):
            print(f"Bước {idx + 1}:")
            path.append(print_board(state))
        # path= [np.array(board_states[key]) for key in board_states]
        # path=print_board(board_states)
        return count,path
    else:
        print("Không có lời giải")

# if __name__ == "__main__":
#     solve_csp_8puzzle()
