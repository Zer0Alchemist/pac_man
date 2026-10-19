from screens import State , Screen
from game_screen import GameScreen
from Menu import MainMenu
import pygame


class App:
    WIDTH = 1400
    HEIGHT = 900

    def __init__(self) -> None:
        pygame.init()
        self.size = (self.WIDTH, self.HEIGHT)
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()

        self.screens: dict[State, Screen] = {
            State.MENU: MainMenu(self.size),
            # HIGHSCORES and INSTRUCTIONS screens get added here
        }
        self.state = State.MENU

    def change_state(self, new_state: State) -> None:
        if new_state == State.PLAYING:
            # always start a fresh game
            self.screens[State.PLAYING] = GameScreen(self.size)
        self.state = new_state

    def run(self) -> None:
        while self.state != State.EXIT:
            dt = self.clock.tick(60) / 1000.0
            screen = self.screens[self.state]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = State.EXIT
                    break
                next_state = screen.handle_event(event)
                if next_state is not None:
                    self.change_state(next_state)
                    break

            if self.state == State.EXIT:
                break

            screen = self.screens[self.state]   # may have changed above
            screen.update(dt)
            screen.draw(self.surface)
            pygame.display.flip()

        pygame.quit()