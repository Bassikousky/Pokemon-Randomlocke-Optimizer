import csv

EVO_CSV = r"C:\Games\Pokemon\Random Optimizer\pokemon_evoluciones.csv"

target_forms = {
    ("Rattata", "RATICATE", "Alolan Rattata"): "Alolan Raticate",
    ("Sandshrew", "SANDSLASH", "Alolan Sandshrew"): "Alolan Sandslash",
    ("Vulpix", "NINETALES", "Alolan Vulpix"): "Alolan Ninetales",
    ("Meowth", "PERSIAN", "Alolan Meowth"): "Alolan Persian",
    ("Meowth", "PERRSERKER", "Galarian Meowth"): "",
    ("Slowpoke", "SLOWBRO", "Galarian Slowpoke"): "Galarian Slowbro",
    ("Slowpoke", "SLOWKING", "Galarian Slowpoke"): "Galarian Slowking",
    ("Farfetch'd", "SIRFETCHD", "Galarian Farfetch'd"): "",
    ("Mr. Mime", "MRRIME", "Galarian Mr. Mime"): "",
    ("Corsola", "CURSOLA", "Galarian Corsola"): "",
    ("Linoone", "OBSTAGOON", "Galarian Linoone"): "",
    ("Darumaka", "DARMANITAN", "Galarian Darumaka"): "Galarian Standard Mode",
    ("Yamask", "RUNERIGUS", "Galarian Yamask"): "",
    ("Voltorb", "ELECTRODE", "Hisuian Voltorb"): "Hisuian Electrode",
    ("Qwilfish", "OVERQWIL", "Hisuian Qwilfish"): "",
    ("Sneasel", "SNEASLER", "Hisuian Sneasel"): "",
}

rows = []
with open(EVO_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames + ["forma_evolucion"]
    for row in reader:
        pkmn = row["pokemon"].strip()
        evo = row["evolucion"].strip()
        form = row.get("form", "").strip()
        key = (pkmn, evo, form)
        row["forma_evolucion"] = target_forms.get(key, "")
        rows.append(row)

with open(EVO_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(rows)} rows with new forma_evolucion column")
