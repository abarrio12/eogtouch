from datetime import datetime
from time import time_ns

import pandas as pd
import pygame
from pygame import display, event, init, quit
from pygame.font import Font
from pygame.time import Clock

from game import GameState, MainStatus

# Definimos algunos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

ESTIMULO_RADIO = 30
EYES_RADIO = 10


class App:
    def __init__(self, width=800, height=600, max_iterations=15):
        self._state = GameState((width, height), iterations_count=max_iterations)
        self.width = width
        self.height = height
        self._filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screen, self.font = None, None
        self.events = []
        self.clock = Clock()

    def log_event(self, e, value: int | float | str):
        key_name = pygame.key.name(e.key)
        ts = time_ns()
        event_type = "press" if e.type == pygame.KEYDOWN else "release"
        self.events.append(
            {"timestamp": ts, "event": event_type, "key": key_name, "value": value}
        )

    def save_events(self):
        df = pd.DataFrame(self.events)
        df.to_parquet(f"./data/{self._filename}_keyboard.parquet", index=False)

    def close(self):
        self.save_events()
        print("Guardando eventos")
        quit()

    def eyes(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, RED, (mouse_x, mouse_y), EYES_RADIO)
        return mouse_x, mouse_y

    def render(self):
        self.screen.fill(BLACK)
        if self._state.main_status == MainStatus.WaitingForInput:
            self._alert = self._state._current_message

        if self._state.main_status == MainStatus.Playing:
            pygame.draw.circle(
                self.screen,
                self._state.stimuli_color.value,
                self._state.stimuli_pos,
                ESTIMULO_RADIO,
            )
            self.eyes()
            self._alert = " "

            time_remaining = max(0, int(self._state._time_remaining))
            timer_surface = self.font.render(
                f"Tiempo restante: {time_remaining}s", True, WHITE
            )
            timer_rect = timer_surface.get_rect(center=(self.width // 2, 50))
            self.screen.blit(timer_surface, timer_rect)

        text_surface = self.font.render(self._alert, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        init()
        display.set_caption("EOG Game")
        self.screen = display.set_mode((self.width, self.height))
        self.font = Font(None, 36)

        while True:
            last_keypress = None
            for e in event.get():
                if e.type == pygame.QUIT:
                    self.close()
                elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                    last_keypress = e.key
                    self.log_event(e, last_keypress)

            self._state.main_logic(
                cursor_pos=pygame.mouse.get_pos(), keypressed=last_keypress
            )
            self._state.update_timer()

            self.render()
            display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()
    app.run()
