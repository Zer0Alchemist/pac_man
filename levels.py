from dataclasses import dataclass
from enum import Enum, auto
from back_end_logic import Player, Ghost
import mazegenerator
from back_end_logic import Direction, PLAYER_SPEED
from backend import valid_move, path_to_player


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
        self.corners = [
                    self.nearest_open(x, y)
                    for x, y in ((0, 0), (self.cols - 1, 0),
                                 (0, self.rows - 1),
                                 (self.cols - 1, self.rows - 1))
                ]
        self.start = self.nearest_open(self.cols // 2, self.rows // 2)
        self.player = Player(self.start)
        self.blinky = Ghost("blinky", self.corners[1])
        self.pinky = Ghost("pinky", self.corners[0])

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
        if self.player.target is None:
            if self.player.wanted == Direction.UP:
                next_cell = valid_move(self.player.cell, Direction.UP, self)

                if next_cell != self.player.cell:
                    self.player.target = next_cell
                    self.player.facing = "up"
            elif self.player.wanted == Direction.RIGHT:
                next_cell = valid_move(self.player.cell, Direction.RIGHT, self)

                if next_cell != self.player.cell:
                    self.player.target = next_cell
                    self.player.facing = "right"
            elif self.player.wanted == Direction.DOWN:
                next_cell = valid_move(self.player.cell, Direction.DOWN, self)

                if next_cell != self.player.cell:
                    self.player.target = next_cell
                    self.player.facing = "down"
            elif self.player.wanted == Direction.LEFT:
                next_cell = valid_move(self.player.cell, Direction.LEFT, self)

                if next_cell != self.player.cell:
                    self.player.target = next_cell
                    self.player.facing = "left"

        if self.player.target is not None:
            self.player.progress += self.player.speed * dt

            if self.player.progress >= 1.0:
                self.player.cell = self.player.target
                self.player.target = None
                self.player.progress = 0.0

        if self.blinky.target is None:
            next_cell = path_to_player(self.blinky.cell, self.player.cell,
                                       self)
            if len(next_cell) > 1:
                self.blinky.target = next_cell[1]

        if self.blinky.target is not None:
            self.blinky.progress += self.blinky.speed * dt

            if self.blinky.progress >= 1.0:
                self.blinky.cell = self.blinky.target
                self.blinky.target = None
                self.blinky.progress = 0.0

        if self.pinky.target is None:
            p_x, p_y = self.player.cell
            if self.player.facing == "up":
                next_cell = next_cell = path_to_player(self.pinky.cell,
                                                       (p_x, p_y - 3), self)
                if not next_cell:
                    next_cell = path_to_player(self.pinky.cell,
                                               (p_x, p_y - 2), self)
                    if not next_cell:
                        next_cell = path_to_player(self.pinky.cell,
                                                   (p_x, p_y - 1), self)
                        if not next_cell:
                            next_cell = path_to_player(self.pinky.cell,
                                                       (p_x, p_y), self)
                if len(next_cell) > 1:
                    self.pinky.target = next_cell[1]
            if self.player.facing == "right":
                next_cell = next_cell = path_to_player(self.pinky.cell,
                                                       (p_x + 3, p_y), self)
                if not next_cell:
                    next_cell = path_to_player(self.pinky.cell,
                                               (p_x + 2, p_y), self)
                    if not next_cell:
                        next_cell = path_to_player(self.pinky.cell,
                                                   (p_x + 1, p_y), self)
                        if not next_cell:
                            next_cell = path_to_player(self.pinky.cell,
                                                       (p_x, p_y), self)
                if len(next_cell) > 1:
                    self.pinky.target = next_cell[1]
            if self.player.facing == "down":
                next_cell = next_cell = path_to_player(self.pinky.cell,
                                                       (p_x, p_y + 3), self)
                if not next_cell:
                    next_cell = path_to_player(self.pinky.cell,
                                               (p_x, p_y + 2), self)
                    if not next_cell:
                        next_cell = path_to_player(self.pinky.cell,
                                                   (p_x, p_y + 1), self)
                        if not next_cell:
                            next_cell = path_to_player(self.pinky.cell,
                                                       (p_x, p_y), self)
                if len(next_cell) > 1:
                    self.pinky.target = next_cell[1]
            if self.player.facing == "left":
                next_cell = next_cell = path_to_player(self.pinky.cell,
                                                       (p_x - 3, p_y), self)
                if not next_cell:
                    next_cell = path_to_player(self.pinky.cell,
                                               (p_x - 2, p_y), self)
                    if not next_cell:
                        next_cell = path_to_player(self.pinky.cell,
                                                   (p_x - 1, p_y), self)
                        if not next_cell:
                            next_cell = path_to_player(self.pinky.cell,
                                                       (p_x, p_y), self)
                if len(next_cell) > 1:
                    self.pinky.target = next_cell[1]

        if self.pinky.target is not None:
            self.pinky.progress += self.pinky.speed * dt

            if self.pinky.progress >= 1.0:
                self.pinky.cell = self.pinky.target
                self.pinky.target = None
                self.pinky.progress = 0.0

        self.time_left -= dt
        self.edible_time = max(0.0, self.edible_time - dt)
        if self.pacgums_left == 0:
            return Result.LEVEL_COMPLETE
        if self.time_left <= 0:
            return Result.TIME_UP
        return Result.RUNNING