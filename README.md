### Pygame foundamentals


## Creating a window 

screen = pygame.display.set_mode((700 , 700))
pygame.display.set_caption("Test")

running = True 

while running :

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False

pygame.quit()


## How to draw a text 


text_font = pygame.font.SysFont("Arial" , 16)


def draw_text(text , font , text_col , x , y) :
    img = font.render(text , True , text_col)
    screen.blit(img , (x , y))

## the difference between screen.blit(surface , dest) and pygame.display.flip() and pygame.display.update()

screen.blit(surface , dest) it copies bytes from a surface to the screen but it doesn't update the screen

pygame.display.flip() it updates the  whole screen like buffering 

pygame.display.update() it updates the whole screen and it can also update a specific region from the screen 
and cannot be used with an OpenGL display mode
