import math
import random
import time
from enum import Enum, IntEnum

import pygame


# Constantes
ALIGNMENT_THRESHOLD = 30  # In pixels
WAITING_FOR_ALIGMENT_THRESHOLD = 20  # In seconds
WAITING_FOR_KEYPRESS_THRESHOLD = 5  # In seconds
KEYPRESS_TIMEOUT = 3  # In seconds

GREEN_KEYS = {
    pygame.K_q, pygame.K_w, pygame.K_e,
    pygame.K_a, pygame.K_s, pygame.K_d,
    pygame.K_z, pygame.K_x, pygame.K_c,
}
BLUE_KEYS = {
    pygame.K_t, pygame.K_y, pygame.K_u,
    pygame.K_h, pygame.K_j, pygame.K_k,
    pygame.K_b, pygame.K_n, pygame.K_m,
}

class MainStatus(IntEnum):
    WaitingForInput = 0
    Playing = 1

class PlayingStatus(IntEnum):
    WaitingForAligment = 0
    WaitingForKeypress = 1
    KeyPress = 2

class StimuliColor(Enum):
    White = "WHITE"
    Green = "GREEN"
    Blue = "BLUE"
    Error = "red"

class GameState:
    def __init__(self, screen_size: tuple[int, int], iterations_count: int = 10):
        self._screen_size = screen_size
        self._current_message = "Presione espacio para comenzar"
        self._main_status = MainStatus.WaitingForInput
        self._playing_status = None

        self._iterations_count = iterations_count
        self._current_iteration = 0
        
        self._time_remaining = 20
        self._last_update_time = time.time()

        self._last_waiting_for_alignment_ts = None
        self._last_waiting_for_keypress_ts = None
        self._last_keypress_ts = None

        self._stimuli_pos = (0, 0)
        self._stimuli_color = StimuliColor.White
        self._cursor_pos = (0, 0)
        self._keep_pos = (0, 0)
        self._keep_iteration = 0
        

        self._errors_count = 0

    @property
    def main_status(self) -> MainStatus:
        return self._main_status

    @property
    def playing_status(self) -> PlayingStatus | None:
        return self._playing_status

    @property
    def current_message(self) -> str:
        return self._current_message

    @property
    def stimuli_pos(self) -> tuple[int, int]:
        return self._stimuli_pos

    @property
    def cursor_pos(self) -> tuple[int, int]:
        return self._cursor_pos

    @property
    def stimuli_color(self) -> StimuliColor:
        return self._stimuli_color

    def start_game(self):
        self._main_status = MainStatus.Playing
        self._current_message = ""
        self._current_iteration = 0
        self._errors_count = 0
        
        self.start_iteration()

    def start_iteration(self):
        self._playing_status = PlayingStatus.WaitingForAligment
        self._last_waiting_for_alignment_ts = time.time()
        self._stimuli_color = StimuliColor.White
        self._stimuli_pos = (
            random.randint(0, self._screen_size[0]),
            random.randint(0, self._screen_size[1]),
        )

    def next_iteration(self):
        self._current_iteration += 1
        if self._current_iteration < self._iterations_count:
            self.start_iteration()
            self._time_remaining = 20
            self._last_update_time = time.time()    
        else:
            self._main_status = MainStatus.WaitingForInput
            self._current_message = "Juego terminado. Presione espacio para reiniciar."
            
    @property
    def is_aligned(self) -> bool:
        stimuli_x, stimuli_y = self._stimuli_pos
        cursor_x, cursor_y = self._cursor_pos
        distance = math.sqrt((stimuli_x - cursor_x) ** 2 + (stimuli_y - cursor_y) ** 2)
       
        return distance <= ALIGNMENT_THRESHOLD

    def is_error(self, keypress: int) -> bool:
        if self._stimuli_color == StimuliColor.Green:
            
            return keypress not in GREEN_KEYS
        if self._stimuli_color == StimuliColor.Blue:
            return keypress not in BLUE_KEYS
        
        return False
    
    def update_timer(self):
        current_time = time.time()
        elapsed = current_time - self._last_update_time
        self._last_update_time = current_time  # Actualizar el último tiempo

        if self.main_status == MainStatus.Playing:
            self._time_remaining -= elapsed  # Restar tiempo transcurrido
            if self._time_remaining <= 0:  # Si el tiempo llega a 0, pasar a la siguiente iteración
                self.next_iteration()


    def main_logic(self, cursor_pos: tuple[int, int], keypressed: int | None = None):
        
        if self._main_status == MainStatus.WaitingForInput:
            if keypressed == pygame.K_SPACE:
                self.start_game()
            return

        self._cursor_pos = cursor_pos
        current_time = time.time()
        
        if self._playing_status == PlayingStatus.WaitingForAligment:
            time_elapsed = current_time - self._last_waiting_for_alignment_ts
            if time_elapsed > WAITING_FOR_ALIGMENT_THRESHOLD:
                self.next_iteration()
                
            elif self.is_aligned:
                self._playing_status = PlayingStatus.WaitingForKeypress
                self._last_waiting_for_keypress_ts = time.time()
                self._stimuli_color = random.choice([StimuliColor.Green, StimuliColor.Blue])

        elif self._playing_status == PlayingStatus.WaitingForKeypress:
            if not self.is_aligned:
                self._playing_status = PlayingStatus.WaitingForAligment
            else:
                if keypressed is not None:
                    if self.is_error(keypressed):
                        self._current_message = "Prueba otra vez"
                        self._stimuli_color = StimuliColor.Error
                        self._errors_count += 1

                    else:
                       
                        self._current_message = " "
                        self._playing_status = PlayingStatus.KeyPress
                        self._last_keypress_ts = time.time()
    
                time_elapsed = current_time - self._last_waiting_for_keypress_ts
              
                if time_elapsed > WAITING_FOR_KEYPRESS_THRESHOLD or self._errors_count > 3:
                    self.next_iteration()
                

        elif self._playing_status == PlayingStatus.KeyPress:
            time_elapsed = current_time - self._last_keypress_ts
            if time_elapsed > KEYPRESS_TIMEOUT:
                self.next_iteration()