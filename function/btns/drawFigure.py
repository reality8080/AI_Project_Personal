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

def drawFiguresNoOb(screen, font, position, belief_matrix, tile_color, bg_color, boardRows, boardCols, squareSize, board_width, HeightBoard, LineWidth, offset_x=0, belief_index=None):
    screen.fill((255, 255, 255))  # Clear screen

    rows = len(belief_matrix)
    cols = len(belief_matrix[0])

    cell_size = min(board_width // cols, HeightBoard // rows)
    font = pygame.font.SysFont(None, cell_size // 2)

    for row in range(rows):
        for col in range(cols):
            value = belief_matrix[row][col]
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)