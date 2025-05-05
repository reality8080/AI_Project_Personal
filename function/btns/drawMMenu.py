import pygame
import sys

from function.btns.drawButton import drawBtn
from function.btns.createBtns import createBtn
from function.btns.handleBtn import handleBtn

def mainMenu(screen,Width,BLUE, GRAY, White,BLACK, algorithm,time,BTN):
    font=pygame.font.Font(None,30)
    btns=createBtn()
    
    while True:
        screen.fill(White)
        tittle=font.render("Select Search Algorithm", True,BLACK)
        tittleRect=tittle.get_rect(center=(Width//2,50))
        screen.blit(tittle,tittleRect)
        
        mousePos=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                selectedAlgorithm=handleBtn(btns,mousePos)
                if selectedAlgorithm:
                    return selectedAlgorithm
            
        for btn in btns:
            hovered=btn[1].collidepoint(mousePos)
            drawBtn(screen,font,BLUE, GRAY, White,btn,hovered)
        # if time and algorithm:
        #     tittle=font.render(f"Thoi gian chay {algorithm} la: {time}", True,BLACK)
        #     tittleRect=tittle.get_rect(center=(500,300))
        #     screen.blit(tittle,tittleRect)
        # if BTN:
        #     y_offset = 350  # Vị trí dòng đầu tiên
        # for step in BTN:
        #     step_text = ",".join([" ".join(map(str, row)) for row in step])  # Chuyển ma trận 3x3 thành dạng dòng
        #     for idx, line in enumerate(step_text.split("\n")):  # Tách từng dòng của ma trận
        #         text_surface = font.render(line, True, BLACK)
        #         text_rect = text_surface.get_rect(center=(400, y_offset + idx * 20))
        #         screen.blit(text_surface, text_rect)
        #     y_offset += 100  # Khoảng cách giữa các ma trận
        pygame.display.update()