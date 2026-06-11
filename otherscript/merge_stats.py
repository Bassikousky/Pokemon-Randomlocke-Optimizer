import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
stats_path = base_dir / "stats.csv"
pokemon_path = base_dir / "Pokemon.csv"
output_path = base_dir / "Pokemon_updated.csv"

# Read stats.csv into a dictionary keyed by name
stats_dict = {}
with stats_path.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stats_dict[row["Name"]] = row

# Read and update Pokemon.csv
updated_rows = []
with pokemon_path.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        name = row["Name"]
        
        # If this Pokemon is in stats.csv, update it
        if name in stats_dict:
            stats = stats_dict[name]
            
            # Update types
            row["Type1"] = stats["Type1"]
            row["Type2"] = stats["Type2"]
            
            # Update Total: current Total + bstChange
            current_total = int(row["Total"])
            bst_change_str = stats["bstChange"]
            # bstChange might have + sign, remove it
            bst_change = int(bst_change_str.replace("+", ""))
            row["Total"] = str(current_total + bst_change)
            
            # Update stats - use the new values from stats.csv
            row["HP"] = stats["HP"]
            row["Attack"] = stats["Attack"]
            row["Defense"] = stats["Defense"]
            row["Sp. Atk"] = stats["Sp. Atk"]
            row["Sp. Def"] = stats["Sp. Def"]
            row["Speed"] = stats["Speed"]
        
        updated_rows.append(row)

# Write updated Pokemon.csv
with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Actualizados {len(updated_rows)} pokemon en Pokemon_updated.csv")

# Count how many were actually updated
count_updated = sum(1 for name in stats_dict.keys() if any(row["Name"] == name for row in updated_rows))
print(f"Filas con stats actualizadas: {count_updated}")
