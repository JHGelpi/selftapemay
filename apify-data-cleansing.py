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

# Determine campaign eligibility

def camp_eligible(input_file, reader, username):
    elig_hashtag = "workingactress"
    column_list = ['ownerUsername']
    # ***********************************
    # Loop through columns to find columns that start with hashtag
    # ***********************************

    # Loop through all of the hashtag columns
    # This will be used to figure out if people have used specific
    # hashtags in their post.  This will be used for campaign tracking
    # (e.g. "Was your self tape a scene from The Witcher?")

    reader_col = csv.reader(input_file)

    # Loop through each row in the CSV file
    for row in reader_col:

        # Loop through each column in the row
        for column in enumerate(row):

            # Check if the column starts with 'hashtag'
            if column.startswith('hashtag'):
                column_list.append(column)

            print(column_list)
        #if i > 0:
            ## Check to see if elig_hashtag is present in any of the 
            ## identified hashtag columns
            #for row in reader:
                #output_row = {key: row[key] for key in column_list}

                ## Loop through the output_row dict
                ## to check for the hashtag stored in elig_hashtag

                #for value in output_row.items():
                #    if value == elig_hashtag:
                #        return True
                
            # If we get through the entire data set w/out matching
            # on the elig_hashtag value then we return a False

            return False

    # ***********************************
    # End loop code
    # ***********************************

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

    # Write the output CSV file
    with open(output_csv, 'w', newline='', encoding=encoding) as output_file:

        writer = csv.DictWriter(output_file, fieldnames=columns_to_keep)

        # Write the header row
        writer.writeheader()

        # Write the data rows, keeping only the specified columns
        for row in reader:
            # Read in the row of data to output
            output_row = {key: row[key] for key in columns_to_keep}

            # Determine if each row in the file has participated
            # In the determined campaign

            camp_elig = camp_eligible(input_file, reader, output_row['ownerUsername'])

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
