import json
import chardet

# file names
input_file = 'dataset_instagram-api-scraper_kaytra.json'
output_file = 'jsonChildPostsOutput.csv'

# Windows filepath
file_path = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'

# Mac filepath
#file_path = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/'

# Determine encoding
def determine_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Determine the encoding type of the csv file
encoding = determine_encoding(file_path + input_file)

# Load the JSON file
with open(file_path + input_file, 'r', encoding=encoding) as f:
    data = json.load(f)

# Extract the data from the third level
for post in data[0]["latestPosts"]:
    for child_post in post["childPosts"]:
        print(child_post["id"])
        print(child_post["type"])
        print("-------------")