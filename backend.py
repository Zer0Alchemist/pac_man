from collections import deque
from typing import Tuple, List
from levels import Level, NORTH, EAST, WEST, SOUTH


# ============= checks if next cell is valid ============
def valid_path(current: Tuple[int, int], next: Tuple[int, int],
               level: Level) -> bool:
    x, y = current

    if next in level.neighbors(x, y):
        return True
    return False


# ===== check if the next move is valid using valid path ======
def valid_move(current: Tuple[int, int], move: int,
               level: Level):
    x, y = current
    if move == NORTH:
        if valid_path(current, (x, y - 1), level):
            return (x, y - 1)
    if move == EAST:
        if valid_path(current, (x + 1, y), level):
            return (x + 1, y)
    if move == SOUTH:
        if valid_path(current, (x, y + 1), level):
            return (x, y + 1)
    if move == WEST:
        if valid_path(current, (x - 1, y), level):
            return (x - 1,)
    return current


# ========= bfs for ghosts (later use) ========
def path_to_player(start: Tuple[int, int], dest: Tuple[int, int],
                   level: Level) -> List[Tuple[int, int]]:
    visited = set()
    queue = deque([start])
    visited.add(start)
    parent = {start: None}

    while queue:
        curr = queue.popleft()

        if curr == dest:
            path = []
            while curr:
                path.append(curr)
                curr = parent[curr]

            return path[::-1]

        x, y = curr
        for neighbor in level.neighbors(x, y):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)

    return []


class TestLevel:
    def __init__(self):
        self.graph = {
            (0, 0): [(1, 0), (0, 1)],
            (1, 0): [(0, 0), (2, 0), (1, 1)],
            (2, 0): [(1, 0), (2, 1)],
            (0, 1): [(0, 0), (1, 1), (0, 2)],
            (1, 1): [(1, 0), (0, 1), (2, 1), (1, 2)],
            (2, 1): [(2, 0), (1, 1), (2, 2)],
            (0, 2): [(0, 1), (1, 2)],
            (1, 2): [(0, 2), (1, 1), (2, 2)],
            (2, 2): [(2, 1), (1, 2)],
        }

    def neighbors(self, x, y):
        return self.graph.get((x, y), [])


level = TestLevel()

print("Test 1:", valid_move((0, 0), NORTH, level))
print("Test 2:", valid_move((0, 0), EAST, level))
print("Test 3:", valid_move((0, 0), SOUTH, level))
print("Test 4:", valid_move((0, 0), WEST, level))
