import pandas as pd

# This is the file name for the initial input file downloaded from Apify
# it needs to match exactly the file.

# input_file = 'exampleJSON.json'
input_file = 'dataset_instagram-api-scraper_2023-04-26_21-46-52-430.json'
output_file = 'jsonOutput.csv'

# This is the folder path where the Apify export file resides as well
# as the location of where the output csv will be
# file_path = 'D:\\consulting\\AudreyHelpsActors\\'
file_path = 'D:\\Nextcloud\\Consulting\\selfTapeMay\\'

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv(file_path + input_file)

# Iterate through each row of the DataFrame
for index, row in df.iterrows():

    # Extract the hashtag column as a string
    hashtags = str(row['hashtags'])

    # Remove the square brackets and single quotes from the string
    hashtags = hashtags.replace('[', '').replace(']', '').replace("'", '')

    # Split the string into a list of individual tags
    tags = hashtags.split(', ')

    # Print each tag to the console
    for tag in tags:
        print(tag)
