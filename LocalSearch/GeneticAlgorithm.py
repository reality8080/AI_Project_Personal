import numpy as np
import random

def flattenState(state):
    return state.flatten()

def unflatten(flatState):
    return np.array(flatState).reshape(3,3)

def neighborRandomState(state, Steps):
    moves = [(-1,0), (0,-1), (1,0), (0,1)]
    newState = state.copy()
    for _ in range(Steps):
        row, col = np.argwhere(newState == 0)[0]
        validMoves = [(row + dr, col + dc) for dr, dc in moves if 0 <= row + dr < 3
                                                                    and 0 <= col + dc <3]
        if validMoves:
            newRow, newCol = random.choice(validMoves)
            newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row, col]
    return(newState)

def generatePopulation(size, state, Steps):
    population=[]
    while len(population)<size:
        newState=neighborRandomState(state,Steps).flatten()
        if len(np.unique(newState))==9:
            population.append(newState)
    return population

def precomputeGoalPosition(goal):
    return {goal[r,c]:(r,c) for r in range(3) for c in range(3)}

def manhattan(state, goalPosition):
    total_distance = 0
    for num in range(1, 9):
        pos = np.argwhere(state == num)
        if pos.size == 0:  # Kiểm tra nếu không tìm thấy số
            continue
        r, c = pos[0]
        total_distance += abs(r - goalPosition[num][0]) + abs(c - goalPosition[num][1])
    return total_distance


def fixDuplicateNumbers(state):
    state=np.array(state)
    flat=state.flatten()
    unique, counts = np.unique(flat, return_counts=True)
    duplicateNumbers = []
    for num, count in zip(unique,counts):
        if num == 0:
            if count > 1:
                duplicateNumbers.extend([num] * (count-1))
        else:
            if count > 1:
                duplicateNumbers.extend([num] * (count-1))

    missingNumbers = list(set(range(9)) - set(unique))
    
    if len(duplicateNumbers) != len(missingNumbers):
        return state

    np.random.shuffle(duplicateNumbers)
    np.random.shuffle(missingNumbers)

    for i in range(len(flat)):
        if flat[i] in duplicateNumbers:
            idx = duplicateNumbers.index(flat[i])
            flat[i] = missingNumbers[idx]
            duplicateNumbers.pop(idx)
            missingNumbers.pop(idx)
            if not duplicateNumbers:
                break
    return flat.reshape(3,3)

def crossOver(parent1, parent2):
    parent1 = parent1.flatten()
    parent2 = parent2.flatten()
    
    size = len(parent1)
    cut1,cut2 = sorted(random.sample(range(size),2 ))
    
    def pmx(parentA,parentB):
        child = np.zeros(size, dtype=int)
        child[cut1:cut2+1] = parentA[cut1:cut2+1]
        mapping = {}
        for i in range(cut1,cut2+1):
            if parentA[i] != parentB[i]:
                mapping[parentA[i]]=parentB[i]
        for i in list(range(0,cut1)) + list(range(cut2+1, size)):
            current = parentB[i]
            while current in mapping:
                current = mapping[current]
            child[i] = current
        return child.reshape(3,3)
    child1 = pmx(parent1,parent2)
    child2 = pmx(parent2, parent1)
    return child1,child2



def tournamentSelect(fitnessList, tournamentSize):
    contestants = random.sample(fitnessList, tournamentSize)
    best = min(contestants, key = lambda x:x[1])
    return best[0]

def mutate(state,mutationRate):
    if random.random() < mutationRate:
        newState = np.array(state).reshape(3,3).copy()
        steps = random.randint(1,3)
        
        for _ in range(steps):
            zeroPos = np.argwhere(newState == 0)
            if zeroPos.size == 0:
                break
            row, col = zeroPos[0]
            moves = [(-1,0),(0,-1),(1,0),(0,1)]
            validMoves=[]
            for dr, dc in moves:
                newRow, newCol = row + dr, col+dc
                if 0<= newRow < 3 and 0 <= newCol < 3:
                    validMoves.append((newRow,newCol))
            
            if validMoves:
                newRow, newCol = random.choice(validMoves)
                newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row, col]
        return newState.flatten()
    return state
    

def search(start, end, populationSize, generations, mutationRate):
    goalposistion=precomputeGoalPosition(end)
    population=generatePopulation(populationSize,start,50)
    path=[start]
    totalSpaceEvaluated = 0

    for gen in range(generations):
        
        fitness = [(state, manhattan(unflatten(state), goalposistion)) for state in population]
        totalSpaceEvaluated+= len(population)
        fitnessSorted = sorted(fitness, key= lambda x: x[1])
        bestState = unflatten(fitnessSorted[0][0])
        path.append(bestState)
         
        # Kiem tra chi phi luc tao trang thai moi co vo tinh tao ra dap an
        if fitnessSorted[0][1]==0:
            return totalSpaceEvaluated,path
        
        eliteSize = max(1, int(populationSize * 0.1))
        elite = [f[0] for f in fitnessSorted[:eliteSize]]
        newPopulation = elite.copy()
                
        while len(newPopulation) < populationSize:
            parent1 = tournamentSelect(fitness, 3)
            parent2 = tournamentSelect(fitness, 3)            
            child1, child2 =crossOver(parent1,parent2)
            newPopulation.append(mutate(child1,mutationRate))
            if len(newPopulation) < populationSize:
                newPopulation.append(mutate(child2,mutationRate))
        population = newPopulation
    return totalSpaceEvaluated,path
            
            

if __name__ == '__main__':
    start = np.array([
        [2,6,5],
        [0,8,7],
        [3,1,4]
    ])
    
    end = np.array([
        [1,2,3],
        [4,5,6],
        [7,8,0]        
    ])
    
    space,path = search(start, end, 100,1000, 0.1)
    print(space)
    if path is not None and len(path) > 0:
        for i,step in enumerate( path):
            print(f"Bước: {i}")
            print(step)
            print()
# Tiep tuc sua loi