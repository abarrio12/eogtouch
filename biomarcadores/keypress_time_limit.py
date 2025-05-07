import pandas as pd
import numpy as np
from os.path import expanduser, join, getmtime, isfile
from glob import glob

# 1. Buscar el último archivo .parquet en la carpeta del usuario
user_dir = expanduser("~")
parquet_files = [f for f in glob(join(user_dir, "*.parquet")) if isfile(f)]

if not parquet_files:
    raise FileNotFoundError("No se encontraron archivos .parquet en el directorio del usuario.")

# 2. Elegir el archivo más reciente
latest_file = max(parquet_files, key=getmtime)

# 3. Cargar los datos
df = pd.read_parquet(latest_file)

# Asegurar orden cronológico
df = df.sort_values("timestamp").reset_index(drop=True)


df['stimulus_change'] = (df['stimuli_x'].diff().abs() + df['stimuli_y'].diff().abs()) > 0


for stimulus_idx, row in df[df['stimulus_change']].iterrows(): 
    stimulus_time = row['timestamp']

    time_limit = stimulus_time + 5000

    # Filtra filas entre aparición del estímulo y los 5 segundos siguientes
    df_window = df[(df["timestamp"] >= stimulus_time) & (df["timestamp"] <= time_limit)]

    # mira si se presionó una tecla en ese intervalo
    pressed_early = df_window["key"].astype(int).any()

    print(f"\n Estímulo en fila {stimulus_idx}, t = {stimulus_time}")
    print("Press in time" if pressed_early else "Press out of time")
