import json
import csv
import chardet
import shutil
import glob
import os

# This is the folder path where the Apify export file resides as well
# as the location of where the output csv will be

# Windows filepath
file_path = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'
archiveFilePath = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\apifyRunData\\'

# Mac filepath
#file_path = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/'

# This is the file name for the initial input file downloaded from Apify
# it needs to match exactly the file.

input_file = ''
files = glob.glob(file_path + "dataset_instagram-api-scraper_*.json")

for file in files:
    input_file = os.path.basename(file)

output_file = 'jsonOutput.csv'

# Determine encoding
def determine_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Load JSON data from a file
# Determine the encoding type of the csv file
encoding = determine_encoding(file_path + input_file)

with open(file_path + input_file, 'r', encoding=encoding) as f:
    data = json.load(f)

# Write data to CSV file
with open(file_path + output_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # Write header row
    writer.writerow(['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType', 'childPostVid'])
    # Write data rows
    childPostVid = ''
    for d in data:
        if d['username'] != 'Restricted profile':
            for i in d['latestPosts']:
                if i['type'] == 'Video':
                    childPostVid = 'Y'
                    postType = 'Video'
                    #row = [post.get('id', ''), post.get('fullName', ''),post.get('ownerUsername', ''), postType, post.get('url', ''), post.get('hashtags', ''), post.get('timestamp', ''), post.get('productType', ''), childPostVid]
                    #row = [d.get('id', ''), d.get('fullName', ''),d.get('ownerUsername', ''), postType, d.get('url', ''), d.get('hashtags', ''), d.get('timestamp', ''), d.get('productType', ''), childPostVid]
                    row = [i.get('id', ''), d.get('fullName', ''),i.get('ownerUsername', ''), postType, i.get('url', ''), i.get('hashtags', ''), i.get('timestamp', ''), i.get('productType', ''), childPostVid]
                    writer.writerow(row)
                elif len(i['childPosts']) > 0:
                    for l in i['childPosts']:
                        if l['type'] == 'Video':
                            childPostVid = 'Y'
                            postType = 'Video'
                            row = [l.get('id', ''), d.get('fullName', ''),i.get('ownerUsername', ''), postType, l.get('url', ''), i.get('hashtags', ''), i.get('timestamp', ''), i.get('productType', ''), childPostVid]
                            writer.writerow(row)
                            #break
                        else:
                            childPostVid = 'N'
                else:
                    childPostVid = 'N'

# move the file to the archive folder
shutil.move(file_path + input_file, archiveFilePath)
