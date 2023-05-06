import json
import csv
import chardet
# from datetime import datetime

# This is the file name for the initial input file downloaded from Apify
# it needs to match exactly the file.

# input_file = 'exampleJSON.json'
input_file = 'dataset_instagram-api-scraper_2023-05-05_20-49-35-239.json'
output_file = 'jsonOutput.csv'

# This is the folder path where the Apify export file resides as well
# as the location of where the output csv will be

# Windows filepath
file_path = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'

# Mac filepath
#file_path = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/'

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
    writer.writerow(['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType'])
    # Write data rows
    for d in data:
        if d['username'] != 'Restricted profile':
            latest_posts = d['latestPosts']
            full_name = d['fullName']
            for post in latest_posts:
                row = [post.get('id', ''), post.get('fullName', ''),post.get('ownerUsername', ''), post.get('type', ''), post.get('url', ''), post.get('hashtags', ''), post.get('timestamp', ''), post.get('productType', '')]
                writer.writerow(row)
'''
# Write data to CSV file
with open(file_path + output_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # Write header row
    writer.writerow(['ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType'])
    # Write data rows
    for post in latest_posts:
        row = [post['ownerUsername'], post['type'], post['url'], post['hashtags'], post['timestamp'], post['productType']]
        writer.writerow(row)
'''