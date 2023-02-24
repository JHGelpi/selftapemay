# Data cleansing for apify data import
# Code writing assisted by ChatGPT :-)
import csv
import chardet
from datetime import datetime

# init variables
# This is the date format for the data downloaded from Apify
# It is used to convert the text string into a true date value before exporting to CSV
date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

# This is the start date for the timeframe that you are performing the data
# clean-up for.  The format is (yyyy,m,d,h,m,s)

# This variable WILL needed to be updated each year
start_dttm = datetime(2022,5,1,0,0,0,1)

# This is the end date for the timeframe you are performing the data
# clean-up for.  The format is (yyyy,m,d,h,m,s)

# This variable WILL needed to be updated each year
end_dttm = datetime(2022,5,31,23,59,59)

# This variable is used to return whether the user used the proper
# hashtag to qualify/be counted toward the campaign (e.g. in 2022 the campaign
# was The Witcher)
camp_elig = False

# This is the file name for the initial input file downloaded from Apify
# it needs to match exactly the file.
input_file = 'inputstm2022.csv'

# This is the folder path where the Apify export file resides as well
# as the location of where the output csv will be
file_path = 'D:\\consulting\\AudreyHelpsActors\\'

# This is the full path of the output file
output_csv = file_path + 'output.csv'

# This is the full path of the input file
input_csv = file_path + input_file

# Determine encoding
def determine_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Before the csv file is imported for manipulation 
# add a column to the file at the end.  This column
# is intended to store a Y/N flag for if the user participated
# in a particular campaign during Self Tape May.  For example:
# in 2022 the campaign was "Witcher sides".  If the user leveraged 
# a hashtag mentioning The Witcher they should have a 'Y' in this column
def add_campaign_col(in_file, encoding):

    # Open the CSV file for reading
    with open(in_file, 'r', encoding=encoding) as file:

        # Read the contents of the CSV file into a list of rows
        reader = csv.reader(file)
        rows = list(reader)

    # Add a header for the new column to the first row
    rows[0].append('campaignFlag')

    # Open the CSV file for writing
    with open(in_file, 'w', newline='', encoding=encoding) as file:

        # Write the updated list of rows to the CSV file
        writer = csv.writer(file)
        writer.writerows(rows)

    return

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

# Determine the encoding type of the csv file
encoding = determine_encoding(input_csv)

# Add the 'campaignFlag' to the source CSV file
add_campaign_col(input_csv, encoding)

# List of column names to keep
columns_to_keep = ['id','locationName','ownerFullName','ownerUsername','timestamp', 'type', 'videoDuration', 'campaignFlag']

# Read the input CSV file
with open(input_csv, 'r', encoding=encoding) as input_file:
    reader = csv.DictReader(input_file)

    hash_columns = hashtag_columns(reader)

    # Write the output CSV file
    with open(output_csv, 'w', newline='', encoding=encoding) as output_file:
        columns_to_write = columns_to_keep

        writer = csv.DictWriter(output_file, fieldnames=columns_to_write)

        # Write the header row
        writer.writeheader()

        # Write the data rows, keeping only the specified columns
        for row in reader:
            # Read in the row of data to output
            output_row = {key: row[key] for key in columns_to_keep}
            
            # Call the campaign check function to see if users participated in the campaign
            camp_check = campaign_check(hash_columns, output_row['ownerUsername'], {key: row[key] for key in hash_columns})

            # Add the '@' symbol to the IG handle to match user profile data
            # at selftapemay.com
            output_row['ownerUsername'] = '@' + output_row['ownerUsername']

            # Based on the results returned from campaign_check set the value accordingly
            if camp_check:
                output_row['campaignFlag'] = 'Y'
            else:
                output_row['campaignFlag'] = 'N'

            # Convert date/time string to formatted date/time stamp
            if output_row['timestamp'] != '':
                date_string = output_row['timestamp']
                dt = datetime.strptime(date_string, date_format)
                output_row['timestamp'] = dt

            # Write out data to CSV file
            if start_dttm <= dt <= end_dttm and output_row['type'] == 'Video':
                writer.writerow(output_row)
