# Comparo entre una fila y otra el color. Si ha cambiado es porque la mirada se ha fijado. 

import pandas as pd
from eogtouch.models.enums import StimuliColor
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

# Aseguramos orden cronológico
df = df.sort_values("timestamp").reset_index(drop=True)

# Detectar los momentos en los que el estímulo cambia de blanco a otro color (fijación detectada)
fixations = df[
    (df["stimuli_color"] != StimuliColor.White.int_value) &
    (df["stimuli_color"].shift(1) == StimuliColor.White.int_value)
]

color_map = {color.int_value: color.name for color in StimuliColor}

# Mostrar resultados
result = fixations[["timestamp", "stimuli_color"]].reset_index(drop=True)

# para que salga en el csv el nombre del color en vez del valor entero
result["stimuli_color_name"] = result["stimuli_color"].map(color_map)

print(result)
