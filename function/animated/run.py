import pygame
import numpy as np
import sys

from function.btns.drawFigure import drawFigures
from function.animated.animation import animation


def runPuzzle(start, steps, path,WHITE,BLACK,WidthBoard, HeightBoard,squareSize,boardRows,boardCols,fontBoard,LineWidth):
    global position, prePosition, nextPosition

    screenBoard = pygame.display.set_mode((WidthBoard, HeightBoard))
    FPS = 144
    animating=False
    index = 0          
    currentStep=0

    currentState = np.array(start).reshape((3, 3))

    position = {
        start[row][col]: (col * squareSize + squareSize // 2, row * squareSize + squareSize // 2)
        for row in range(boardRows) for col in range(boardCols)
        if start[row][col] != 0
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screenBoard.fill(BLACK)
        drawFigures(screenBoard,fontBoard,position,WHITE,BLACK,boardRows,squareSize,WidthBoard,HeightBoard,LineWidth)
        pygame.display.update()

        if not animating and index<len(path)-1:
            currentState=np.array(path[index+1]).reshape((3,3))
            prePosition,nextPosition=animation(boardRows,boardCols,squareSize,path[index], path[index+1])
            index+=1
            animating=True

        # currenTime= pygame.time.get_ticks()
        if animating:
            currentStep+=1
            if currentStep<steps:
                for num in prePosition:
                    x1,y1=prePosition[num]
                    x2,y2=nextPosition[num]
                    newX=x1+(x2-x1)*(currentStep+1)/steps
                    newY=y1+(y2-y1)*(currentStep+1)/steps
                    position[num]=(newX,newY)
            else:
                position=nextPosition.copy()
                animating=False
                currentStep=0
            # pygame.time.delay(10)
        # drawF.drawFigures(screenBoard, start if index==0 else path[index], position,Color.WHITE,Color.BLACK,font.font_board,Config.squareSize)
        drawFigures(screenBoard,fontBoard,position,WHITE,BLACK,boardRows,squareSize,WidthBoard,HeightBoard,LineWidth)
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

        if index>len(path)-2 and not animating:
            pygame.time.wait(4000)
            return