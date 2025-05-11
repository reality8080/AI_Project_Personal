import pygame
import sys
import numpy as np
import timeit
import time
import os
import json
from PIL import Image
import imageio

from Uninformed.BFS import searchBFS, reconstruct_path as BFSRP
from Uninformed.DFS import DFS, reconstruct_path
from Uninformed.ID import ID
from Informed.Greedy import Greedy
from Uninformed.UCS import searchBFS_Heapq 
from Informed.AStar import AStar
from Informed.IDAStar import IDAStar
from LocalSearch.RandomHillClimbing import search as RandomHillClimbing
from LocalSearch.SimpHillClimbing import search as SimpHillClimbing
from LocalSearch.SteepesHillClimbing import search as SteepesHillClimbing
from LocalSearch.SimulatedAnnealing import search as SimulatedAnnealing
from LocalSearch.BeamSearch import search as BeamSearch
from LocalSearch.GeneticAlgorithm import search as GeneticAlgorithm
from SearchInComplex.AND_OR_ASTAR import hybridAStar_AND_OR as AND_OR
from SearchInComplex.AStarNoOb import AStarNoOb as AStarNoOb, BeliefList
from CSP.SeePartOfMatrix import solve_partial_8puzzle as SeePartOfMatrix
from CSP.CSP_BackTracking import solve_csp_8puzzle as CSPBackTracking, print_board
from Qlearing.QL import trainAstar as QLearning, solve as solve_QLearning, qTable
from function.btns.drawMMenu import mainMenu
from function.btns.drawFigure import drawFigures,drawFiguresNoOb
from function.animated.animation import animation

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (113, 113, 113)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# class Config:
Height, Width = 600, 800
WidthBoard = 500
HeightBoard = 500
boardRows = 3
boardCols = 3
squareSize = WidthBoard // boardCols
LineWidth = 5

screen = pygame.display.set_mode((Width, Height))
screen = pygame.display.set_mode((WidthBoard, HeightBoard))

font = pygame.font.Font(None, 100)
fontBoard = pygame.font.Font(None, 150)
algorithm = ""

def log_selection_to_file(filename, algorithm, time, path, space_state):
    """Log algorithm selection and metrics to a JSON file."""
    log_entry = {
        "algorithm": algorithm,
        "execution_time": time,
        "states_explored": space_state,
        "path_length": len(path) if path is not None else 0
    }
    
    # Read existing data or initialize empty list
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    # Append new entry
    data.append(log_entry)
    
    # Write back to file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def save_result_to_file(filename, algorithm, time, path, space_state):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Thuật toán: {algorithm}\n")
        file.write(f"Thời gian chạy: {time:.6f} giây\n")
        file.write(f"Số trạng thái duyệt: {space_state}\n")
        if path is not None:
            file.write(f"Số trạng thái đường đi: {len(path)}\n")
            file.write("Đường đi:\n")
            for i, step in enumerate(path):
                file.write(f"\nBước {i + 1}:\n")
                if algorithm == "NoOb":
                    for i, belief in enumerate(path):
                        file.write(f" Belief {i+1}:\n")
                        for row in belief:
                            file.write("  " + " ".join(map(str, row)) + "\n")
                    file.write("\n")
                else:
                    step_matrix = np.array(step).reshape((3, 3))
                    for row in step_matrix:
                        file.write(" ".join(map(str, row)) + "\n")
        else:
            file.write("Không tìm thấy đường đi.\n")

def runPuzzle(start, steps, path, WHITE, BLACK, WidthBoard, HeightBoard, squareSize, boardRows, boardCols, fontBoard, LineWidth):
    global position, prePosition, nextPosition

    screenBoard = pygame.display.set_mode((WidthBoard, HeightBoard))
    FPS = 60
    animating = False
    index = 0
    currentStep = 0
    frames = []

    output_dir = "animations"
    os.makedirs(output_dir, exist_ok=True)
    
    currentState = np.array(start).reshape((3, 3))

    position = {
        start[row][col]: (col * squareSize + squareSize // 2, row * squareSize + squareSize // 2)
        for row in range(boardRows) for col in range(boardCols)
        if start[row][col] != 0
    }

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screenBoard.fill(BLACK)
            drawFigures(screenBoard, fontBoard, position, WHITE, BLACK, boardRows, squareSize, WidthBoard, HeightBoard, LineWidth)
            
            pygame.display.update()

            if not animating and index < len(path) - 1:
                currentState = np.array(path[index + 1]).reshape((3, 3))
                prePosition, nextPosition = animation(boardRows, boardCols, squareSize, path[index], path[index + 1])
                index += 1
                animating = True

            if animating:
                currentStep += 1
                if currentStep < steps:
                    for num in prePosition:
                        x1, y1 = prePosition[num]
                        x2, y2 = nextPosition[num]
                        newX = x1 + (x2 - x1) * (currentStep + 1) / steps
                        newY = y1 + (y2 - y1) * (currentStep + 1) / steps
                        position[num] = (newX, newY)
                else:
                    position = nextPosition.copy()
                    animating = False
                    currentStep = 0

            drawFigures(screenBoard, fontBoard, position, WHITE, BLACK, boardRows, squareSize, WidthBoard, HeightBoard, LineWidth)
            
            frame = pygame.surfarray.array3d(screenBoard)
            frame = np.transpose(frame, (1, 0, 2))
            frames.append(frame)
            
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

            if index > len(path) - 2 and not animating:
                output_path = os.path.join(output_dir, f"puzzle_animation_{algorithm}.gif")
                imageio.mimsave(output_path, frames, fps=FPS)
                print(f"Đã lưu GIF tại: {output_path}")
                pygame.time.wait(2000)
                break

    except Exception as e:
        print(f"Lỗi khi lưu animation: {e}")
        pygame.time.wait(2000)
 
def runPuzzleNoOb(belief_list, path, WHITE, BLACK, WidthBoard, HeightBoard, squareSize, boardRows, boardCols, fontBoard, LineWidth):
    num_boards = len(belief_list)
    total_width = WidthBoard * num_boards
    screenBoard = pygame.display.set_mode((total_width, HeightBoard))
    FPS = 60
    animating = False
    index = 0
    currentStep = 0
    frames = []

    output_dir = "animations"
    os.makedirs(output_dir, exist_ok=True)

    board_width = WidthBoard
    squareSize = board_width // boardCols

    # Khởi tạo vị trí cho từng bảng
    positions = []
    for i, belief in enumerate(belief_list):
        belief_matrix = np.array(belief).reshape((boardRows, boardCols))
        pos = {}
        for row in range(boardRows):
            for col in range(boardCols):
                num = belief_matrix[row][col]
                if num != 0:
                    x = col * squareSize + squareSize // 2 + (i * board_width)
                    y = row * squareSize + squareSize // 2
                    pos[num] = (x, y)
        positions.append(pos)

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screenBoard.fill(BLACK)

            # Vẽ từng bảng với trạng thái hiện tại từ path
            for i in range(num_boards):
                # Lấy trạng thái từ path[index] nếu có, nếu không thì dùng belief_list
                if index < len(path) and i < len(path[index]):
                    belief_matrix = np.array(path[index][i]).reshape((boardRows, boardCols))
                else:
                    belief_matrix = np.array(belief_list[i]).reshape((boardRows, boardCols))
                drawFiguresNoOb(
                    screenBoard, fontBoard, positions[i], belief_matrix, WHITE, BLACK, boardRows, boardCols, squareSize,
                    board_width, HeightBoard, LineWidth, offset_x=i * board_width
                )

            pygame.display.update()

            # Animation
            if not animating and index < len(path) - 1:
                prePositions = positions.copy()
                nextPositions = []
                for i in range(num_boards):
                    # Lấy trạng thái tiếp theo từ path[index + 1]
                    if index + 1 < len(path) and i < len(path[index + 1]):
                        belief = np.array(path[index + 1][i]).reshape((boardRows, boardCols))
                    else:
                        belief = np.array(belief_list[i]).reshape((boardRows, boardCols))
                    belief_matrix = belief
                    pos = {}
                    for row in range(boardRows):
                        for col in range(boardCols):
                            num = belief_matrix[row][col]
                            if num != 0:
                                x = col * squareSize + squareSize // 2 + (i * board_width)
                                y = row * squareSize + squareSize // 2
                                pos[num] = (x, y)
                    nextPositions.append(pos)
                index += 1
                animating = True

            if animating:
                steps = 10
                currentStep += 1
                if currentStep < steps:
                    for i in range(num_boards):
                        for num in prePositions[i]:
                            x1, y1 = prePositions[i][num]
                            x2, y2 = nextPositions[i].get(num, (x1, y1))  # Giữ nguyên nếu số không tồn tại
                            newX = x1 + (x2 - x1) * (currentStep + 1) / steps
                            newY = y1 + (y2 - y1) * (currentStep + 1) / steps
                            positions[i][num] = (newX, newY)
                else:
                    positions = nextPositions.copy()
                    animating = False
                    currentStep = 0

            # Vẽ lại với trạng thái hiện tại từ path
            for i in range(num_boards):
                if index < len(path) and i < len(path[index]):
                    belief_matrix = np.array(path[index][i]).reshape((boardRows, boardCols))
                else:
                    belief_matrix = np.array(belief_list[i]).reshape((boardRows, boardCols))
                drawFiguresNoOb(
                    screenBoard, fontBoard, positions[i], belief_matrix, WHITE, BLACK, boardRows, boardCols, squareSize,
                    board_width, HeightBoard, LineWidth, offset_x=i * board_width
                )

            frame = pygame.surfarray.array3d(screenBoard)
            frame = np.transpose(frame, (1, 0, 2))
            frames.append(frame)

            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

            if index >= len(path) - 1 and not animating:
                output_path = os.path.join(output_dir, f"puzzle_animation_{algorithm}.gif")
                imageio.mimsave(output_path, frames, fps=FPS)
                print(f"Đã lưu GIF tại: {output_path}")
                pygame.time.wait(2000)
                break

    except Exception as e:
        print(f"Lỗi khi lưu animation: {e}")
        pygame.time.wait(2000)
        
# Sửa đổi hàm drawFigures để hỗ trợ offset_x
# def drawFigures(screen, font, position, tile_color, bg_color, boardRows, squareSize, WidthBoard, HeightBoard, LineWidth, offset_x=0):
#     screen.fill(bg_color)
#     for row in range(boardRows + 1):
#         pygame.draw.line(screen, tile_color, (offset_x, row * squareSize), (offset_x + WidthBoard, row * squareSize), LineWidth)
#     for col in range(boardRows + 1):
#         pygame.draw.line(screen, tile_color, (offset_x + col * squareSize, 0), (offset_x + col * squareSize, HeightBoard), LineWidth)

#     for num, (x, y) in position.items():
#         if num != 0:
#             text = font.render(str(num), True, tile_color)
#             text_rect = text.get_rect(center=(x, y))
#             screen.blit(text, text_rect)


def main():
    global screen, algorithm
    algorithmLb = None
    BTN = []
    while True:
        screen = pygame.display.set_mode((Width, Height))
        algorithm = mainMenu(screen, Width, BLUE, GRAY, WHITE, BLACK, algorithmLb, None, BTN)
        
        if algorithm == "BFS":
            start = np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, action = searchBFS(start, end)
            path = BFSRP(start, action)
            timeTaken = timeit.timeit(lambda: searchBFS(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "DFS":
            start = np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, actions = DFS(start, end)
            path = reconstruct_path(start, actions) if actions else None
            timeTaken = timeit.timeit(lambda: DFS(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "UCS":
            start = np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = searchBFS_Heapq(start, end)
            timeTaken = timeit.timeit(lambda: searchBFS_Heapq(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "ID":
            start = np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = ID(start, end)
            timeTaken = timeit.timeit(lambda: ID(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "Greedy":
            start = np.array([[8, 6, 7], [2, 5, 4], [3, 0, 1]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = Greedy(start, end)
            timeTaken = timeit.timeit(lambda: Greedy(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "AStar":
            start = np.array([[8, 6, 7], [2, 5, 4], [3, 0, 1]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = AStar.AStar(start, end)
            timeTaken = timeit.timeit(lambda: AStar.AStar(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "IDAStar":
            start = np.array([[8, 6, 7], [2, 5, 4], [3, 0, 1]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = IDAStar(start, end)
            timeTaken = timeit.timeit(lambda: IDAStar(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "SimpleHillClimbing":
            start = np.array([[2, 6, 5], [0, 8, 7], [3, 1, 4]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = SimpHillClimbing(start, end)
            timeTaken = timeit.timeit(lambda: SimpHillClimbing(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "SHillClimbing":
            start = np.array([[2, 6, 5], [0, 8, 7], [3, 1, 4]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = SteepesHillClimbing(start, end)
            timeTaken = timeit.timeit(lambda: SteepesHillClimbing(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "RHillClimbing":
            start = np.array([[2, 6, 5], [0, 8, 7], [3, 1, 4]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = RandomHillClimbing(start, end)
            timeTaken = timeit.timeit(lambda: RandomHillClimbing(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "SimulatedAnne":
            start = np.array([[2, 6, 5], [0, 8, 7], [3, 1, 4]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            steps, path, bestState, spaceState = SimulatedAnnealing(start, end)
            timeTaken = timeit.timeit(lambda: SimulatedAnnealing(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "Beam Search":
            start = np.array([[2, 6, 5], [0, 8, 7], [3, 1, 4]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = BeamSearch(start, end, 10)
            timeTaken = timeit.timeit(lambda: BeamSearch(start, end, 10), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "Genetic Algorithm":
            start = np.array([[2, 6, 5], [0, 8, 7], [3, 1, 4]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = GeneticAlgorithm(start, end, 100, 1000, 0.1)
            timeTaken = timeit.timeit(lambda: GeneticAlgorithm(start, end, 100, 1000, 0.1), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "AND_OR":
            start = np.array([[2, 8, 3], [7, 0, 4], [1, 6, 5]])
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            spaceState, path = AND_OR(start, end)
            timeTaken = timeit.timeit(lambda: AND_OR(start, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "NoOb":
            listStart = BeliefList(5)
            end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
            path, spaceState = AStarNoOb(listStart, end)
            timeTaken = timeit.timeit(lambda: AStarNoOb(listStart, end), number=1)
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
            if path is not None and len(path) > 0:
                runPuzzleNoOb(listStart, path, WHITE, BLACK, WidthBoard, HeightBoard, squareSize, boardRows, boardCols, fontBoard, LineWidth)
            else:
                print("Không tìm thấy đường đi cho NoOb.")
        
        elif algorithm == "SeePartOfMatrix":
            start = [[2, '?', '?'], ['?', 8, '?'], ['?', '?', 1]]
            goal_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
            path, runtime, spaceState = SeePartOfMatrix(start, goal_state)
            save_result_to_file("KetQua.txt", algorithm, runtime, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, runtime, path, spaceState)
        
        elif algorithm == "CSPBacktracking":
            startTime = time.time()
            spaceState, path = CSPBackTracking()
            endTime = time.time()
            timeTaken = endTime - startTime
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        elif algorithm == "QLearning":
            start = np.array([[8, 6, 7], [2, 5, 4], [3, 0, 1]])
            startTime = time.time()
            QLearning(start)
            spaceState, path = solve_QLearning(start, qTable)
            endTime = time.time()
            timeTaken = endTime - startTime
            save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
            log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        
        else:
            print("Ko dung")
            return
        
        if algorithm != "NoOb":
            runPuzzle(start, 10, path, WHITE, BLACK, WidthBoard, HeightBoard, squareSize, boardRows, boardCols, fontBoard, LineWidth)
            
        # if algorithm == "NoOb":
        #     listStart = BeliefList(5)
        #     end = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        #     path, spaceState = AStarNoOb(listStart, end)
        #     timeTaken = timeit.timeit(lambda: AStarNoOb(listStart, end), number=1)
        #     save_result_to_file("KetQua.txt", algorithm, timeTaken, path, spaceState)
        #     log_selection_to_file("Selections.json", algorithm, timeTaken, path, spaceState)
        #     runPuzzleNoOb(listStart, path, WHITE, BLACK, WidthBoard, HeightBoard, squareSize, boardRows, boardCols, fontBoard, LineWidth)

if __name__ == "__main__":
    main()