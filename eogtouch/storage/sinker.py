from os.path import expanduser, join
from time import time

import numpy as np
import pandas as pd

from eogtouch.models.enums import StimuliColor


class DataSinker:
    def __init__(self, samples: int = 5 * 60 * 1000):
        self.current_sample = 0
        self.samples = samples
        self.data = np.zeros((self.samples, 7), dtype=np.uint64)

    def add_sample(
        self,
        stimuli_x: int,
        stimuli_y: int,
        stimuli_color: StimuliColor,
        eyes_x: int,
        eyes_y: int,
        key: int,
    ):
        self.data[self.current_sample][0] = int(time() * 1000)
        self.data[self.current_sample][1] = stimuli_x
        self.data[self.current_sample][2] = stimuli_y
        self.data[self.current_sample][3] = stimuli_color.int_value
        self.data[self.current_sample][4] = eyes_x
        self.data[self.current_sample][5] = eyes_y
        self.data[self.current_sample][6] = key
        self.current_sample += 1

    def build_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(
            self.data[: self.current_sample],
            columns=[
                "timestamp",
                "stimuli_x",
                "stimuli_y",
                "stimuli_color",
                "eyes_x",
                "eyes_y",
                "key",
            ],
        )
        df = df.astype({
            "timestamp": np.uint64,
            "stimuli_x": np.uint16,
            "stimuli_y": np.uint16,
            "stimuli_color": np.uint32,
            "eyes_x": np.uint16,
            "eyes_y": np.uint16,
            "key": np.uint8,
        })

        return df

    def save(self, filename: str):
        if not filename.endswith(".parquet"):
            filename += ".parquet"

        basepath = expanduser("~")
        filename = join(basepath, filename)

        print(f"Saving data to {filename}")

        df = self.build_dataframe()
        df.to_parquet(filename, index=False)
