from dataclasses import dataclass
from enum import Enum, auto
import mazegenerator


NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
CLOSED = 15          # a cell with 4 walls = part of the "42"


from collections import deque
from typing import Optional

Cell = tuple[int, int]

# (dx, dy, wall on this side, wall on the neighbor's side)
DIRECTIONS = (
    (0, -1, NORTH, SOUTH),
    (1, 0, EAST, WEST),
    (0, 1, SOUTH, NORTH),
    (-1, 0, WEST, EAST),
)
EDIBLE_DURATION = 8.0      # seconds the ghosts stay edible


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


class Level:
    """Rebuilt for every level."""

    def __init__(self, maze: list[list[int]], max_time: int) -> None:
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.pattern_cells: set[Cell] = {
            (x, y)
            for y, row in enumerate(maze)
            for x, value in enumerate(row)
            if value == CLOSED
        }
        self.max_time = float(max_time)
        self.time_left = self.max_time
        self.edible_time = 0.0

        # the player starts in the middle, the ghosts will start in the corners
        self.start = self.nearest_open(self.cols // 2, self.rows // 2)
        self.corners = [
            self.nearest_open(x, y)
            for x, y in ((0, 0), (self.cols - 1, 0),
                         (0, self.rows - 1),
                         (self.cols - 1, self.rows - 1))
        ]

        # only cells the player can really walk to get a pacgum,
        # otherwise a level could be impossible to finish
        reachable = self.reachable_from(self.start)
        self.super_pacgums: set[Cell] = {c for c in self.corners
                                         if c in reachable}
        self.pacgums: set[Cell] = reachable - self.super_pacgums - {self.start}

    # ---------- maze queries ----------

    def is_open(self, x: int, y: int) -> bool:
        """True if the cell is inside the maze and not part of the 42."""
        return (0 <= x < self.cols and 0 <= y < self.rows
                and (x, y) not in self.pattern_cells)

    def neighbors(self, x: int, y: int) -> list[Cell]:
        """Adjacent cells you can walk to (no wall in between)."""
        result = []
        cell = self.maze[y][x]
        for dx, dy, wall, opposite in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if not self.is_open(nx, ny):
                continue
            if cell & wall or self.maze[ny][nx] & opposite:
                continue
            result.append((nx, ny))
        return result

    def reachable_from(self, start: Cell) -> set[Cell]:
        seen = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for nxt in self.neighbors(x, y):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen

    def nearest_open(self, x: int, y: int) -> Cell:
        """Closest cell to (x, y) that is not part of the 42."""
        seen = {(x, y)}
        queue = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) not in self.pattern_cells:
                return cx, cy
            for dx, dy, _, _ in DIRECTIONS:
                nxt = (cx + dx, cy + dy)
                if (0 <= nxt[0] < self.cols and 0 <= nxt[1] < self.rows
                        and nxt not in seen):
                    seen.add(nxt)
                    queue.append(nxt)
        return x, y

    # ---------- pacgums ----------

    @property
    def pacgums_left(self) -> int:
        return len(self.pacgums)

    @property
    def ghosts_edible(self) -> bool:
        return self.edible_time > 0

    def eat_at(self, x: int, y: int) -> Optional[str]:
        """Remove what is at (x, y). Returns 'pacgum', 'super' or None."""
        if (x, y) in self.pacgums:
            self.pacgums.remove((x, y))
            return "pacgum"
        if (x, y) in self.super_pacgums:
            self.super_pacgums.remove((x, y))
            self.edible_time = EDIBLE_DURATION
            return "super"
        return None

    # keep reset_timer() and respawn_entities() as they are
    
    def reset_timer(self) -> None:
            self.time_left = self.max_time
    
    def respawn_entities(self) -> None:
        """Put the player and ghosts back at their start. Keep the pacgums."""

    def update(self, dt: float, session: Session) -> Result:
        self.time_left -= dt
        self.edible_time = max(0.0, self.edible_time - dt)
        if self.pacgums_left == 0:
            return Result.LEVEL_COMPLETE
        if self.time_left <= 0:
            return Result.TIME_UP
        return Result.RUNNING
