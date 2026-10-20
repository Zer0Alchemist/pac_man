from screens import State , Screen
from game_screen import GameScreen
from Menu import MainMenu
from maze_loader import MazeError
import pygame
from maze_loader import MazeLoader

class App:
    WIDTH = 1400
    HEIGHT = 900

    def __init__(self , config) -> None:
        pygame.init()
        self.size = (self.WIDTH, self.HEIGHT)
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pac-Man Sboo3a")
        self.clock = pygame.time.Clock()
        self.config = config
        self.maze_loader = MazeLoader()
        self.screens: dict[State, Screen] = {
            State.MENU: MainMenu(self.size),
            # HIGHSCORES and INSTRUCTIONS screens get added here
        }
        self.state = State.MENU

    
    def change_state(self, new_state: State) -> None:
        if new_state == State.PLAYING:
            try:
                self.game = GameScreen(self.size, self.config, self.maze_loader)
            except MazeError as error:
                print(f"Cannot start the game: {error}")
                return                          # stays on the menu
            self.screens[State.PLAYING] = self.game
        elif new_state in (State.GAME_OVER, State.VICTORY):
            new_state = State.MENU

        if new_state not in self.screens and new_state != State.EXIT:
            print(f"Screen for {new_state.name} not implemented yet")
            return

        self.state = new_state                  # easy to forget

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