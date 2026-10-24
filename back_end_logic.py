"""Player and ghosts: attributes only, the logic is up to the peer."""
from __future__ import annotations

from enum import Enum, auto
from typing import Optional

Cell = tuple[int, int]

PLAYER_SPEED = 5.0          # cells per second
GHOST_SPEED = 4.0
GHOST_FLEE_SPEED = 2.5
GHOST_RESPAWN_DELAY = 8.0   # seconds before an eaten ghost comes back


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class GhostState(Enum):
    CHASE = auto()      # chases the player, can hurt him
    FLEE = auto()       # edible: runs away, can be eaten
    EATEN = auto()      # eaten: waits in its corner, then comes back


class Entity:
    """Something that moves from cell to cell on the maze grid."""

    def __init__(self, start: Cell, speed: float) -> None:
        self.start = start                     # cell it (re)spawns on
        self.speed = speed                     # cells per second
        self.cell: Cell = start                # cell it is on (or just left)
        self.target: Optional[Cell] = None     # neighbor it is moving to
        self.progress = 0.0                    # 0.0 to 1.0 toward target
        self.direction = Direction.LEFT        # last direction


class Player(Entity):
    def __init__(self, start: Cell) -> None:
        super().__init__(start, PLAYER_SPEED)
        self.wanted: Optional[Direction] = None   # last key pressed
        self.speed_multiplier = 1.0               # changed by the cheat mode


class Ghost(Entity):
    def __init__(self, name: str, corner: Cell) -> None:
        super().__init__(corner, GHOST_SPEED)
        self.name = name
        self.state = GhostState.CHASE
        self.respawn_timer = 0.0
        self.frozen = False                    # set by the cheat mode