import csv

targets = ['Oricorio', 'Wormadam', 'Deoxys', 'Rotom', 'Darmanitan', 'Castform', 'Farfetch\'d']
with open('Pokemon.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1] in targets:
            form = row[2]
            t1, t2 = row[3], row[4]
            print('%s | Form="%s" | %s/%s' % (row[1], form, t1, t2))
