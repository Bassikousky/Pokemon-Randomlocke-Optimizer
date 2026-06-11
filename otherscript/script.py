import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
items_path = base_dir / "items.txt"
output_path = base_dir / "items.csv"

filas = []
valor = None

with items_path.open("r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()

        # Captura el valor entre corchetes
        if linea.startswith("[") and linea.endswith("]"):
            valor = linea[1:-1]

        # Captura el nombre visible
        elif linea.startswith("Name ="):
            nombre = linea.split("=", 1)[1].strip()
            filas.append([nombre, valor])

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["nombre", "valor"])
    writer.writerows(filas)

print(f"Exportados {len(filas)} items")