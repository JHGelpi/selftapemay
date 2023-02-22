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

# Before the csv file is imported for manipulation 
# add a column to the file at the end.
def add_campaign_col(in_file):
    #import csv

    # Open the CSV file for reading
    with open('my_csv_file.csv', 'r') as file:

        # Read the contents of the CSV file into a list of rows
        reader = csv.reader(file)
        rows = list(reader)

    # Add a header for the new column to the first row
    rows[0].append('New Column')

    ## Iterate through each row and append the value for the new column
    #for row in rows[1:]:
        ## Replace 'new_value' with the value you want to add to the new column
        #row.append('new_value')

    # Open the CSV file for writing
    with open('my_csv_file.csv', 'w', newline='') as file:

        # Write the updated list of rows to the CSV file
        writer = csv.writer(file)
        writer.writerows(rows)

    return False

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

    return hashtag_cols

# Loop through every column that has the `hashtag` in its name
# and see if the campaign hashtag(s) were mentioned
def campaign_check(columns, userName, dataRow):

    # This variable identifies the campaign hashtag.
    # Current assumption is there will only be one campaign hashtag
    # at a time.
    camp_hashtag = "audreyhelpsactors"

    # Loop through all of the items in this dictionary
    # and check to see if the user leveraged the campaign hashtag
    # If they did use it than the function should return a 'True' value.  Otherwise
    # the function should return a 'False' value.
    for key, value in dataRow.items():
        if value == camp_hashtag:
            return True

    return False

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

    hash_columns = hashtag_columns(reader)

    # Write the output CSV file
    with open(output_csv, 'w', newline='', encoding=encoding) as output_file:
        columns_to_write = columns_to_keep
        #columns_to_write.append('campaignFlag')

        writer = csv.DictWriter(output_file, fieldnames=columns_to_write)

        # Write the header row
        writer.writeheader()

        # Write the data rows, keeping only the specified columns
        for row in reader:
            # Read in the row of data to output
            output_row = {key: row[key] for key in columns_to_keep}

            camp_check = campaign_check(hash_columns, output_row['ownerUsername'], {key: row[key] for key in hash_columns})

            # Add the '@' symbol to the IG handle to match user profile data
            # at selftapemay.com
            output_row['ownerUsername'] = '@' + output_row['ownerUsername']

            # -------------------------------
            # OUTSTANDING ITEM
            # I still need to figure out how to add the boolean flag to an
            # added column called 'campaignFlag'.  I cannot seem to get this to work
            # just yet.
            # -------------------------------
            if camp_check:
                output_row['campaignFlag'] = 'Y'
            #else:
            #    output_row['campaignFlag'] = 'N'

            # Convert date/time string to formatted date/time stamp
            if output_row['timestamp'] != '':
                date_string = output_row['timestamp']
                #date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                dt = datetime.strptime(date_string, date_format)
                output_row['timestamp'] = dt

            # Write out data to CSV file
            if start_dttm <= dt <= end_dttm and output_row['type'] == 'Video':
                writer.writerow(output_row)
