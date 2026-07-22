import re, csv

forms_path = "otherscript/pokemon_forms.txt"
csv_path = "Pokemon.csv"

# Load existing CSV entries
existing = {}
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["Name"]
        form = row.get("Form", "").strip()
        existing[(name, form)] = row

# Read the forms file and extract mega entries
with open(forms_path, "r", encoding="utf-8") as f:
    content = f.read()

# Split into sections
blocks = re.split(r'#-+\n', content)

def name_title(s):
    """Convert VENUSAUR -> Venusaur, FARFETCHD -> Farfetch'd, etc."""
    if s == "NIDORAN":
        return "Nidoran"
    if s == "MRMIME":
        return "Mr. Mime"
    if s == "FARFETCHD":
        return "Farfetch'd"
    if s == "TYPE_NULL":
        return "Type: Null"
    if s == "FLOETTE":
        return "Floette"
    if s == "FLABEBE":
        return "Flabébé"
    if s == "MIME_JR":
        return "Mime Jr."
    return s.title()

def parse_stats_line(line):
    parts = line.split("=")
    if len(parts) < 2:
        return None
    vals = parts[1].strip().split(",")
    if len(vals) != 6:
        return None
    return [int(v.strip()) for v in vals]

def parse_section(section):
    section = section.strip()
    if not section:
        return None
    # Check if this block has a header like [VENUSAUR,1]
    header_match = re.match(r'\[(\w+),(\d+)\]', section)
    if not header_match:
        return None
    base_name_raw = header_match.group(1)
    form_num = int(header_match.group(2))
    
    # Parse FormName
    form_name = None
    types_line = None
    base_stats = None
    generation = None
    
    lines = section.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('FormName ='):
            form_name = line.split('=', 1)[1].strip()
        elif line.startswith('Types ='):
            types_line = line.split('=', 1)[1].strip()
        elif line.startswith('BaseStats ='):
            base_stats = parse_stats_line(line)
        elif line.startswith('Generation ='):
            try:
                generation = int(line.split('=', 1)[1].strip())
            except:
                pass
    
    # Only process if it has a mega form name
    if not form_name or 'mega' not in form_name.lower():
        return None
    if not base_stats:
        return None
    
    base_name = name_title(base_name_raw)
    
    # Get generation from existing CSV if not in forms file
    if generation is None:
        for (n, f), row in existing.items():
            if n.lower() == base_name.lower() and (f == '' or f == ' '):
                generation = int(row['Generation'])
                break
    
    # Get types from forms file or from existing CSV
    type1 = None
    type2 = ''
    if types_line:
        parts = [t.strip() for t in types_line.split(',')]
        type1 = parts[0].title()
        type2 = parts[1].title() if len(parts) > 1 else ''
    else:
        for (n, f), row in existing.items():
            if n.lower() == base_name.lower():
                type1 = row['Type1']
                type2 = row['Type2'].strip() if row['Type2'].strip() else ''
                break
    
    if not type1:
        return None
    
    hp, atk, defense, speed, spatk, spdef = base_stats
    total = hp + atk + defense + spatk + spdef + speed
    
    # Get ID from existing CSV
    pokemon_id = None
    for (n, f), row in existing.items():
        if n.lower() == base_name.lower() and (f == '' or f == ' '):
            pokemon_id = int(row['ID'])
            break
    if pokemon_id is None:
        return None
    
    return {
        'id': pokemon_id,
        'name': base_name,
        'form': form_name,
        'type1': type1,
        'type2': type2,
        'total': total,
        'hp': hp,
        'attack': atk,
        'defense': defense,
        'sp_atk': spatk,
        'sp_def': spdef,
        'speed': speed,
        'generation': generation or 6
    }

# Parse all mega entries
mega_entries = []
for block in blocks:
    entry = parse_section(block)
    if entry:
        mega_entries.append(entry)

print(f"Found {len(mega_entries)} mega form entries in forms file")

# Check which are already in CSV
existing_set = set()
for (n, f) in existing:
    existing_set.add((n.lower(), f.lower().strip() if f.strip() else ''))

missing = []
for e in mega_entries:
    form_check = e['form'].strip().lower()
    if (e['name'].lower(), form_check) not in existing_set:
        # Also check with common variations
        found = False
        for (n, f) in existing:
            if n.lower() == e['name'].lower():
                # Mega Venusaur X vs Mega Venusaur
                ef = form_check.replace(' x', '').replace(' y', '')
                xf = f.replace(' x', '').replace(' y', '')
                if ef == xf:
                    found = True
                    break
        if not found:
            missing.append(e)

print(f"Missing mega entries to add: {len(missing)}")
for e in missing:
    print(f"  {e['id']},{e['name']},{e['form']},{e['type1']},{e['type2']},{e['total']},{e['hp']},{e['attack']},{e['defense']},{e['sp_atk']},{e['sp_def']},{e['speed']},{e['generation']}")

# Append missing entries to CSV
if missing:
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for e in missing:
            writer.writerow([
                e['id'], e['name'], e['form'], e['type1'], e['type2'],
                e['total'], e['hp'], e['attack'], e['defense'],
                e['sp_atk'], e['sp_def'], e['speed'], e['generation']
            ])
    print(f"\nAppended {len(missing)} new mega forms to {csv_path}")
else:
    print("\nNo new mega forms to add")
