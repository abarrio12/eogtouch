import pandas as pd
import os
from os.path import expanduser, join

# 1. Ruta al archivo parquet en tu carpeta de usuario
user_dir = expanduser("~")
file_name = "20250507_134319.parquet"
file_path = join(user_dir, file_name)

# 2. Verificar si existe
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"No se encontró el archivo en: {file_path}")

# 3. Leer y ordenar
df = pd.read_parquet(file_path)
df = df.sort_values("timestamp").reset_index(drop=True)

# 4. Mostrar primeras filas (opcional)
print(df.head())

# 5. Guardar a CSV en el mismo sitio
csv_path = join(user_dir, "resultado_exportado.csv")
df.to_csv(csv_path, index=False)
print(f"✅ Datos exportados a: {csv_path}")
