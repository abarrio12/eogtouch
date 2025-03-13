from pygame.time import Clock
from pygame import display, event, init, quit
from pygame.font import Font
from pygame.surface import Surface
from datetime import datetime
from time import time_ns
from game import GameState, MainStatus
import pygame
import pygame.event as Event
import pandas as pd



# Definimos algunos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

CM_TO_PIXELS = 6 * (96 / 2.54)
ESTIMULO_RADIO = 30 
EYES_RADIO = 10

class App:
    def __init__(self, width=800, height=600, max_iterations=15):
        self._state = GameState((width, height), iterations_count=max_iterations)
        self.width = width
        self.height = height
        self._filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screen, self.font = None, None
        self._events_file, self.space_pressed = None, False
        self.clock = Clock()
        

    def init_events_file(self):
        self._events_file = open(f"./data/{self._filename}_keyboard.csv", "wt")
        self._events_file.write("timestamp;event;value\n")
        
    def log_event(self, event: Event, value: int | float | str):
        ts = time_ns()
        #self._events_file.write(f"{ts};{event.value};{value}\n")
        self._events_file.write(f"{ts};{event.type};{value}\n")
   
    def close(self):
        if self._events_file:
            self._events_file.close()
            csv_path = f"./data/{self._filename}_keyboard.csv"
            parquet_path = f"./data/{self._filename}_keyboard.parquet"

            df = pd.read_csv(csv_path, sep=";")  # Cargamos el CSV
            df.to_parquet(parquet_path, engine="pyarrow", index=False)
        quit()
        exit()

    def eyes(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, RED, (mouse_x, mouse_y), EYES_RADIO)
        return mouse_x, mouse_y

    def render(self):
        self.screen.fill(BLACK)
        if self._state.main_status == MainStatus.WaitingForInput:
            self._alert = self._state._current_message
     
        if self._state.main_status == MainStatus.Playing: #me ha cambiado el color y tengo que pintar 
            
            pygame.draw.circle(self.screen, self._state.stimuli_color.value, self._state.stimuli_pos, ESTIMULO_RADIO)
            self.eyes()
            self._alert = " "
            
            time_remaining = max(0, int(self._state._time_remaining))  # Evita valores negativos
            timer_surface = self.font.render(f"Tiempo restante: {time_remaining}s", True, WHITE)
            timer_rect = timer_surface.get_rect(center=(self.width // 2, 50))  # Posición arriba centrada
            self.screen.blit(timer_surface, timer_rect)
           
        
        text_surface = self.font.render(self._alert, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)    

    def run(self):
        init()
        display.set_caption("EOG Game")
        self.screen = display.set_mode((self.width, self.height))
        self.font = Font(None, 36)

        self.init_events_file()
        
        while True:
            last_keypress = None
            for e in event.get():
                if e.type == pygame.QUIT:
                    self.close()
                elif e.type == pygame.KEYDOWN:
                    last_keypress = pygame.key.name(e.key)
                    self.log_event(e, last_keypress) 

            self._state.main_logic(cursor_pos= pygame.mouse.get_pos(), keypressed=last_keypress)
            self._state.update_timer()
                
            self.render()
            display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    app = App()
    app.run()