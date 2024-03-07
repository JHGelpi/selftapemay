# data_processor.py

# Functions to process the raw data from Apify.
# Filter posts by video/reel type, date range, and check for duplicates.
# Tasks left to do:
    # - Filter out posts that were already uploaded to BigQuery

import csv
import ast
from datetime import datetime
from google.cloud import bigquery

def process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag):
    output_file_path = input_file_path.replace("scrape_results", "processed_results")
    
    # Step 1: Process and filter the initial CSV
    temp_output_path = input_file_path.replace("scrape_results", "temp_processed_results")
    final_output_path = input_file_path.replace("scrape_results", "final_processed_results")

    with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(temp_output_path, mode='w', newline='', encoding='utf-8') as temp_outfile:
         #open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['selftapemayFlag', 'campaignFlag']  # Add new columns
        
        temp_writer = csv.DictWriter(temp_outfile, fieldnames=fieldnames)
        temp_writer.writeheader()
        #writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        #writer.writeheader()

        for row in reader:
            # Initialize flags as False
            row['selftapemayFlag'] = False
            row['campaignFlag'] = False

            # Convert the string representation of the list back to a list

            try:
                hashtags = ast.literal_eval(row['hashtags'])
            except (ValueError, SyntaxError):
                hashtags = []  # Fallback to an empty list in case of a parsing error
            
            # Check if 'selftapemay' is in hashtags
            if selftapemay_hashtag in hashtags:
                row['selftapemayFlag'] = True

            # Check for the campaign hashtag
            if campaign_hashtag in hashtags:
                row['campaignFlag'] = True

            if row['selftapemayFlag']:
                temp_writer.writerow(row)
            #writer.writerow(row)
    
    # Step 2: Download BigQuery data - Handled outside this script or by a separate function
    # Initialize the BigQuery client
    client = bigquery.Client()

    def get_posts():
        # Function to retrieve user data from BigQuery
        # Retrieve user data from the BigQuery table.
        query = """
            SELECT * FROM `self-tape-may.self_tape_may_data.tblInstagramData`
        """
        query_job = client.query(query)  # Make an API request.
        
        try:
            posts = query_job.result()  # Waits for the query to finish
            return posts
        except Exception as e:
            print("Error in get_users:", e)
            return None

    posts = get_posts()
    
    # Step 3: Compare and generate diffs
    bq_data_path = 'path_to_downloaded_BigQuery_data.csv'  # Set this to your downloaded BigQuery data path
    diffs_output_path = f"instagram_diffs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    
    existing_ids = set()
    with open(bq_data_path, mode='r', newline='', encoding='utf-8') as bq_file:
        bq_reader = csv.DictReader(bq_file)
        for row in bq_reader:
            existing_ids.add(row['id'])
    
    with open(temp_output_path, mode='r', newline='', encoding='utf-8') as temp_infile, \
         open(diffs_output_path, mode='w', newline='', encoding='utf-8') as diffs_outfile:
        reader = csv.DictReader(temp_infile)
        writer = csv.DictWriter(diffs_outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            if row['id'] not in existing_ids:
                writer.writerow(row)

    # Step 4: Append new data to BigQuery - Handled outside this script or by a separate function

    return diffs_output_path
    #return output_file_path
'''
# Example usage
selftapemay_hashtag = 'selftapemay'
campaign_hashtag = 'asmr'  # Replace with your actual campaign hashtag
#processed_file_path = process_csv(csv_file_path, campaign_hashtag)
input_file_path = '/home/wesgelpi/Downloads/instagram_scrape_results_2024-03-04_21-28-23.csv'  # Update the path

processed_file_path = process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag)
print(f"Processed file saved as: {processed_file_path}")
'''