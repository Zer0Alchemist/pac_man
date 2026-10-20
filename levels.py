from dataclasses import dataclass
from enum import Enum, auto
import mazegenerator



class Result(Enum):
    RUNNING = auto()
    LEVEL_COMPLETE = auto()
    LIFE_LOST = auto()
    TIME_UP = auto()


@dataclass
class Session:
    """Survives between levels."""
    score: int = 0
    lives: int = 3
    level_index: int = 0          # 0-based

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
CLOSED = 15          # a cell with 4 walls = part of the "42"

class Level:
    """Rebuilt for every level."""

    def __init__(self, maze: list[str], max_time: int) -> None:
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        # the cells of the "42", stored as (x, y)
        self.pattern_cells = {
            (x, y)
            for y, row in enumerate(maze)
            for x, value in enumerate(row)
            if value == CLOSED
        }
        self.max_time = float(max_time)
        self.time_left = self.max_time
        # placeholder until pacgums exist, so the level doesn't end instantly
        self.pacgums_left = self.rows * self.cols - len(self.pattern_cells)


    def reset_timer(self) -> None:
        self.time_left = self.max_time

    def respawn_entities(self) -> None:
        """Put the player and ghosts back at their start. Keep the pacgums."""

    def update(self, dt: float, session: Session) -> Result:
        self.time_left -= dt
        if self.pacgums_left == 0:
            return Result.LEVEL_COMPLETE
        if self.time_left <= 0:
            return Result.TIME_UP
        # later: move player and ghosts, check collisions, return LIFE_LOST
        return Result.RUNNING
