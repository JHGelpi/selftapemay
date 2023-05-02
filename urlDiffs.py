import csv

gcpFile = 'gcpInstagramExport.csv'
newFile = 'videoOutput.csv'
output = 'diffs.csv'

# Windows filepath
folderLocation = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'

# Mac filepath
#folderLocation = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/'

# read in the data from gcpFile
with open(folderLocation + gcpFile, newline='') as f:
    reader = csv.DictReader(f)
    data1 = set([row['url'] for row in reader])

# compare data from newFile to data from gcpFile
with open(folderLocation + newFile, newline='') as f, open(folderLocation + output, 'w', newline='') as out:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        if row['url'] not in data1:
            writer.writerow(row)
