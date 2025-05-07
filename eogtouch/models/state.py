import math
import random
import time

import pygame

from eogtouch.models import config

from .enums import MainStatus, PlayingStatus, StimuliColor


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
        self._waiting_time = 2
        self._last_iteration_ts = time.time()
        self._message_display_ts = None  # saved time when message was displayed
        self._message_display_time = 2  # min time to show message in seconds
        self._alignment_color = None

        self._last_waiting_for_alignment_ts = None
        self._last_waiting_for_keypress_ts = None
        self._last_keypress_ts = None

        self._stimuli_pos = (0, 0)
        self._stimuli_color = StimuliColor.White

        self._min_distance_new_stimuli = 500  # min distance between stimuli
        self._previous_stimuli_pos = None
        self._cursor_pos = (0, 0)
        self._pos_before_error = (0, 0)
        self._color_before_error = StimuliColor.White  # save color before error to restore it later

        self._error_display_start_ts = None
        self._errors_count = 0
        self._error = False

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
        self._current_message = " "
        self._playing_status = PlayingStatus.WaitingForAligment
        self._last_waiting_for_alignment_ts = time.time()
        self._alignment_color = random.choice([StimuliColor.Green, StimuliColor.Blue])
        self._stimuli_color = StimuliColor.White
        while True:
            new_pos = (
                random.randint(0, self._screen_size[0]),
                random.randint(0, self._screen_size[1]),
            )
            if self._previous_stimuli_pos is None:
                break
            distance = math.dist(new_pos, self._previous_stimuli_pos)
            if distance >= self._min_distance_new_stimuli:
                break

        self._stimuli_pos = new_pos
        self._previous_stimuli_pos = new_pos  # saves new position for comparison in next iteration
        self._errors_count = 0

    def next_iteration(self):
        current_time = time.time()

        self._message_display_ts = None
        self._error_display_start_ts = None
        self._current_message = ""
        self._errors_count = 0

        if self._message_display_ts:
            time_elapsed_since_message = current_time - self._message_display_ts
            if time_elapsed_since_message < self._message_display_time:
                return  # if not enough time has passed, do not continue
        self._current_iteration += 1
        if self._current_iteration < self._iterations_count:
            self.start_iteration()
            self._time_remaining = 20
            self._last_update_time = time.time()
            self._last_iteration_ts = current_time
            self._message_display_ts = None  # clean message display time before next iteration
        else:
            self._main_status = MainStatus.Finished
            self._current_message = "Juego terminado. Presione espacio para reiniciar."

    def show_message(self, message: str):
        self._current_message = message
        self._message_display_ts = time.time()

    def is_aligned(self) -> bool:
        stimuli_x, stimuli_y = self._stimuli_pos
        cursor_x, cursor_y = self._cursor_pos
        distance = math.sqrt((stimuli_x - cursor_x) ** 2 + (stimuli_y - cursor_y) ** 2)

        return distance <= config.alignment_threshold

    def is_error(self, keypress: int) -> bool:
        if self._stimuli_color == StimuliColor.Green:
            return keypress not in config.GREEN_KEYS
        if self._stimuli_color == StimuliColor.Blue:
            return keypress not in config.BLUE_KEYS

        return True

    def update_timer(self):
        current_time = time.time()
        elapsed = current_time - self._last_update_time
        self._last_update_time = current_time

        if self.main_status == MainStatus.Playing:
            self._time_remaining -= elapsed
            if self._time_remaining <= 0:
                self.next_iteration()

    def handle_error(self):
        self._errors_count += 1
        self._color_before_error = self._stimuli_color
        self._pos_before_error = self._stimuli_pos
        self._stimuli_color = StimuliColor.Error
        self.show_message("Error! Prueba otra vez")
        self._error_display_start_ts = time.time()
        if self._errors_count == 3:
            self.show_message("No has logrado presionar la tecla correcta")

    def main_logic(self, cursor_pos: tuple[int, int], keypressed: int | None = None):
        if self._main_status == MainStatus.WaitingForInput:
            if keypressed == pygame.K_SPACE:
                self.start_game()
            return

        self._cursor_pos = cursor_pos
        current_time = time.time()

        if self._playing_status == PlayingStatus.WaitingForAligment:
            time_elapsed = current_time - self._last_waiting_for_alignment_ts
            if time_elapsed > config.waiting_for_alignment_threshold:
                self.next_iteration()

            elif self.is_aligned():
                self._playing_status = PlayingStatus.WaitingForKeypress
                self._last_waiting_for_keypress_ts = time.time()
                self._stimuli_color = self._alignment_color

        elif self._playing_status == PlayingStatus.WaitingForKeypress:
            if self._error_display_start_ts is not None:
                error_time = current_time - self._error_display_start_ts
                if error_time >= config.error_display_time:
                    if self.is_aligned():
                        self._stimuli_color = self._alignment_color
                    else:
                        self._stimuli_color = StimuliColor.White

                    self._last_waiting_for_keypress_ts = current_time
                    self._error_display_start_ts = None
                    self._current_message = ""
                    self._message_display_ts = None

                    if self._errors_count == 3:
                        self.next_iteration()

            elif not self.is_aligned():
                self._playing_status = PlayingStatus.WaitingForAligment
                self._stimuli_color = StimuliColor.White
            else:
                if keypressed is not None:
                    if self.is_error(keypressed):
                        self.handle_error()
                    else:
                        self.show_message(f"Bien hecho! Has presionado: {pygame.key.name(keypressed)}")
                        self.next_iteration()
                else:
                    time_elapsed = current_time - self._last_waiting_for_keypress_ts
                    if time_elapsed > config.waiting_for_keypress_threshold:
                        self.next_iteration()
