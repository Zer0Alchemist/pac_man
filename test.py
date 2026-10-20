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


# os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


# import pygame

# pygame.init()

# # creating a window 
# py_window = pygame.display.set_mode((500 , 500)) # return a surface
# pygame.display.set_caption("test")

# pygame_clock = pygame.time.Clock() # set the frame rate



# running = True



# while running :
#     for event in pygame.event.get() :
#         if event.type == pygame.QUIT :
#             running = False

#     pygame.display.update()
#     pygame_clock.tick(60) # 60 frames per second

# pygame.quit()

object_maze = mazegenerator.MazeGenerator()

print(object_maze.maze)