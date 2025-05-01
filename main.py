import os
from datetime import datetime
from time import time_ns

import pandas as pd
import pygame
from game import GameState, MainStatus
from pygame import display, event, init
from pygame.font import Font
from pygame.time import Clock
from keyboard import Keyboard

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ESTIMULO_RADIO = 30
EYES_SIZE = 60

class App:
    def __init__(self, width=800, height=600, max_iterations=15):
        self._state = GameState((width, height), iterations_count=max_iterations)
        self.width = width
        self.height = height
        self._filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screen, self.font = None, None
        self.events = []
        self.clock = Clock()
        
        self.eye_image = pygame.image.load("eye.png")
        self.eye_image = pygame.transform.scale(self.eye_image, (EYES_SIZE, EYES_SIZE))

        self.keyboard = Keyboard()  
        

    def log_event(self, e, value):
        key_name = pygame.key.name(e.key)
        ts = time_ns()
        event_type = "press" if e.type == pygame.KEYDOWN else "release"
        self.events.append({
            "timestamp": ts,
            "event": event_type,
            "color": self._state.stimuli_color.value,
            "key": key_name,
            "value": value,
            "error": self._state._errors_count,
            "iteracion": self._state._current_iteration,
        })

    def save_events(self):
        os.makedirs("./data", exist_ok=True)
        df = pd.DataFrame(self.events)
        df.to_parquet(f"./data/{self._filename}_keyboard.parquet", index=False)

    def close(self):
        print("Guardando eventos")
        self.save_events()
        pygame.quit()
        exit()
    
    def eyes(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.screen.blit(self.eye_image, (mouse_x - EYES_SIZE // 2, mouse_y - EYES_SIZE // 2))
        return mouse_x, mouse_y


    def render(self):
        if self._state.main_status == MainStatus.WaitingForInput:
            self.keyboard.render_intro(self.screen, self.width, self.height)
            return

        self.screen.fill(BLACK)

        if self._state.main_status == MainStatus.Playing:
            x, y = self._state.stimuli_pos
            x = max(ESTIMULO_RADIO, min(self.width - ESTIMULO_RADIO, x))
            y = max(ESTIMULO_RADIO, min(self.height - ESTIMULO_RADIO, y))
            pygame.draw.circle(self.screen, self._state.stimuli_color.value, (x, y), ESTIMULO_RADIO)
            self.eyes()
            
            # Dibujando el temporizador
            time_remaining = max(0, int(self._state._time_remaining))
            timer_surface = self.font.render(f"Tiempo restante: {time_remaining}s", True, WHITE)
            self.screen.blit(timer_surface, timer_surface.get_rect(topright=(self.width - 10, 10)))

            # Estilo mensaje feedback
            alert = self._state.current_message
            text_surface = self.font.render(alert, True, WHITE)
            self.screen.blit(text_surface, text_surface.get_rect(center=(self.width // 2, self.height // 2)))

         

    def run(self):
        init()
        display.set_caption("EOG Game")
        self.screen = display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h
        self.font = Font(None, 36)
        pygame.mouse.set_visible(False)  # Ocultar el cursor del raton

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
                    self.log_event(e, last_keypress)

                elif e.type == pygame.KEYUP:
                    self.log_event(e, last_keypress)

            self._state.main_logic(cursor_pos=pygame.mouse.get_pos(), keypressed=last_keypress)
            self._state.update_timer()
            self.render()
            display.flip()
            self.clock.tick(60)  # Limitar a 60 FPS

if __name__ == "__main__":
    app = App()
    app.run()
