import sys
sys.path.insert(0, r"C:\Games\Pokemon\Random Optimizer")

def _norm(s):
    return s.lower().strip().replace("-", "").replace("'", "").replace(".", "").replace(" ", "")

tests = [
    ("MRMIME", "Mr. Mime"),
    ("MRRIME", "Mr. Rime"),
    ("MR.RIME", "Mr. Rime"),
    ("Mime Jr.", "Mime Jr."),
    ("SIRFETCHD", "Sirfetch'd"),
    ("SIRFETCH'D", "Sirfetch'd"),
    ("PORYGONZ", "Porygon-Z"),
    ("PORYGON-Z", "Porygon-Z"),
]

for evo_name, pkmn_name in tests:
    n1 = _norm(evo_name)
    n2 = _norm(pkmn_name)
    match = "MATCH" if n1 == n2 else "MISMATCH"
    print(f"{evo_name:15s} -> {n1:12s} vs {pkmn_name:15s} -> {n2:12s} [{match}]")

# Now test with app module
import app

print("\n--- evolution_map keys for mime/rime ---")
for key in sorted(app.evolution_map.keys()):
    if "mime" in key[0] or "mime" in key[1]:
        print(f"  {key}")
        for evo in app.evolution_map[key]:
            print(f"    -> {dict(evo)}")

print("\n--- pokemon_data keys for mime/rime ---")
for k, v in app.pokemon_data.items():
    if "mime" in k.lower() or "rime" in k.lower():
        print(f"  {k!r} -> name={v['name']!r}, form={v.get('form','')!r}")

print("\n--- get_name_key tests ---")
print(f"  get_name_key('MRMIME') = {app.get_name_key('MRMIME')!r}")
print(f"  get_name_key('MRRIME') = {app.get_name_key('MRRIME')!r}")
print(f"  get_name_key('MR.RIME') = {app.get_name_key('MR.RIME')!r}")

# Check the current caught list
print("\n--- caught.json ---")
try:
    with open(r"C:\Games\Pokemon\Random Optimizer\caught.json", "r") as f:
        caught = json.load(f)
    for c in caught:
        print(f"  {c}")
except Exception as e:
    print(f"  Error: {e}")
