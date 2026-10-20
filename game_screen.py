from screens import Screen , State
import pygame
from typing import Optional
from levels import Session , Level , Result


from levels import CLOSED, EAST, NORTH, SOUTH, WEST, Level, Result, Session


BG_COLOR = (0, 0, 0)
WALL_OUTER = (30, 50, 210)        # outer blue line
WALL_INNER = (90, 150, 255)       # lighter inner line
PATTERN_FILL = (10, 10, 70)       # inside of the 42
PATTERN_COLOR = (255, 184, 222)   # pink, like the ghost-house gate
PACGUM_COLOR = (255, 184, 174)    # peach, for later
TEXT_WHITE = (255, 255, 255)
PAC_YELLOW = (255, 255, 0)
ALERT_RED = (255, 40, 40)
MARGIN = 10

Edge = tuple[str, int, int]


def collect_edges(level: Level) -> tuple[set[Edge], set[Edge]]:
    """Return (normal wall edges, outline edges of the 42)."""
    walls: set[Edge] = set()
    outline: set[Edge] = set()
    pattern = level.pattern_cells

    for y, row in enumerate(level.maze):
        for x, value in enumerate(row):
            if (x, y) in pattern:
                # only the border of the 42 is drawn, not the inside
                if (x, y - 1) not in pattern:
                    outline.add(("h", x, y))
                if (x, y + 1) not in pattern:
                    outline.add(("h", x, y + 1))
                if (x - 1, y) not in pattern:
                    outline.add(("v", x, y))
                if (x + 1, y) not in pattern:
                    outline.add(("v", x + 1, y))
                continue
            if value & NORTH:
                walls.add(("h", x, y))
            if value & SOUTH:
                walls.add(("h", x, y + 1))
            if value & WEST:
                walls.add(("v", x, y))
            if value & EAST:
                walls.add(("v", x + 1, y))

    # walls touching the 42 are already drawn as part of its outline
    return walls - outline, outline


def edge_rect(edge: Edge, cw: int, ch: int, pad: int,
              thickness: int) -> pygame.Rect:
    """Rectangle centered on the edge, with the given thickness."""
    kind, x, y = edge
    px, py = pad + x * cw, pad + y * ch
    half = thickness // 2
    if kind == "h":
        return pygame.Rect(px - half, py - half, cw + thickness, thickness)
    return pygame.Rect(px - half, py - half, thickness, ch + thickness)
class GameScreen(Screen):
    HUD_TOP = 70
    HUD_BOTTOM = 56

    def __init__(self, size: tuple[int, int], config : dict , maze_loader) -> None:
        self.size = size
        self.config = config
        self.maze_loader = maze_loader
        self.session = Session(lives=config["lives"])
        self.paused = False
        self.label_font = pygame.font.SysFont("monospace", 22, bold=True)
        self.value_font = pygame.font.SysFont("monospace", 28, bold=True)
        self.high_score = 0        # later: best score from the highscore file
        self.level = self.build_level()

    def maze_area(self) -> pygame.Rect:
        """Free rectangle between the top and bottom HUD bars."""
        width, height = self.size
        return pygame.Rect(MARGIN, self.HUD_TOP + MARGIN,
                        width - 2 * MARGIN,
                        height - self.HUD_TOP - self.HUD_BOTTOM - 2 * MARGIN)
    # ---------- level flow ----------

    def build_level(self) -> Level:
        index = self.session.level_index
        seed = self.config["seed"] if index == 0 else None
        grid = self.maze_loader.generate(self.config["level"][index], seed)
        level = Level(grid, self.config["level_max_time"])
        self.maze_surface = self.render_maze(level)
        return level

    def advance_level(self) -> Optional[State]:
        self.session.level_index += 1
        if self.session.level_index >= len(self.config["level"]):
            return State.VICTORY
        self.level = self.build_level()
        return None

    def lose_life(self, time_up: bool = False) -> Optional[State]:
        self.session.lives -= 1
        if self.session.lives <= 0:
            return State.GAME_OVER
        self.level.respawn_entities()
        if time_up:
            self.level.reset_timer()
        return None

    # ---------- Screen interface ----------

    def handle_event(self, event: pygame.event.Event) -> Optional[State]:
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_ESCAPE:
            return State.MENU              # later: open the pause menu
        if event.key == pygame.K_p:
            self.paused = not self.paused
        # temporary debug keys, to test the flow before the engine exists
        elif event.key == pygame.K_n:
            return self.advance_level()
        elif event.key == pygame.K_l:
            return self.lose_life()
        return None

    def update(self, dt: float) -> Optional[State]:
        if self.paused:
            return None
        result = self.level.update(dt, self.session)
        if result == Result.LEVEL_COMPLETE:
            return self.advance_level()
        if result == Result.LIFE_LOST:
            return self.lose_life()
        if result == Result.TIME_UP:
            return self.lose_life(time_up=True)
        return None

    MARGIN = 10      # smaller margin, covers more of the screen

    def render_maze(self, level: Level) -> pygame.Surface:
        width, height = self.size
        cw = max(8, (width - 2 * MARGIN) // level.cols)
        ch = max(
            8,
            (height - self.HUD_TOP - self.HUD_BOTTOM - 2 * MARGIN)
            // level.rows
        )
        t = max(4, min(cw, ch) // 5 // 2 * 2)   # wall thickness (even number)
        o = max(1, t // 5)
        pad = t // 2 + 1

        # kept for later: entities will use these
        area = self.maze_area()
        cw = max(8, area.width // level.cols)
        ch = max(8, area.height // level.rows)

        self.maze_pad = pad
        self.origin = (area.x + (area.width - cw * level.cols) // 2,
               area.y + (area.height - ch * level.rows) // 2)

        surf = pygame.Surface((cw * level.cols + 2 * pad,
                            ch * level.rows + 2 * pad))
        surf.fill(BG_COLOR)
        walls, outline = collect_edges(level)

        t = max(6, min(cw, ch) // 5 // 2 * 2)     # use `cell` in the square version
        o = max(1, t // 6)
        rects = [edge_rect(edge, cw, ch, pad, t) for edge in walls]

        for rect in rects:                         # 1) outer dark blue
            pygame.draw.rect(surf, WALL_OUTER, rect, border_radius=t // 2)
        for rect in rects:                         # 2) lighter inner line
            pygame.draw.rect(surf, WALL_INNER, rect.inflate(-2 * o, -2 * o),
                            border_radius=max(1, t // 2 - o))
        for rect in rects:                         # 3) black core
            pygame.draw.rect(surf, BG_COLOR, rect.inflate(-4 * o, -4 * o),
                            border_radius=max(1, t // 2 - 2 * o))

        for x, y in level.pattern_cells:
            surf.fill(PATTERN_FILL, (pad + x * cw, pad + y * ch, cw, ch))
        line = max(2, t // 3 // 2 * 2)
        for edge in outline:
            surf.fill(PATTERN_COLOR, edge_rect(edge, cw, ch, pad, line))
        return surf
    
    def draw_stat(self, surface: pygame.Surface, label: str, value: str,
                  center_x: int, value_color=TEXT_WHITE) -> None:
            """A label with its value under it, both centered on center_x."""
            label_img = self.label_font.render(label, True, TEXT_WHITE)
            value_img = self.value_font.render(value, True, value_color)
            surface.blit(label_img, label_img.get_rect(midtop=(center_x, 6)))
            surface.blit(value_img, value_img.get_rect(midtop=(center_x, 32)))
    
    def draw_life_icon(self, surface: pygame.Surface,
                    center: tuple[int, int], radius: int) -> None:
        """Small Pac-Man facing right: a yellow disc with a mouth wedge."""
        cx, cy = center
        pygame.draw.circle(surface, PAC_YELLOW, center, radius)
        mouth = [center,
                (cx + radius + 1, cy - int(radius * 0.7)),
                (cx + radius + 1, cy + int(radius * 0.7))]
        pygame.draw.polygon(surface, BG_COLOR, mouth)

    def draw_hud(self, surface: pygame.Surface) -> None:
        s = self.session
        width, height = self.size
        total_levels = len(self.config["level"])
        seconds = int(max(0, self.level.time_left))
        time_color = ALERT_RED if seconds <= 10 else TEXT_WHITE

        # top bar
        self.draw_stat(surface, "1UP", str(s.score), width // 6)
        self.draw_stat(surface, "HIGH SCORE",
                    str(max(self.high_score, s.score)), width // 2)
        self.draw_stat(surface, "TIME", str(seconds), width * 5 // 6,
                    time_color)

        # bottom bar: lives on the left, level on the right
        y = height - self.HUD_BOTTOM // 2
        radius = self.HUD_BOTTOM // 3
        if s.lives <= 6:
            for i in range(s.lives):
                self.draw_life_icon(surface, (30 + radius + i * (2 * radius + 10), y), radius)
        else:                                   # cheat mode can give many lives
            self.draw_life_icon(surface, (30 + radius, y), radius)
            text = self.value_font.render(f"x{s.lives}", True, TEXT_WHITE)
            surface.blit(text, text.get_rect(midleft=(30 + 2 * radius + 10, y)))

        level_text = self.value_font.render(
            f"LEVEL {s.level_index + 1}/{total_levels}", True, TEXT_WHITE)
        surface.blit(level_text, level_text.get_rect(midright=(width - 30, y)))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        surface.blit(self.maze_surface,
                    (self.origin[0] - self.maze_pad,
                    self.origin[1] - self.maze_pad))
        self.draw_hud(surface)

    
