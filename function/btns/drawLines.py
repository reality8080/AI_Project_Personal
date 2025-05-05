import pygame

def drawLines(screen,boardRows,WHITE,squareSize,WidthBoard,HeightBoard,LineWidth):
        for i in range(1, boardRows):
            pygame.draw.line(screen,WHITE, start_pos=(0, i*squareSize), end_pos=(WidthBoard, i*squareSize), width=LineWidth)
            pygame.draw.line(screen,WHITE, start_pos=(i*squareSize, 0), end_pos=(i*squareSize, HeightBoard), width=LineWidth)