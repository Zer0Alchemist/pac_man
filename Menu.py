
# import pygame
# import sys
# from pathlib import Path


# class MainMenu:
#     WIDTH = 1400
#     HEIGHT = 900

#     BLACK = (0, 0, 0)
#     YELLOW = (255, 210, 40)
#     WHITE = (255, 255, 255)
#     GRAY = (140, 140, 140)

#     OPTIONS = [
#         "Start Game",
#         "View Highscores",
#         "Instructions",
#         "Exit",
#     ]
    
#     BACKGROUND = (244, 164, 96)

#     def __init__(self) -> None:
#         pygame.init()

#         self.screen = pygame.display.set_mode(
#             (self.WIDTH, self.HEIGHT)
#         )
#         pygame.display.set_caption("Pac-Man")

#         self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
#         for y in range(self.HEIGHT):
#             for x in range(self.WIDTH):
#                 self.background.set_at((x, y), self.BACKGROUND)
        
        
#         # color = (244,164,96)

#         # self.screen.fill(color)
#         # pygame.display.flip()
#         self.clock = pygame.time.Clock()
#         self.running = True
#         self.selected = 0

#         self.menu_font = pygame.font.SysFont(
#             "monospace", 38, bold=True
#         )
#         self.info_font = pygame.font.SysFont(
#             "monospace", 18
#         )

#         ASSETS_DIR = Path(__file__).parent / "assets" / "pac_man_title"
#         # TITLE_IMAGE = ASSETS_DIR / "pac_man_title.png"
#         TITLE_IMAGE = Path(
#         "/home/manzar/Desktop/42Cursus/pac_man/assets/pac_man_title/pac_man_title_transparent.png")
#         # print(TITLE_IMAGE)
#         print(TITLE_IMAGE.exists())
#         # image = pygame.image.load(str(TITLE_IMAGE)).convert()
#         image = self.load_title(TITLE_IMAGE)
#         title_width = 700
#         title_height = int(
#             image.get_height() * title_width / image.get_width()
#         )

#         self.title = pygame.transform.scale(
#             image, (title_width, title_height)
#         )

#     def load_title(self, title_image: Path) -> pygame.Surface:
#         image = pygame.image.load(str(title_image)).convert_alpha()
#         # no set_colorkey needed anymore
#         title_width = 700
#         title_height = int(image.get_height() * title_width / image.get_width())
#         return pygame.transform.scale(image, (title_width, title_height))
    
#     def clear_screen(self) -> None:
#         """Clear the screen using pixel operations."""
#         # y = 0
#         # while y < self.HEIGHT:
#         #     x = 0
#         #     while x < self.WIDTH:
#         #         self.screen.set_at((x, y), self.BACKGROUND)
#         #         x += 1
#         #     y += 1
#         # self.screen.fill(self.BACKGROUND)
#         self.screen.blit(self.background, (0, 0))

#     def draw_text(
#         self,
#         text: str,
#         color: tuple[int, int, int],
#         y: int,
#         font: pygame.font.Font,
#     ) -> None:
#         """Draw centered text."""
#         text_surface = font.render(text, True, color)
#         text_rect = text_surface.get_rect(
#             center=(self.WIDTH // 2, y)
#         )
#         self.screen.blit(text_surface, text_rect)

#     def draw(self) -> None:
#         self.clear_screen()

#         # Display the only image: the Pac-Man title.
#         title_rect = self.title.get_rect(
#             center=(self.WIDTH // 2, 125)
#         )
#         self.screen.blit(self.title, title_rect)

#         # Draw the large menu options.
#         for index, option in enumerate(self.OPTIONS):
#             y = 310 + index * 75

#             if index == self.selected:
#                 color = self.YELLOW
#                 text = f">  {option}  <"
#             else:
#                 color = self.WHITE
#                 text = option

#             self.draw_text(text, color, y, self.menu_font)

#         self.draw_text(
#             "UP / DOWN: SELECT     ENTER: CONFIRM",
#             self.GRAY,
#             610,
#             self.info_font,
#         )

#         pygame.display.flip()

#     def handle_events(self) -> None:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False

#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     self.selected = (
#                         self.selected - 1
#                     ) % len(self.OPTIONS)

#                 elif event.key == pygame.K_DOWN:
#                     self.selected = (
#                         self.selected + 1
#                     ) % len(self.OPTIONS)

#                 elif event.key == pygame.K_RETURN:
#                     self.select_option()

#                 elif event.key == pygame.K_ESCAPE:
#                     self.running = False

#     def select_option(self) -> None:
#         option = self.OPTIONS[self.selected]

#         if option == "Start Game":
#             print("Start Game selected")

#         elif option == "View Highscores":
#             print("View Highscores selected")

#         elif option == "Instructions":
#             print("Instructions selected")

#         elif option == "Exit":
#             self.running = False

#     def run(self) -> None:
#         while self.running:
#             self.handle_events()
#             self.draw()
#             self.clock.tick(60)

#         pygame.quit()
#         sys.exit()

import pygame

from screens import Screen , State
from typing import Optional


from pathlib import Path
from typing import Optional

import pygame

from screens import Screen, State


class MainMenu(Screen):
    BACKGROUND = (244, 164, 96)
    YELLOW = (255, 210, 40)
    WHITE = (255, 255, 255)
    GRAY = (140, 140, 140)

    OPTIONS = [
        ("Start Game", State.PLAYING),
        ("View Highscores", State.HIGHSCORES),
        ("Instructions", State.INSTRUCTIONS),
        ("Exit", State.EXIT),
    ]

    TITLE_PATH = (Path(__file__).parent / "assets" / "pac_man_title"
                  / "pac_man_title_transparent.png")

    def __init__(self, size: tuple[int, int]) -> None:
        self.width, self.height = size
        self.selected = 0

        # Background: built once, copied every frame
        self.background = pygame.Surface(size)
        self.background.fill(self.BACKGROUND)

        self.menu_font = pygame.font.SysFont("monospace", 38, bold=True)
        self.info_font = pygame.font.SysFont("monospace", 18)

        self.title = self.load_title(self.TITLE_PATH)

    def load_title(self, path: Path) -> Optional[pygame.Surface]:
        """Load and scale the title image, or return None if it fails."""
        try:
            image = pygame.image.load(str(path)).convert_alpha()
        except (pygame.error, FileNotFoundError) as error:
            print(f"Could not load title image: {error}")
            return None
        title_width = 700
        title_height = int(image.get_height() * title_width / image.get_width())
        return pygame.transform.scale(image, (title_width, title_height))

    def handle_event(self, event: pygame.event.Event) -> Optional[State]:
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.OPTIONS)
        elif event.key == pygame.K_RETURN:
            return self.OPTIONS[self.selected][1]
        elif event.key == pygame.K_ESCAPE:
            return State.EXIT
        return None

    def draw_text(self, surface: pygame.Surface, text: str,
                  color: tuple[int, int, int], y: int,
                  font: pygame.font.Font) -> None:
        """Draw horizontally centered text."""
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(self.width // 2, y))
        surface.blit(text_surface, rect)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        if self.title is not None:
            rect = self.title.get_rect(center=(self.width // 2, 125))
            surface.blit(self.title, rect)
        else:
            self.draw_text(surface, "PAC-MAN", self.YELLOW, 125, self.menu_font)

        for index, (label, _) in enumerate(self.OPTIONS):
            y = 310 + index * 75
            if index == self.selected:
                color, text = self.YELLOW, f">  {label}  <"
            else:
                color, text = self.WHITE, label
            self.draw_text(surface, text, color, y, self.menu_font)

        self.draw_text(surface, "UP / DOWN: SELECT     ENTER: CONFIRM",
                       self.GRAY, 650, self.info_font)