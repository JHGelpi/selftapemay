import json
import csv
import chardet
import shutil
import glob
import os
import datetime

now = datetime.datetime.now()
print(now, ": Executing...")

# This is the folder path where the Apify export file resides as well
# as the location of where the output csv will be

# Windows filepath
file_path = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'
#archiveFilePath = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\apifyRunData\\'
archiveFilePath = file_path + 'apifyRunData\\'

# Mac filepath
#file_path = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/'
#archiveFilePath = file_path + 'apifyRunData/'

# This is the file name for the initial input file downloaded from Apify
# it needs to match exactly the file.
input_file = ''
files = glob.glob(file_path + "dataset_instagram-api-scraper_*.json")

for file in files:
    input_file = os.path.basename(file)

output_file = 'jsonHashtagOutput.csv'

# Determine encoding
def determine_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.UniversalDetector()
        for chunk in iter(lambda: file.read(8192), b''):
            detector.feed(chunk)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

# Load JSON data from a file
# Determine the encoding type of the csv file
now = datetime.datetime.now()
print(now, ": Determining encoding...")
encoding = determine_encoding(file_path + input_file)
now = datetime.datetime.now()
print(now, ": Done with encoding...")

now = datetime.datetime.now()
print(now, ": Loading file...")
with open(file_path + input_file, 'r', encoding=encoding) as f:
    data = json.load(f)
now = datetime.datetime.now()
print(now, ": Analyzing JSON and writing to CSV...")

# Write data to CSV file
with open(file_path + output_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # Write header row
    writer.writerow(['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'postType', 'childPostVid'])
    # Write data rows
    childPostVid = ''
    for d in data:
        if 'ownerUsername' in d:
            if d['type'] == 'Sidecar':
                for e in d['childPosts']:
                    if e['type'] == 'Video':
                        row = [e.get('id', ''), d.get('fullName', ''),d.get('ownerUsername', ''), 'Sidecar', e.get('url', ''), d.get('hashtags', ''), d.get('timestamp', ''), e.get('type', ''), childPostVid]
                        writer.writerow(row)
            elif d['type'] == 'Video':
                row = [d.get('id', ''), d.get('fullName', ''),d.get('ownerUsername', ''), d.get('type', ''), d.get('url', ''), d.get('hashtags', ''), d.get('timestamp', ''), d.get('type', ''), childPostVid]
                writer.writerow(row)
now = datetime.datetime.now()
print(now, ": Archiving JSON file...")
# move the file to the archive folder
shutil.move(file_path + input_file, archiveFilePath)

now = datetime.datetime.now()
print(now, ": Done...")