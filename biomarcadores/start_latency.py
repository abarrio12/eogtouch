# (Latencia de arranque): Tiempo transcurrido (ms) desde que el estímulo cambia de posición y los
#   ojos comienzan a moverse. Para esto hay que definir un umbral de velocidad que defina cuando se arranca.


import pandas as pd
from numpy import array, sqrt
from scipy.signal import find_peaks, convolve
from numpy import ndarray
import numpy as np
from os.path import expanduser, isfile, join, getmtime
import glob



# 1. Buscar el último archivo .parquet en la carpeta del usuario
user_dir = expanduser("~")
parquet_files = [f for f in glob.glob(join(user_dir, "*.parquet")) if isfile(f)]
if not parquet_files:
    raise FileNotFoundError("No se encontraron archivos .parquet en el directorio del usuario.")

# 2. Elegir el archivo más reciente
latest_file = max(parquet_files, key=getmtime)

# 3. Cargar y ordenar los datos
df = pd.read_parquet(latest_file)
df = df.sort_values("timestamp").reset_index(drop=True)

# Renombrar columnas para que coincidan con las que esperan las funciones

df = df.rename(columns={
    'timestamp': 'ts',
    'stimuli_x': 'sx',
    'stimuli_y': 'sy',
    'eyes_x': 'ex',
    'eyes_y': 'ey'
})


def rellenar_muestras(df: pd.DataFrame) -> pd.DataFrame:
   
    nuevas_filas = []

    # recorrer el dataframe original comparando la fila actual con la siguiente
    for i in range(len(df) - 1):
        fila_actual = df.iloc[i]
        fila_siguiente = df.iloc[i + 1]
        # accedo a los timestamps de la fila actual y la siguiente
        ts_actual = fila_actual["ts"]
        ts_siguiente = fila_siguiente["ts"]

        # agregar la fila actual a la lista
        nuevas_filas.append(fila_actual)

        # Si hay diferencia entre timestamps, rellenar
        # el rango va desde el siguiente al actual (nuevo) y el siguiente al ts original.
        for ts_intermedio in range(ts_actual + 1, ts_siguiente):
            fila_intermedia = fila_actual.copy()
            fila_intermedia["ts"] = ts_intermedio
            nuevas_filas.append(fila_intermedia)

    # Agregamos la última fila original
    nuevas_filas.append(df.iloc[-1])

    return pd.DataFrame(nuevas_filas).reset_index(drop=True)




def distance(x, y):
    """
    Calcula la distancia entre dos puntos en un espacio 2D (vector desplazamiento).

    Args:
        x (ndarray): Coordenadas x de los puntos.
        y (ndarray): Coordenadas y de los puntos.

    Returns:
        ndarray: Distancia entre los puntos.
    """
    x_prev = x[:-1]
    x_curr = x[1:]
    y_prev = y[:-1]
    y_curr = y[1:]
    return sqrt((x_prev - x_curr) ** 2 + (y_prev - y_curr) ** 2)



def differentiate(channel):
    window = array([300, -294, -532, -503, -296, 0, 296, 503, 532, 294, -300])
    result = convolve(channel, window, "same") / 5148.0
    result[:5] = 0
    result[-5:] = 0
    return result*1000




def velocity_peaks(velocity: ndarray, threshold: float = 0.5) -> list[int]:
    
    """
    Encuentra picos de velocidad, permitiendo mesetas si son mayores al umbral.

    Args:
        velocity (ndarray): Perfil de velocidad.
        threshold (float): Umbral mínimo para considerar un pico.

    Returns:
        list[int]: Índices de los picos detectados.
    """
    abs_velocity = np.abs(velocity)
    peaks, _ = find_peaks(abs_velocity, height=threshold)

    return peaks.tolist()




def starts(abs_velocity, peaks, threshold=0.5):
    """
    Encuentra los índices de inicio de los picos de velocidad.

    Args:
        abs_velocity (ndarray): Perfil de velocidad absoluto.
        peaks (list[int]): Índices de los picos detectados.
        threshold (float): Umbral mínimo para considerar un pico.

    Returns:
        list[int]: Índices de inicio de los picos detectados.
    """
    start_indices = []
    for peak in peaks:
        for i in range(peak, 0, -1):
            if abs_velocity[i] < threshold and abs_velocity[i + 1] > threshold:
                start_indices.append(i + 1)
                break
        else:
            start_indices.append(0)
    return start_indices



def start_latency(df, threshold = 0.5, ventana = 600):
    
    """
    Calcula la latencia de arranque a partir de un DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame con columnas 'ts', 'sx', 'sy', 'ex', 'ey'.
        threshold (float): Umbral mínimo para considerar un pico.
        ventana (int): Tamaño de la ventana para el cálculo de la velocidad.

    Returns:
        list[int]: Lista de latencias de arranque.
    """
    
    latencias = []
    df = df.reset_index(drop=True)
    df["stimuli_change"] = (df["sx"].diff() != 0) | (df["sy"].diff() != 0)

    for i in range(1, len(df)):
        if df.loc[i, "stimuli_change"] and i + ventana <= len(df):
            ts_cambio = df.loc[i, 'ts']
            ventana_df = df.iloc[i:i + ventana]
        
            ex = ventana_df['ex'].values
            ey = ventana_df['ey'].values
            ts = ventana_df['ts'].values

            vx = differentiate(ex)
            vy = differentiate(ey)
            vel = np.sqrt(vx**2 + vy**2)
            abs_vel = np.abs(vel)

            peaks = velocity_peaks(abs_vel, threshold)
            print("Picos:", peaks)
            
            if not peaks:
                latencias.append(None)
                continue

            inicios = starts(abs_vel, peaks, threshold)
            ts_inicio = ts[inicios[0]]
            latencias.append(int(ts_inicio - ts_cambio))


    return latencias





latencias = start_latency(df, threshold=0.1, ventana=600)
print("Latencia detectada:", latencias)
