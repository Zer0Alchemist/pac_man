from typing import Any, Optional
import mazegenerator


class MazeError(Exception):
    """Raised when the maze cannot be generated or is invalid."""


def validate(grid: Any) -> list[list[int]]:
    """Check that grid is a non-empty rectangle of ints from 0 to 15."""
    if not isinstance(grid, list) or not grid:
        raise MazeError("maze is empty or not a list")
    width = len(grid[0])
    for row in grid:
        if not isinstance(row, list) or len(row) != width or width == 0:
            raise MazeError("maze rows are not all the same length")
        for value in row:
            if (isinstance(value, bool) or not isinstance(value, int)
                    or not 0 <= value <= 15):
                raise MazeError(f"invalid cell value: {value!r}")
    return grid


# class MazeLoader:
#     def generate(self, level_cfg: dict[str, int],
#                  seed: Optional[int]) -> list[list[int]]:
#         try:
#             # TODO: pass width/height/seed/PERFECT=False here.
#             # I don't know this package's constructor, so check its README.
#             generator = mazegenerator.MazeGenerator()
#             grid = generator.maze
#         except Exception as error:
#             raise MazeError(f"maze generator failed: {error}") from error
#         return validate(grid)

import random
from typing import Optional

import mazegenerator


import random
from typing import Optional

import mazegenerator


class MazeLoader:
    def generate(self, level_cfg: dict[str, int],
                 seed: Optional[int]) -> list[list[int]]:
        width = level_cfg["width"]
        height = level_cfg["height"]
        if seed is None:                        # levels after the first
            seed = random.randrange(2**31)
        try:
            generator = mazegenerator.MazeGenerator(
                size=(width, height),
                perfect=False,                  # required by the subject
                seed=seed,
            )
            grid = generator.maze
        except (Exception, SystemExit) as error:
            raise MazeError(f"maze generator failed: {error}") from error

        grid = validate(grid)
        if len(grid[0]) != width or len(grid) != height:
            print(f"Warning: asked for {width}x{height}, "
                  f"got {len(grid[0])}x{len(grid)}")
        return grid