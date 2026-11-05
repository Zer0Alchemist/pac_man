

import pygame

pygame.init()



screen = pygame.display.set_mode((700 , 700))
pygame.display.set_caption("Test")

text_font = pygame.font.SysFont("Arial",26)

def draw_text(text : str , font : pygame.font.Font , text_col , x , y):

    img  = font.render(text , True , text_col)
    screen.blit(img , (x , y))

running = True


while (running):

    screen.fill((255 , 255 , 255))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False

    draw_text("Hello world" , text_font , (0,0,0) , 300 , 300)

    pygame.display.flip()
    # pygame.display.update()


pygame.quit()