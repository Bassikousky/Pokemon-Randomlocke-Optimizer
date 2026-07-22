import re

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

names = set(re.findall(r"'name':\s*'([^']+)'", content))
print('Pokemon in data.js:', len(names))

checks = ['Charizard|Mega Charizard X', 'Charizard|Mega Charizard Y',
          'Wormadam|Sandy Cloak', 'Castform|Sunny Form',
          'Wormadam|Trash Cloak', 'Castform|Rainy Form', 'Castform|Snowy Form']

for search in checks:
    esc = re.escape(search)
    if re.search(esc, content):
        print('  FOUND: ' + search)
    else:
        print('  NOT FOUND: ' + search)

# Check types for Wormadam forms
for form in ['Sandy Cloak', 'Trash Cloak']:
    # Find the entry for Wormadam with this form
    pattern = r"'Wormadam\|" + re.escape(form) + r"'\s*:\s*\{[^}]*'type1':\s*'([^']+)'[^}]*'type2':\s*'([^']+)'"
    m = re.search(pattern, content)
    if m:
        print('Wormadam|' + form + ': ' + m.group(1) + '/' + m.group(2))

for form in ['Sunny Form', 'Rainy Form', 'Snowy Form']:
    pattern = r"'Castform\|" + re.escape(form) + r"'\s*:\s*\{[^}]*'type1':\s*'([^']+)'[^}]*'type2':\s*'([^']+)'"
    m = re.search(pattern, content)
    if m:
        print('Castform|' + form + ': ' + m.group(1) + '/' + m.group(2))
