import pygame
from function.btns.drawLines import drawLines


def drawFigures(screen,font,position,WHITE,BLACK,boardRows,squareSize,WidthBoard,HeightBoard,LineWidth):
        screen.fill(BLACK)
        drawLines(screen,boardRows,WHITE,squareSize,WidthBoard,HeightBoard,LineWidth)
        for num, (x,y) in position.items():
            if num != 0:  # Không vẽ ô trống (0)
                textSurface = font.render(str(num), True, WHITE)
                textRect = textSurface.get_rect(center=(x, y))
                screen.blit(textSurface, textRect)
        pygame.display.update()