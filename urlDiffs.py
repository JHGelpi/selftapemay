import csv
import chardet

gcpFile = 'gcpInstagramExport.csv'
newFile = 'videoOutput.csv'
output = 'diffs.csv'

# Windows filepath
folderLocation = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'

# Mac filepath
#folderLocation = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/'

# Determine encoding
def determine_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Determine the encoding type of the csv file
encoding = determine_encoding(folderLocation + gcpFile)

# read in the data from gcpFile
with open(folderLocation + gcpFile, newline='', encoding=encoding) as f:
    reader = csv.DictReader(f)
    data1 = set([row['url'] for row in reader])

# Determine the encoding type of the csv file
encoding = determine_encoding(folderLocation + newFile)

# compare data from newFile to data from gcpFile
with open(folderLocation + newFile, newline='', encoding=encoding) as f, open(folderLocation + output, 'w', newline='', encoding='utf-8') as out:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        if row['url'] not in data1:
            writer.writerow(row)
