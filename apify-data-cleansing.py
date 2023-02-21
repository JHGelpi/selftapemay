# Data cleansing for apify data import
# Code writing assisted by ChatGPT :-)
import csv
import chardet
from datetime import datetime

# init variables
date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
start_dttm = datetime(2022,5,1,0,0,0,1)
end_dttm = datetime(2022,5,31,23,59,59)
camp_elig = False

# Determine encoding
def determine_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Identify the columns in the csv file that include the word
# `hashtag` in their name.  This will be the starting point for me to
# loop through the `hashtag` columns to see if they used the campaign
# hashtag (e.g. `thewitcher`).

def hashtag_columns(csv_reader):
    header_row = next(csv_reader)
    all_cols = []
    search_string = "hashtag"
    hashtag_cols = ['ownerUsername']

    # Identify all the headers
    for header in header_row:
        all_cols.append(header)

    # Figure out which headers start with `hashtag` and create a list
    # Be sure to make the first list value 'ownerUsername'

    for header in all_cols:
        if search_string in header:
            hashtag_cols.append(header)
            #print("Match found: {}".format(header))

    #print(hashtag_cols)
    return hashtag_cols

# List of column names to keep
columns_to_keep = ['id','locationName','ownerFullName','ownerUsername','timestamp', 'type', 'videoDuration']

# CSV files
input_file = 'inputstm2022.csv'
#input_file = 'dataset_instagram-hashtag-scraper_2023-01-17_02-48-20-006.csv'

file_path = 'D:\\consulting\\AudreyHelpsActors\\'

output_csv = file_path + 'output.csv'

input_csv = file_path + input_file

encoding = determine_encoding(input_csv)

# Read the input CSV file
with open(input_csv, 'r', encoding=encoding) as input_file:
    reader = csv.DictReader(input_file)

    hashtag_columns = hashtag_columns(reader)

    # Write the output CSV file
    with open(output_csv, 'w', newline='', encoding=encoding) as output_file:

        writer = csv.DictWriter(output_file, fieldnames=columns_to_keep)

        # Write the header row
        writer.writeheader()

        # Write the data rows, keeping only the specified columns
        for row in reader:
            # Read in the row of data to output
            output_row = {key: row[key] for key in columns_to_keep}

            # Add the '@' symbol to the IG handle to match user profile data
            # at selftapemay.com

            output_row['ownerUsername'] = '@' + output_row['ownerUsername']

            # Convert date/time string to formatted date/time stamp
            if output_row['timestamp'] != '':
                date_string = output_row['timestamp']
                #date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                dt = datetime.strptime(date_string, date_format)
                output_row['timestamp'] = dt

            # Write out data to CSV file
            if start_dttm <= dt <= end_dttm and output_row['type'] == 'Video':
                writer.writerow(output_row)
