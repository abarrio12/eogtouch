# Calculo cuando el stimuli color pasa de blanco a azul o verde y viceversa, lo que implica inicio y fin de una fijación ocular. 
# Asegurarse de que cada par tiene inicio y fin.

import pandas as pd
from os.path import expanduser, join, getmtime, isfile
from glob import glob
from eogtouch.models.enums import StimuliColor


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

# Identificar cuándo empieza una fijación (de blanco a azul o verde)
df["prev_color"] = df["stimuli_color"].shift(1)

df["start_fixation"] = (
    (df["prev_color"] == StimuliColor.White.int_value) &
    (df["stimuli_color"].isin([StimuliColor.Green.int_value, StimuliColor.Blue.int_value]))
)

# Identificar cuándo termina una fijación (cuando vuelve a blanco)
df["end_fixation"] = (
    (df["prev_color"].isin([StimuliColor.Green.int_value, StimuliColor.Blue.int_value]) &
    (df["stimuli_color"] == StimuliColor.White.int_value)
    )
)

# Obtener los timestamps de inicio y fin
start_times = df[df["start_fixation"]]["timestamp"].reset_index(drop=True)
end_times = df[df["end_fixation"]]["timestamp"].reset_index(drop=True)

# Asegurarse de que hay pares completos --> evita restar arrays de diferente tamaño 
# o que solo haya inicio porque el usuario cierra antes el programa

min_len = min(len(start_times), len(end_times))
duraciones = end_times[:min_len] - start_times[:min_len]

# Crear DataFrame con resultados
resultados = pd.DataFrame({
    "start_time": start_times[:min_len],
    "end_time": end_times[:min_len],
    "fixation_duration_ms": duraciones
})

# Mostrar resultados (ms)
print(resultados)
