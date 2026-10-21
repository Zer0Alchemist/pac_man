# ---- This is for extracting the background of the image ----- #

# from PIL import Image

# SRC = "assets/pac_man_title/pac _man _ tile _ 1.png"
# DST = "assets/pac_man_title/pac_man_title_transparent.png"

# img = Image.open(SRC).convert("RGBA")
# pixels = img.load()
# width, height = img.size

# for y in range(height):
#     for x in range(width):
#         r, g, b, a = pixels[x, y]
#         # Near-white and light-gray pixels with no color = checkerboard squares
#         if min(r, g, b) >= 200 and max(r, g, b) - min(r, g, b) <= 12:
#             pixels[x, y] = (r, g, b, 0)

# img.save(DST)


# ---- Pygame training ---- #

import os

import mazegenerator


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


import pygame

pygame.init()

def draw(window) :
    window.fill("blue")
    pygame.draw.rect(window ,(2 , 239 , 238 ), player)

# creating a window 
py_window = pygame.display.set_mode((500 , 500)) # return a surface
pygame.display.set_caption("test")

pygame_clock = pygame.time.Clock() # set the frame rate



running = True

player = pygame.Rect(120 , 120 , 50 , 50)




while running :
    for event in pygame.event.get() : # listen on evenets coming from the mouse or the keyboard or from a button in a window
        if event.type == pygame.QUIT :
            running = False

        # if event.type == pygame.KEYDOWN :
        #     if event.key == pygame.K_SPACE :
        #         print("space pressed")
        # if event.type == pygame.KEYUP :
        #     if event.key == pygame.K_SPACE:
        #         print("space released")

        # if event.type == pygame.KEYDOWN :
        #     if event.key == pygame.K_UP :
        #         player.y -= 5
        #     if event.key == pygame.K_DOWN :
        #         player.y += 5
        #     if event.key == pygame.K_RIGHT :
        #         player.x += 5
        #     if event.key == pygame.K_LEFT :
        #         player.x -= 5
    
    draw(py_window)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] :
        player.y -= 5

    if keys[pygame.K_DOWN] :
        player.y += 5

    if keys[pygame.K_RIGHT]:
        player.x += 5

    if keys[pygame.K_LEFT]:
        player.x -= 5

    pygame.display.update()

    pygame_clock.tick(60) # 60 frames per second

pygame.quit()

