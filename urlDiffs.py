import csv

file1 = 'file1.csv'
file2 = 'file2.csv'
output = 'diffs.csv'

# read in the data from file1
with open(file1, newline='') as f:
    reader = csv.DictReader(f)
    data1 = set([row['url'] for row in reader])

# compare data from file2 to data from file1
with open(file2, newline='') as f, open(output, 'w', newline='') as out:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        if row['url'] not in data1:
            writer.writerow(row)
