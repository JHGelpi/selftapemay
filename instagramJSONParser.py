import json
import csv
import chardet
# from datetime import datetime

# This is the file name for the initial input file downloaded from Apify
# it needs to match exactly the file.

# input_file = 'exampleJSON.json'
input_file = 'dataset_instagram-api-scraper.json'
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
    writer.writerow(['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType', 'childPostVid'])
    # Write data rows
    for d in data:
        if d['username'] != 'Restricted profile':
            latest_posts = d['latestPosts']
            print(latest_posts)
            full_name = d['fullName']
            #*********************************
            # loop through the latestPosts and childPosts and print their ids
            childPostVid = ''
            for i in range(len(data)):
                if 'latestPosts' in data[i]:
                    for post in data[i]['latestPosts']:
                        if data[i]['id'] == '3097962891307534033':
                            print("stop here!")
                        #print(f"Post ID: {post['id']}")
                        for child_post in post['childPosts']:
                            if child_post['type'] == 'Video':
                                #print(f"\tChild Post ID: {child_post['id']}")
                                #print(f"\tChild Post ID: {child_post['type']}")
                                childPostVid = 'Y'
                                break
            #*********************************
            for post in latest_posts: 
                #*********************************
                if childPostVid == 'Y':
                    postType = 'Video'
                else:
                    postType = post.get('type', '')  
                #*********************************
                row = [post.get('id', ''), post.get('fullName', ''),post.get('ownerUsername', ''), postType, post.get('url', ''), post.get('hashtags', ''), post.get('timestamp', ''), post.get('productType', ''), childPostVid]
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