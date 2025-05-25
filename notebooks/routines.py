import pandas as pd

def rellenar_muestras(df: pd.DataFrame) -> pd.DataFrame:
    nuevas_filas = []

    # recorrer el dataframe original comparando la fila actual con la siguiente
    for i in range(len(df) - 1):
        fila_actual = df.iloc[i]
        fila_siguiente = df.iloc[i + 1]
        # accedo a los timestamps de la fila actual y la siguiente
        ts_actual = fila_actual["timestamp"]
        ts_siguiente = fila_siguiente["timestamp"]

        # agregar la fila actual a la lista
        nuevas_filas.append(fila_actual)

        # Si hay diferencia entre timestamps, rellenar
        # el rango va desde el siguiente al actual (nuevo) y el siguiente al ts original.
        for ts_intermedio in range(ts_actual + 1, ts_siguiente):
            fila_intermedia = fila_actual.copy()
            fila_intermedia["timestamp"] = ts_intermedio
            nuevas_filas.append(fila_intermedia)

    # Agregamos la última fila original
    nuevas_filas.append(df.iloc[-1])

    return pd.DataFrame(nuevas_filas).reset_index(drop=True)



