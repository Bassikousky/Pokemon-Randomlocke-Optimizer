import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
evo_csv_path = base_dir / "pokemon_evoluciones.csv"

# These are the original CSV evolution entries for pokemon that ALSO have
# regional form evolutions. Keep only these (form empty) + any entry with form set.
original_valid = {
    ("rattata", "raticate", "level", "20"),
    ("sandshrew", "sandslash", "level", "22"),
    ("vulpix", "ninetales", "item", "FIRESTONE"),
    ("meowth", "persian", "level", "28"),
    ("slowpoke", "slowbro", "level", "37"),
    ("slowpoke", "slowking", "dayholditem", "KINGSROCK"),
    ("slowpoke", "slowking", "item", "WATERSTONE"),
    ("slowpoke", "slowking", "tradeitem", "KINGSROCK"),
    ("farfetch'd", "sirfetchd", "level", "36"),  # Not in original, but keep
    ("mrmime", "mrrime", "item", "DAWNSTONE"),
}

rows = []
removed = 0
with open(evo_csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        form = row.get("form", "").strip()
        pokemon = row["pokemon"].strip().lower()
        evolucion = row["evolucion"].strip().lower()
        metodo = row["metodo"].strip().lower()
        valor = row["valor"].strip().upper()

        # Remove entries where pokemon name is a number (junk from first run)
        if row["pokemon"].strip().isdigit():
            removed += 1
            continue

        # For entries with empty form, check if they're from the original CSV
        if not form:
            # Build the key for comparison
            clean_pokemon = pokemon.replace("'", "").replace(".", "").replace("é", "e")
            is_valid = (clean_pokemon, evolucion, metodo, valor) in original_valid or \
                       (pokemon, evolucion, metodo, valor) in original_valid
            
            if not is_valid and pokemon in ("rattata", "sandshrew", "vulpix", "meowth",
                                            "slowpoke", "farfetchd", "mrmime", "corsola",
                                            "linoone", "darumaka", "yamask", "voltorb",
                                            "qwilfish", "sneasel"):
                # This is likely a bad entry from the first run
                removed += 1
                continue

        rows.append(row)

with open(evo_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Cleaned CSV: {len(rows)} rows (removed {removed} bad entries)")
