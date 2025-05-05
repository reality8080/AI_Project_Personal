import numpy as np

def animation(boardRows,boardCols,squareSize,pre,next):
    # animating=True
    # currentStep=0
    pre = np.array(pre).reshape((3, 3))
    next = np.array(next).reshape((3, 3))
    prePosition={
        pre[row][col]:(col*squareSize+squareSize//2,row*squareSize+squareSize//2)
        for row in range(boardRows) for col in range(boardCols)
        if pre[row][col]!=0
    }
    nextPosition={
        next[row][col]:(col*squareSize+squareSize//2,row*squareSize+squareSize//2)
        for row in range(boardRows) for col in range(boardCols)
        if next[row][col]!=0
    }
    # pygame.display.update()
    return prePosition, nextPosition