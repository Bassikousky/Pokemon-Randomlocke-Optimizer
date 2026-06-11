import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
input_path = base_dir / "stats.txt"
output_path = base_dir / "stats.csv"

rows = []

with input_path.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        if len(parts) < 6:
            continue
        
        name = parts[0]
        old_type = parts[1]
        new_type = parts[2]
        old_stats = parts[3]
        new_stats = parts[4]
        bst_change = parts[5]
        
        # Parse old type
        if "/" in old_type:
            old_type1, old_type2 = old_type.split("/")
        else:
            old_type1 = old_type
            old_type2 = ""
        
        # Parse new type
        if "/" in new_type:
            type1, type2 = new_type.split("/")
        else:
            type1 = new_type
            type2 = ""
        
        # Parse old stats
        old_stats_list = old_stats.split("/")
        if len(old_stats_list) == 6:
            old_hp, old_attack, old_defense, old_sp_atk, old_sp_def, old_speed = old_stats_list
        else:
            continue
        
        # Parse new stats
        new_stats_list = new_stats.split("/")
        if len(new_stats_list) == 6:
            hp, attack, defense, sp_atk, sp_def, speed = new_stats_list
        else:
            continue
        
        row = [
            name,
            old_type1,
            old_type2,
            type1,
            type2,
            old_hp,
            old_attack,
            old_defense,
            old_sp_atk,
            old_sp_def,
            old_speed,
            hp,
            attack,
            defense,
            sp_atk,
            sp_def,
            speed,
            bst_change
        ]
        rows.append(row)

# Write CSV
with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Name",
        "oldType1",
        "oldType2",
        "Type1",
        "Type2",
        "oldHP",
        "oldAttack",
        "oldDefense",
        "oldSp. Atk",
        "oldSp. Def",
        "oldSpeed",
        "HP",
        "Attack",
        "Defense",
        "Sp. Atk",
        "Sp. Def",
        "Speed",
        "bstChange"
    ])
    writer.writerows(rows)

print(f"Exportados {len(rows)} pokemon a stats.csv")
