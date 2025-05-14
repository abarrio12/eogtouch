# Buscar las filas donde color estimulo es blanco y la posición del estimulo ha cambiado respecto a la anterior fila blanca.
# Guardar en un csv las filas donde se ha detectado un cambio de posición
# aparicion_estimulo.py

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

# Detectar cambios de posición (nuevo estímulo)
df["stimuli_change"] = (df["stimuli_x"].diff() != 0) | (df["stimuli_y"].diff() != 0)

# Filtramos las filas donde el estímulo es blanco (inicio de iteración) y hay cambio de posición
apariciones = df[(df["stimuli_color"] == StimuliColor.White.int_value) & df["stimuli_change"]]

# Extraemos los timestamps de aparición
resultados = apariciones["timestamp"].reset_index(drop=True)

# Mostrar resultados (ms)

print(resultados)

print("Columnas disponibles:", df.columns)