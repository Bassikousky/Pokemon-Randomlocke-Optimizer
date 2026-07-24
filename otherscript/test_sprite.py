def build_sprite_name(name, form=""):
    base = name.lower().replace(" ", "-").replace(".", "").replace("'", "").replace("\u2640", "-f").replace("\u2642", "-m")
    f = form.strip() if form else ""
    if not f or f == " ":
        return base
    f_lower = f.lower()
    if f_lower.startswith("alolan "):
        return base + "-alola"
    if f_lower.startswith("galarian "):
        return base + "-galar"
    if f_lower.startswith("hisuian "):
        return base + "-hisui"
    if f_lower.startswith("mega "):
        return base + ("-mega-z" if f_lower.rstrip().endswith(" z") else "-mega")
    if f_lower.startswith("gmax ") or f_lower.startswith("gigantamax "):
        return base + "-gmax"
    sprite_suffixes = {
        "oricorio": {"baile style": "-baile", "pom-pom style": "-pom-pom", "pa'u style": "-pau", "sensu style": "-sensu"},
        "wormadam": {"plant cloak": "-plant", "sandy cloak": "-sandy", "trash cloak": "-trash"},
        "deoxys": {"normal forme": "-normal", "attack forme": "-attack", "defense forme": "-defense", "speed forme": "-speed"},
        "rotom": {"heat rotom": "-heat", "wash rotom": "-wash", "frost rotom": "-frost", "fan rotom": "-fan", "mow rotom": "-mow"},
        "castform": {"sunny form": "-sunny", "rainy form": "-rainy", "snowy form": "-snowy"},
        "darmanitan": {"standard mode": "-standard", "zen mode": "-zen", "galarian standard mode": "-galar-standard", "galarian zen mode": "-galar-zen"},
    }
    forms = sprite_suffixes.get(base)
    if forms and f_lower in forms:
        return base + forms[f_lower]
    return base

tests = [
    ("Venusaur", "Mega Venusaur"),
    ("Venusaur", "Mega Venusaur X"),
    ("Venusaur", "Mega Venusaur Y"),
    ("Charizard", "Mega Charizard X"),
    ("Charizard", "Mega Charizard Y"),
    ("Absol", "Mega Absol Z"),
    ("Garchomp", "Mega Garchomp Z"),
    ("Lucario", "Mega Lucario Z"),
    ("Kingler", "Mega Kingler"),
    ("Gengar", "Mega Gengar Y"),
    ("Farfetch'd", "Galarian Farfetch'd"),
    ("Farfetch'd", ""),
    ("Rotom", "Heat Rotom"),
    ("Oricorio", "Baile Style"),
    ("Charizard", "Gmax Charizard"),
    ("Eevee", "Gigantamax Eevee"),
]
for name, form in tests:
    print("%-20s | %-25s -> %s" % (name, form, build_sprite_name(name, form)))
