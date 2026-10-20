"""
The first step of implementing the code
"""
import sys
import pygame
from Menu import MainMenu
from app import App
from parsing.parsing import parse_config
def init_screen() -> tuple[pygame.Surface, pygame.Surface]:
    pygame.init()

    screen = pygame.display.set_mode((800, 600)) # create a window 
    buffer = pygame.Surface((800, 600)) # draw a surface
    pygame.display.set_caption("Pac Man Sboo3a")

    return screen, buffer

def flip(screen: pygame.Surface, buffer: pygame.Surface) -> None:
    screen.blit(buffer, (0, 0)) # copy your drawing surface onto the display surface

def fill_screen(screen: pygame.Surface, color: tuple[int, int, int]) -> None:
    """
    This fills the surface with black, reproducing the functionality of:

    screen.fill((0, 0, 0))
    """
    width, height = screen.get_size()

    y = 0
    while y < height:
        x = 0
        while x < width:
            screen.set_at((x, y), color) # modifies a pixel in a Pygame surface, but it does not immediately present the completed frame
            x += 1
        y += 1


def game_loop(screen: pygame.Surface , buffer : pygame.Surface) -> None:
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fill_screen(screen , (0, 0, 0))
        flip(screen , buffer)

    pygame.quit()




def main() -> None:
    
    # menu = MainMenu()
    # menu.run()
    # config = parse_config("config.json")

    if len(sys.argv) != 2:
        print("Usage: python3 main.py <config.json>", file=sys.stderr)
        return 1

    try:
        config = parse_config(sys.argv[1])
    except Exception as error:
        print(f"Error: cannot load configuration: {error}", file=sys.stderr)
        return 1


    try:
        pac_man = App(config)
        pac_man.run()
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    main()