import json

# file names
input_file = 'dataset_instagram-api-scraper_kaytra.json'
output_file = 'jsonChildPostsOutput.csv'

# Windows filepath
file_path = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'

# Mac filepath
#file_path = '/Users/wegelpi/Nextcloud/Consulting/selfTapeMay/'

# Load the JSON file
with open(file_path + input_file) as f:
    data = json.load(f)

# Extract the data from the third level
child_posts = data['latestPosts']['0']['childPosts']

# Print the extracted data
print(child_posts)

