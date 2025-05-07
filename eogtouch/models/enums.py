from enum import Enum, IntEnum


class MainStatus(IntEnum):
    WaitingForInput = 0
    Playing = 1
    Finished = 2


class PlayingStatus(IntEnum):
    WaitingForAligment = 0
    WaitingForKeypress = 1
    KeyPress = 2


class StimuliColor(Enum):
    White = "WHITE"
    Green = "GREEN"
    Blue = "BLUE"
    Error = "RED"

    @property
    def int_value(self) -> int:
        return {
            StimuliColor.White: 0x00FFFFFF,
            StimuliColor.Error: 0x00FF0000,
            StimuliColor.Green: 0x0000FF00,
            StimuliColor.Blue: 0x000000FF,
        }[self]

    @classmethod
    def from_int_value(cls, value: int) -> "StimuliColor":
        for color in cls:
            if color.int_value == value:
                return color
        return None
