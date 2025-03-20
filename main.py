import os
from datetime import datetime
from time import time_ns

import pandas as pd
import pygame
from game import GameState, MainStatus
from pygame import display, event, init
from pygame.font import Font
from pygame.time import Clock
from keyboard import Keyboard  #importa la clase Keyboard desde el archivo keyboard.py

# Definimos algunos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

ESTIMULO_RADIO = 30
EYES_SIZE = 60  # Tamaño de los ojos


class App:
    def __init__(self, width=800, height=600, max_iterations=15):
        self._state = GameState((width, height), iterations_count=max_iterations)
        self.width = width
        self.height = height
        self._filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screen, self.font = None, None
        self.events = []
        self.clock = Clock()

        # Crea la instancia de la clase Keyboard
        self.keyboard = Keyboard("keyboard.jpg", "arrow.png", width=self.width, height=self.height)
        
        self.eye_image = pygame.image.load("eye.png") 
        self.eye_image = pygame.transform.scale(self.eye_image, (EYES_SIZE, EYES_SIZE))

    def log_event(self, e, value: int | float | str):
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
        save_dir = "./data"  # Usa raw string para evitar problemas con \

        # Crea el directorio si no existe
        os.makedirs(save_dir, exist_ok=True)

        # Guarda el archivo en formato parquet
        df = pd.DataFrame(self.events)
        file_path = os.path.join(save_dir, f"{self._filename}_keyboard.parquet")
        df.to_parquet(file_path, index=False)

    def close(self):
        print("Guardando eventos")
        self.save_events()  # Guarda eventos antes de cerrar pygame
        pygame.quit()
        exit()  # Asegura que el bucle se detenga completamente

    def eyes(self):
        mouse_x, mouse_y = pygame.mouse.get_pos() #posicion del cursor
        self.screen.blit(self.eye_image, (mouse_x - EYES_SIZE // 2, mouse_y - EYES_SIZE // 2))  # Centrado en el cursor
        return mouse_x, mouse_y

    def render(self):
        self.screen.fill(BLACK)
        if self._state.main_status == MainStatus.WaitingForInput:
            self._alert = self._state._current_message

        elif self._state.main_status == MainStatus.Playing:
            #Limites x,y en la pantalla
            x, y = self._state.stimuli_pos
            x = max(ESTIMULO_RADIO, min(self.width - ESTIMULO_RADIO, x))
            y = max(ESTIMULO_RADIO, min(self.height - ESTIMULO_RADIO, y))

            pygame.draw.circle(self.screen, self._state._stimuli_color.value, (x, y), ESTIMULO_RADIO)

            self.eyes() 

            time_remaining = max(0, int(self._state._time_remaining))
            timer_surface = self.font.render(f"Tiempo restante: {time_remaining}s", True, WHITE)
            #timer_rect = timer_surface.get_rect(center=(self.width // 2, 50))
            #self.screen.blit(timer_surface, timer_rect)
            timer_rect = timer_surface.get_rect(topright=(self.width - 10, 10))
            self.screen.blit(timer_surface, timer_rect)

            self._alert = self._state.current_message

        # Renderizamos el mensaje
        text_surface = self.font.render(self._alert, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)

        # Actualizar la visibilidad del teclado y renderizar
        self.keyboard.update_keyboard_visibility()
        self.keyboard.render(self.screen)

    def run(self):
        init()
        display.set_caption("EOG Game")
        self.screen = display.set_mode((self.width, self.height))
        self.font = Font(None, 36)

        #oculta la flecha del cursor para que solo se vean los ojo
        pygame.mouse.set_visible(False)

        while True:
            last_keypress = None
            for e in event.get():
                if e.type == pygame.QUIT:
                    self.close()
                elif e.type == pygame.KEYDOWN:
                    last_keypress = e.key
                    self.log_event(e, last_keypress)
                elif e.type == pygame.KEYUP:
                    self.log_event(e, last_keypress)

            self._state.main_logic(cursor_pos=pygame.mouse.get_pos(), keypressed=last_keypress)
            self._state.update_timer()

            self.render()
            display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()
    app.run()
