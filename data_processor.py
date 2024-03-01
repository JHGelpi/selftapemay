# data_processor.py

# Functions to process the raw data from Apify.
# Filter posts by video/reel type, date range, and check for duplicates.
# Use Pandas for efficient data processing.

import csv

def process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag):
    output_file_path = input_file_path.replace("scrape_results", "processed_results")

    with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['selftapemayFlag', 'campaignFlag']  # Add new columns

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Initialize flags as False
            row['selftapemayFlag'] = False
            row['campaignFlag'] = False

            # Convert the string representation of the list back to a list
            hashtags = eval(row['hashtags'])

            # Check if 'selftapemay' is in hashtags
            if selftapemay_hashtag in hashtags:
                row['selftapemayFlag'] = True

            # Check for the campaign hashtag
            if campaign_hashtag in hashtags:
                row['campaignFlag'] = True

            writer.writerow(row)

    return output_file_path

# Example usage
#selftapemay_hashtag = 'selftapemay'
#campaign_hashtag = 'asmr'  # Replace with your actual campaign hashtag
#processed_file_path = process_csv(csv_file_path, campaign_hashtag)
#input_file_path = '/home/wesgelpi/Downloads/instagram_scrape_results_2024-02-29_22-28-54.csv'  # Update the path

#processed_file_path = process_csv(input_file_path, campaign_hashtag)
#print(f"Processed file saved as: {processed_file_path}")
