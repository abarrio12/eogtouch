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


# movement_threshold: umbral de movimiento ocular (en píxeles) para considerar que ha habido un movimiento significativo.
# direction_threshold: umbral de dirección (coseno del ángulo >= 0.7) para considerar que el movimiento ocular va hacia el estímulo.

def detect_latency_from_parquet(df, movement_threshold=5, direction_threshold=0.7):
    latencies = []
    movement_start_indices = []

    # Detectar aparición de nuevo estímulo
    df['stimulus_change'] = (df['stimuli_x'].diff().abs() + df['stimuli_y'].diff().abs()) > 0
    print(f"Estímulos detectados: {df['stimulus_change'].sum()}")

    # recorremos cada fila donde haya un cambio en la posición del estímulo
    for stimulus_idx, row in df[df['stimulus_change']].iterrows(): 
        stimulus_position = np.array([row['stimuli_x'], row['stimuli_y']])
        stimulus_time = row['timestamp']
        search_start_index = df.index.get_loc(stimulus_idx) # cogemos el indice a partir del cual comparamos is there eye movement?

        print(f"\nEstímulo en fila {stimulus_idx}, t = {stimulus_time}, pos = {stimulus_position}")

        for i in range(search_start_index + 1, len(df)):
            eye_prev = np.array([df.iloc[i - 1]['eyes_x'], df.iloc[i - 1]['eyes_y']])
            eye_curr = np.array([df.iloc[i]['eyes_x'], df.iloc[i]['eyes_y']])
            delta = eye_curr - eye_prev
            displacement = np.linalg.norm(delta)

            if displacement > movement_threshold:
                direction_vector = stimulus_position - eye_prev
                if np.linalg.norm(direction_vector) == 0:
                    continue
                
                # se calcula el coseno del ángulo entre el vector de movimiento ocular y el vector hacia el estímulo. 
                # Si es > umbral entenderemos que va hacia el estimulo    
                cos_angle = np.dot(delta, direction_vector) / (
                    np.linalg.norm(delta) * np.linalg.norm(direction_vector)
                )

                if cos_angle >= direction_threshold:
                    latency = df.iloc[i]['timestamp'] - stimulus_time
                    latencies.append(latency)
                    movement_start_indices.append(i)
                    print(f"Movimiento hacia el estímulo detectado en fila {i} con latencia {latency} ms")
                    break
        else:
            print("No se detectó movimiento ocular hacia el estímulo.")
            latencies.append(None)
            movement_start_indices.append(None)

    return latencies, movement_start_indices


# Ejecutar análisis
latencies, start_indices = detect_latency_from_parquet(df)


# # Mostrar resultados formato tabla
# for i, (latency, index) in enumerate(zip(latencies, start_indices)):
#     if latency is not None:
#         print(f"Estímulo {i+1}: movimiento comienza en fila {index}, latencia = {latency} ms")
#     else:
#         print(f"Estímulo {i+1}: no se detectó movimiento")
