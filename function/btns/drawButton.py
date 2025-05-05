import pygame

def drawBtn(screen, font, BLUE, GRAY, White, button,hovered):
    label,rect=button
    colorBtn=(255, 64, 64) if hovered else (0, 206, 209)
    textColor=White if hovered else (240, 240, 240)
    
    shadowRect=pygame.Rect(rect.x+2,rect.y+2,rect.width,rect.height)
    pygame.draw.rect(screen,(50, 50, 50, 50),shadowRect, border_radius=10)
    
    pygame.draw.rect(screen,colorBtn,rect,border_radius=10)
    
    pygame.draw.rect(screen,(100, 100, 100),rect,width=2,border_radius=10)
    
    text=font.render(label,True,textColor)
    textRect=text.get_rect(center=rect.center)
    screen.blit(text,textRect)
    