import glob
import pandas as pd

# Buscar todos los archivos .parquet en ./data/
parquet_files = sorted(glob.glob("./data/*.parquet"))

# Cargar el último archivo generado
if parquet_files:
    latest_file = parquet_files[-1]  # El más reciente
    df = pd.read_parquet(latest_file, engine="pyarrow")
    print(df)
else:
    print("No se encontraron archivos .parquet en ./data/")
