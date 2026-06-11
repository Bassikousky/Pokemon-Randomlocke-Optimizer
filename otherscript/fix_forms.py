import re
import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

forms_path = base_dir / "otherscript" / "pokemon_forms.txt"
pokemon_csv_path = base_dir / "Pokemon.csv"
evo_csv_path = base_dir / "pokemon_evoluciones.csv"

spanish_to_english_form = {
    "Forma Alola": "Alolan",
    "Forma Galar": "Galarian",
    "Forma Hisui": "Hisuian",
}

def parse_forms_file(path):
    sections = {}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r'#-+\n', content)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        header_match = re.match(r'\[([A-Z0-9_.-]+),(\d+)\]', block)
        if not header_match:
            continue
        base_name = header_match.group(1)
        form_id = int(header_match.group(2))
        fields = {}
        for line in block.split('\n'):
            if '=' in line:
                key, _, value = line.partition('=')
                fields[key.strip()] = value.strip()
        form_name = fields.get("FormName", "")
        region = fields.get("Region", "")
        types = fields.get("Types", "")
        evolutions = fields.get("Evolutions", "")
        if types or region or evolutions:
            sections[(base_name, form_id)] = {
                "form_name": form_name,
                "region": region,
                "types": types,
                "evolutions": evolutions,
                "base_name": base_name,
            }
    return sections

def form_to_english(base_name, spanish_form_name):
    prefix = spanish_to_english_form.get(spanish_form_name, "")
    if not prefix:
        return None
    return f"{prefix} {base_name.capitalize()}"

method_mapping = {
    "LevelUp": "Level",
    "LevelNight": "Level",
    "LevelDay": "Level",
    "LevelFemale": "LevelFemale",
    "LevelMale": "LevelMale",
    "UseItem": "Item",
    "Trade": "Trade",
    "Happiness": "Happiness",
    "None": None,
}

def parse_evolutions(evo_str):
    if not evo_str:
        return []
    result = []
    # Pattern: EVOTARGET,METHOD,VALUE (VALUE optional, then possibly more groups)
    # Tokenize: split by comma, then group as (target, method, value?)
    tokens = [t.strip() for t in evo_str.split(",")]
    i = 0
    while i < len(tokens):
        if i + 1 >= len(tokens):
            break
        target = tokens[i]
        method_raw = tokens[i + 1]
        method = method_mapping.get(method_raw, method_raw)
        if method is None:
            i += 2
            continue
        # Check if next token is a numeric value or item name
        if i + 2 < len(tokens):
            next_tok = tokens[i + 2]
            # Is it a value (digits) or item name (all caps)?
            if next_tok.isdigit() or (next_tok.isupper() and next_tok.isalpha()):
                valor = next_tok
                i += 3
            else:
                valor = ""
                i += 2
        else:
            valor = ""
            i += 2
        result.append((target, method, valor))
    return result

print("Parsing pokemon_forms.txt...")
form_sections = parse_forms_file(forms_path)

# Build mapping: english_form_name -> types
form_type_fix = {}
for (base, fid), info in form_sections.items():
    if not info["types"] or not info["form_name"]:
        continue
    eng_form = form_to_english(info["base_name"], info["form_name"])
    if not eng_form:
        continue
    types = [t.strip() for t in info["types"].split(",")]
    type1 = types[0].capitalize()
    type2 = types[1].capitalize() if len(types) > 1 else ""
    form_type_fix[eng_form] = (type1, type2)
    print(f"  {eng_form}: {type1}/{type2}")

# Update Pokemon.csv
print("\nUpdating Pokemon.csv types...")
rows = []
with open(pokemon_csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        form = row.get("Form", "").strip()
        if form in form_type_fix:
            old_t1, old_t2 = row["Type1"], row["Type2"]
            new_t1, new_t2 = form_type_fix[form]
            if old_t1 != new_t1 or old_t2.strip() != new_t2:
                print(f"  Fix {form}: {old_t1}/{old_t2} -> {new_t1}/{new_t2}")
            row["Type1"] = new_t1
            row["Type2"] = new_t2 if new_t2 else ""
        rows.append(row)

with open(pokemon_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print("Done updating Pokemon.csv")

# Build regional evolution entries
print("\nBuilding regional evolution entries...")
regional_evos = []
for (base, fid), info in form_sections.items():
    if not info["evolutions"] or not info["form_name"]:
        continue
    eng_form = form_to_english(info["base_name"], info["form_name"])
    if not eng_form:
        continue
    evos = parse_evolutions(info["evolutions"])
    if not evos:
        continue
    prefix = eng_form.split()[0]
    for target, method, valor in evos:
        # Target form: same prefix + target name
        target_form = f"{prefix} {target.capitalize()}"
        print(f"  {eng_form} -> {target_form} ({method}, {valor})")
        regional_evos.append({
            "pokemon": info["base_name"].capitalize(),
            "form": eng_form,
            "evolucion": target.upper(),
            "metodo": method,
            "valor": valor,
        })

# Remove duplicates
seen_evo = set()
unique_evos = []
for e in regional_evos:
    key = (e["pokemon"].lower(), e["form"].lower(), e["evolucion"].lower(), e["metodo"], e["valor"])
    if key not in seen_evo:
        seen_evo.add(key)
        unique_evos.append(e)
regional_evos = unique_evos

print(f"\nFound {len(regional_evos)} regional evolution entries")

# Write new pokemon_evoluciones.csv with form column
print("\nWriting new pokemon_evoluciones.csv...")
old_evos = []
with open(evo_csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        old_evos.append(row)

new_fieldnames = ["pokemon", "evolucion", "metodo", "valor", "form"]
with open(evo_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=new_fieldnames)
    writer.writeheader()
    for row in old_evos:
        writer.writerow({
            "pokemon": row["pokemon"],
            "evolucion": row["evolucion"],
            "metodo": row["metodo"],
            "valor": row["valor"],
            "form": "",
        })
    for e in regional_evos:
        writer.writerow({
            "pokemon": e["pokemon"],
            "evolucion": e["evolucion"],
            "metodo": e["metodo"],
            "valor": e["valor"],
            "form": e["form"],
        })
print("Done writing new pokemon_evoluciones.csv")
print("\nAll fixes applied!")
