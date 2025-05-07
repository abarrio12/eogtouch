import pandas as pd
from os.path import expanduser, join, getmtime, isfile
from glob import glob
from eogtouch.models.enums import StimuliColor
from eogtouch.models.config import GREEN_KEYS, BLUE_KEYS
import pygame

# 1. Buscar el último archivo .parquet en la carpeta del usuario
user_dir = expanduser("~")
parquet_files = [f for f in glob(join(user_dir, "*.parquet")) if isfile(f)]

if not parquet_files:
    raise FileNotFoundError("No se encontraron archivos .parquet en el directorio del usuario.")

# 2. Elegir el archivo más reciente
latest_file = max(parquet_files, key=getmtime)

# 3. Cargar los datos
df = pd.read_parquet(latest_file)

# Aseguramos orden cronológico
df = df.sort_values("timestamp").reset_index(drop=True)

# Detectar si hay cambio de color del estímulo entre filas consecutivas
df['stimulus_change'] = df['stimuli_color'].diff().abs() > 0

# Solo itero las filas donde hubo un cambio de color del estímulo
for idx, row in df[df['stimulus_change']].iterrows():
    stimulus_time = row['timestamp']
    stimulus_color = row['stimuli_color']

    if stimulus_color not in [StimuliColor.Green.int_value, StimuliColor.Blue.int_value]: 
        continue

    df_window = df[(df['timestamp'] >= stimulus_time) & (df['timestamp'] <= stimulus_time + 5000)] # creo una ventana de 5 segundos para comprobar la tecla pulsada

    key_row = df_window[df_window["key"] > 0].head(1)
    if not key_row.empty:
        key_pressed = int(key_row["key"].values[0])
        is_correct = False

        if stimulus_color == StimuliColor.Green.int_value:
            is_correct = key_pressed in GREEN_KEYS
        elif stimulus_color == StimuliColor.Blue.int_value:
            is_correct = key_pressed in BLUE_KEYS

        color_enum = StimuliColor.from_int_value(stimulus_color)
        key_name = pygame.key.name(key_pressed)
        result = "bien" if is_correct else "fallo"
        
        print(f"StimuliColor: {color_enum.name}  Tecla: {key_name} = {result}")
    else:
        print(f"No se presionó ninguna tecla. Fila: {idx}")
