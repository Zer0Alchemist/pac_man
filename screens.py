from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional

import pygame


class State(Enum):
    MENU = auto()
    PLAYING = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    EXIT = auto()


class Screen(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[State]:
        """Return a new State to switch screen, or None to stay."""

    def update(self, dt: float) -> None:
        """Advance logic by dt seconds (menus can ignore this)."""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw onto the window surface."""