from screens import Screen , State
import pygame
from typing import Optional

class GameScreen(Screen):
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.paused = False
        # later: Engine / GameState goes here

    def handle_event(self, event: pygame.event.Event) -> Optional[State]:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return State.MENU      # later: toggle the pause menu instead
        return None

    def update(self, dt: float) -> None:
        if not self.paused:
            pass                       # later: engine.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))        # later: draw maze, entities, HUD