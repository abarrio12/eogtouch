from datetime import datetime

import pygame
from pygame import display, event, init
from pygame.font import Font
from pygame.time import Clock

from eogtouch.gui import config
from eogtouch.models import GameState, MainStatus
from eogtouch.storage import DataSinker

from .imgs import img_path
from .keyboard import Keyboard


class App:
    def __init__(self, width=800, height=600, max_iterations=15):
        self._state = GameState((width, height), iterations_count=max_iterations)
        self.width = width
        self.height = height
        self.screen, self.font = None, None
        self.sinker: DataSinker | None = None
        self.clock = Clock()

        self.eye_image = pygame.image.load(img_path("eye.png"))
        self.eye_image = pygame.transform.scale(self.eye_image, (config.eyes_size, config.eyes_size))

        self.keyboard = Keyboard()


    def close(self):
        filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.sinker.save(filename)
        pygame.quit()
        exit()

    def eyes(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.screen.blit(self.eye_image, (mouse_x - config.eyes_size // 2, mouse_y - config.eyes_size // 2))
        return mouse_x, mouse_y

    def render(self):
        if self._state.main_status == MainStatus.WaitingForInput:
            self.keyboard.render_intro(self.screen, self.width, self.height)
            return

        self.screen.fill(config.BLACK)

        if self._state.main_status == MainStatus.Playing:
            x, y = self._state.stimuli_pos
            x = max(config.stimulus_radio, min(self.width - config.stimulus_radio, x))
            y = max(config.stimulus_radio, min(self.height - config.stimulus_radio, y))
            pygame.draw.circle(self.screen, self._state.stimuli_color.value, (x, y), config.stimulus_radio)
            self.eyes()

            # Dibujando el temporizador
            time_remaining = max(0, int(self._state._time_remaining))
            timer_surface = self.font.render(f"Tiempo restante: {time_remaining}s", True, config.WHITE)
            self.screen.blit(timer_surface, timer_surface.get_rect(topright=(self.width - 10, 10)))

            # Estilo mensaje feedback
            alert = self._state.current_message
            text_surface = self.font.render(alert, True, config.WHITE)
            self.screen.blit(text_surface, text_surface.get_rect(center=(self.width // 2, self.height // 2)))

    def run(self):
        self.sinker = DataSinker()

        init()
        display.set_caption("EOG Game")
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h
        self.screen = display.set_mode((self.width, self.height))
        self.font = Font(None, 36)
        pygame.mouse.set_visible(False)  # Ocultar el cursor del raton

        key_sample = 0

        while True:
            last_keypress = None
            for e in event.get():
                if e.type == pygame.QUIT:
                    self.close()

                elif e.type == pygame.KEYDOWN:
                    # Salir con Ctrl + Q
                    if e.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.close()
                    last_keypress = e.key
                    key_sample = e.key

                elif e.type == pygame.KEYUP:
                    last_keypress = e.key
                    key_sample = 0

            self._state.main_logic(cursor_pos=pygame.mouse.get_pos(), keypressed=last_keypress)
            self._state.update_timer()
            self.render()
            display.flip()

            # Log data to sinker
            stimuli_x, stimuli_y = self._state.stimuli_pos
            eyes_x, eyes_y = self.eyes()
            self.sinker.add_sample(
                stimuli_x=stimuli_x,
                stimuli_y=stimuli_y,
                stimuli_color=self._state.stimuli_color,
                eyes_x=eyes_x,
                eyes_y=eyes_y,
                key=key_sample,
            )

            self.clock.tick(60)

            if self._state.main_status == MainStatus.Finished:
                self.close()
                break
