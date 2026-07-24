import csv

csv_path = "Pokemon.csv"

rows = []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        rows.append(row)

# Manual corrections from the forms file (Spanish name -> English CSV name mapping)
corrections = {
    # Wormadam (Spanish: Forma Tronco Arena -> Sandy Cloak, Forma Tronco Basura -> Trash Cloak)
    ('Wormadam', 'Sandy Cloak'): ('Bug', 'Ground'),
    ('Wormadam', 'Trash Cloak'): ('Bug', 'Steel'),
    # Castform
    ('Castform', 'Sunny Form'): ('Fire', ''),
    ('Castform', 'Rainy Form'): ('Water', ''),
    ('Castform', 'Snowy Form'): ('Ice', ''),
    # Oricorio styles (already correct, but include for reference)
    # Deoxys forms
    ('Deoxys', 'Attack Forme'): ('Psychic', ''),
    ('Deoxys', 'Defense Forme'): ('Psychic', ''),
    ('Deoxys', 'Speed Forme'): ('Psychic', ''),
    # Rotom forms (already correct in CSV)
    # Lycanroc forms
    # Wishiwashi forms
}

fixes = 0
for i, row in enumerate(rows):
    name = row[1]
    form = row[2].strip()
    if (name, form) in corrections:
        new_t1, new_t2 = corrections[(name, form)]
        old_t1, old_t2 = row[3], row[4].strip()
        if new_t1 != old_t1 or new_t2 != old_t2:
            print(f"FIX: {name}|{form}: {old_t1}/{old_t2} -> {new_t1}/{new_t2}")
            row[3] = new_t1
            row[4] = new_t2
            fixes += 1

print(f"\nFixed {fixes} entries")

if fixes > 0:
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Written to {csv_path}")
