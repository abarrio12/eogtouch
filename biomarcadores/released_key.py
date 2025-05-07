# Detecta el momento en que se soltó una tecla (cuando 'key' pasa de un valor positivo a 0)

import pandas as pd
from os.path import expanduser, join, getmtime, isfile
from glob import glob
import pygame


# 1. Buscar el último archivo .parquet en la carpeta del usuario
user_dir = expanduser("~")
parquet_files = [f for f in glob(join(user_dir, "*.parquet")) if isfile(f)]
if not parquet_files:
    raise FileNotFoundError("No se encontraron archivos .parquet en el directorio del usuario.")

# 2. Elegir el archivo más reciente
latest_file = max(parquet_files, key=getmtime)

# 3. Cargar y ordenar los datos
df = pd.read_parquet(latest_file)
df = df.sort_values("timestamp").reset_index(drop=True)


# cuando key pasa de un valor > 0 a 0 → release
df["key_prev"] = df["key"].shift(1)

# Detectar presiones y liberaciones directamente
pressed_times = df[(df["key_prev"] == 0) & (df["key"] > 0)]["timestamp"].reset_index(drop=True)
df_released = df[(df["key_prev"] > 0) & (df["key"] == 0)][["timestamp", "key_prev"]].reset_index(drop=True)

# Lo he puesto opcional calcular cuánto mantienen presionada la tecla
df_released["press_time"] = pressed_times
df_released["duracion_ms"] = df_released["timestamp"] - df_released["press_time"]


df_released["key_prev"] = df_released["key_prev"].astype(int)
df_released["key_name"] = df_released["key_prev"].apply(pygame.key.name)

print(df_released)