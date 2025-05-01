from enum import Enum, IntEnum


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
    Error = "RED"
