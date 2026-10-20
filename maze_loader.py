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


class MazeLoader:
    def generate(self, level_cfg: dict[str, int],
                 seed: Optional[int]) -> list[list[int]]:
        try:
            # TODO: pass width/height/seed/PERFECT=False here.
            # I don't know this package's constructor, so check its README.
            generator = mazegenerator.MazeGenerator()
            grid = generator.maze
        except Exception as error:
            raise MazeError(f"maze generator failed: {error}") from error
        return validate(grid)