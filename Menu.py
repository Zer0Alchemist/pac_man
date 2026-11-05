# import pygame

# from screens import Screen , State
# from typing import Optional


# from pathlib import Path
# from typing import Optional

# import pygame

# from screens import Screen, State


# class MainMenu(Screen):
#     BACKGROUND = (244, 164, 96)
#     YELLOW = (255, 210, 40)
#     WHITE = (255, 255, 255)
#     GRAY = (140, 140, 140)

#     OPTIONS = [
#         ("Start Game", State.PLAYING),
#         ("View Highscores", State.HIGHSCORES),
#         ("Instructions", State.INSTRUCTIONS),
#         ("Exit", State.EXIT),
#     ]

#     TITLE_PATH = (Path(__file__).parent / "assets" / "pac_man_title"
#                   / "pac_man_title_transparent.png")

#     def __init__(self, size: tuple[int, int]) -> None:
#         self.width, self.height = size
#         self.selected = 0

#         # Background: built once, copied every frame
#         self.background = pygame.Surface(size)
#         self.background.fill(self.BACKGROUND)

#         self.menu_font = pygame.font.SysFont("monospace", 38, bold=True)
#         self.info_font = pygame.font.SysFont("monospace", 18)

#         self.title = self.load_title(self.TITLE_PATH)

#     def load_title(self, path: Path) -> Optional[pygame.Surface]:
#         """Load and scale the title image, or return None if it fails."""
#         try:
#             image = pygame.image.load(str(path)).convert_alpha()
#         except (pygame.error, FileNotFoundError) as error:
#             print(f"Could not load title image: {error}")
#             return None
#         title_width = 700
#         title_height = int(image.get_height() * title_width / image.get_width())
#         return pygame.transform.scale(image, (title_width, title_height))

#     def handle_event(self, event: pygame.event.Event) -> Optional[State]:
#         if event.type != pygame.KEYDOWN:
#             return None
#         if event.key == pygame.K_UP:
#             self.selected = (self.selected - 1) % len(self.OPTIONS)
#         elif event.key == pygame.K_DOWN:
#             self.selected = (self.selected + 1) % len(self.OPTIONS)
#         elif event.key == pygame.K_RETURN:
#             return self.OPTIONS[self.selected][1]
#         elif event.key == pygame.K_ESCAPE:
#             return State.EXIT
#         return None

#     def draw_text(self, surface: pygame.Surface, text: str,
#                   color: tuple[int, int, int], y: int,
#                   font: pygame.font.Font) -> None:
#         """Draw horizontally centered text."""
#         text_surface = font.render(text, True, color)
#         rect = text_surface.get_rect(center=(self.width // 2, y))
#         surface.blit(text_surface, rect)

#     def draw(self, surface: pygame.Surface) -> None:
#         surface.blit(self.background, (0, 0))

#         if self.title is not None:
#             rect = self.title.get_rect(center=(self.width // 2, 125))
#             surface.blit(self.title, rect)
#         else:
#             self.draw_text(surface, "PAC-MAN", self.YELLOW, 125, self.menu_font)

#         for index, (label, _) in enumerate(self.OPTIONS):
#             y = 310 + index * 75
#             if index == self.selected:
#                 color, text = self.YELLOW, f">  {label}  <"
#             else:
#                 color, text = self.WHITE, label
#             self.draw_text(surface, text, color, y, self.menu_font)

#         self.draw_text(surface, "UP / DOWN: SELECT     ENTER: CONFIRM",
#                        self.GRAY, 650, self.info_font)


from pathlib import Path
from typing import Optional

import pygame

# from gfx import BitmapFont, GfxError, Image, load_image, new_image, put_image
from screens import Screen, State


# class MainMenu(Screen):
#     BACKGROUND = (244, 164, 96)
#     YELLOW = (255, 210, 40)
#     WHITE = (255, 255, 255)
#     HELP_COLOR = (100, 55, 20)

#     OPTIONS = [
#         ("Start Game", State.PLAYING),
#         ("View Highscores", State.HIGHSCORES),
#         ("Instructions", State.INSTRUCTIONS),
#         ("Exit", State.EXIT),
#     ]

#     TITLE_PATH = (Path(__file__).parent / "assets" / "pac_man_title"
#                   / "pac_man_title_transparent.png")


#     def __init__(self, size: tuple[int, int]) -> None:
#         self.width, self.height = size
#         self.selected = 0
#         font = BitmapFont()

#         # built once: the loop of set_at runs here, not every frame
#         self.background = new_image(self.width, self.height,
#                                     transparent=False)
#         self.background.fill_rect(0, 0, self.width, self.height,
#                                   self.BACKGROUND)

#         try:
#             self.title = load_image(self.TITLE_PATH)
#         except GfxError as error:
#             print(f"Warning: {error}")
#             self.title = font.render("PAC-MAN", self.YELLOW, 12)

#         # every label in both states, rendered once
#         self.labels = [
#             (font.render(label, self.WHITE, 5),
#              font.render(f">  {label}  <", self.YELLOW, 5))
#             for label, _ in self.OPTIONS
#         ]
#         self.help = font.render("UP / DOWN: SELECT     ENTER: CONFIRM",
#                                 self.HELP_COLOR, 2)

#     def handle_event(self, event: pygame.event.Event) -> Optional[State]:
#         if event.type != pygame.KEYDOWN:
#             return None
#         if event.key == pygame.K_UP:
#             self.selected = (self.selected - 1) % len(self.OPTIONS)
#         elif event.key == pygame.K_DOWN:
#             self.selected = (self.selected + 1) % len(self.OPTIONS)
#         elif event.key == pygame.K_RETURN:
#             return self.OPTIONS[self.selected][1]
#         elif event.key == pygame.K_ESCAPE:
#             return State.EXIT
#         return None

#     def put_centered(self, surface: pygame.Surface, image: Image,
#                      center_y: int) -> None:
#         put_image(surface, image, (self.width - image.width) // 2,
#                   center_y - image.height // 2)

#     def draw(self, surface: pygame.Surface) -> None:
#         put_image(surface, self.background, 0, 0)
#         self.put_centered(surface, self.title, 125)
#         for i, (normal, selected) in enumerate(self.labels):
#             image = selected if i == self.selected else normal
#             self.put_centered(surface, image, 310 + i * 75)
#         self.put_centered(surface, self.help, 650)


from gfx import Bit_map_font

class MainMenu(Screen):

    BACKGROUND = (244, 164, 96) # lemmon clr
    YELLOW = (255, 210, 40) # yellow clr
    WHITE = (255, 255, 255) # white clr
    HELP_COLOR = (100, 55, 20) # help clr

    TITLE_PATH = (Path(__file__).parent / "assets" / "pac_man_title"
                      / "pac_man_title_transparent.png")

    

    OPTIONS = [
            ("Start Game", State.PLAYING),
            ("View Highscores", State.HIGHSCORES),
            ("Instructions", State.INSTRUCTIONS),
            ("Exit", State.EXIT),
        ]

    labels = [
        "START GAME",
        "VIEW HIGHSCORES",
        "INSTRUCTIONS",
        "EXIT"
        ]

    help = "UP / DOWN: SELECT     ENTER: CONFIRM"

    TITLE_PATH = (Path(__file__).parent / "assets" / "pac_man_title"
                      / "pac_man_title_transparent.png")

    def __init__(self , size):
        self.width , self.height = size
        self.selected = 0
        



        self.title = pygame.image.load(self.TITLE_PATH)
        self.image_width = self.title.get_width()
        self.image_height = self.title.get_height()
        self.x_image , self.y_image = (self.width - self.image_width) // 2 , 20


    def draw_image(self , screen : pygame.Surface) :
        screen.blit(self.title , (self.x_image , self.y_image))


    def handle_event(self , event) ->Optional[State]:
        if event.type != pygame.KEYDOWN :
            return None
        
        if event.key == pygame.K_UP :
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        elif event.key == pygame.K_DOWN :
            self.selected = (self.selected + 1) % len(self.OPTIONS)
        elif event.key == pygame.K_RETURN :
            return self.OPTIONS[self.selected][1]
        elif event.key == pygame.K_ESCAPE:
            return State.EXIT
        return None

    def draw(self , screen : pygame.Surface):
        font = Bit_map_font(screen , (self.width , self.height))
        spacing_text = self.height * 0.09
        start_y_text = self.height * 0.34
        last_y = 0
        screen.fill(self.BACKGROUND)
        self.draw_image(screen)
        for index , label in enumerate(self.labels):
            y = int(start_y_text + index * spacing_text)
            last_y = y
            color = "white"
            if index == self.selected :
                color = "yellow"
                label = f">  {label}  <"
    
            font.draw_centered_text(label , y , color , 5)
    
        font.draw_centered_text(self.help , int(last_y + spacing_text * 2)  , "black" , 2)
