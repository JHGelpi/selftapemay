# data_processor.py

# Functions to process the raw data from Apify.
# Filter posts by video/reel type, date range, and check for duplicates.
# Tasks left to do:
    # - Filter out posts that were already uploaded to BigQuery

import csv
import ast
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

def process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag):
    # Step 1: Load and filter the initial CSV
    df = pd.read_csv(input_file_path)

    # Safely evaluate the hashtags column, accounting for NaN values
    safe_eval = lambda x: ast.literal_eval(x) if pd.notna(x) else []
    df['hashtags_list'] = df['hashtags'].apply(safe_eval)

    # Filter based on selftapemay_hashtag and campaign_hashtag
    df['selftapemayFlag'] = df['hashtags_list'].apply(lambda x: selftapemay_hashtag in x)
    df['campaignFlag'] = df['hashtags_list'].apply(lambda x: campaign_hashtag in x)
    filtered_df = df[df['selftapemayFlag']]

    # Step 2: Download BigQuery data and convert to DataFrame
    client = bigquery.Client()
    query = "SELECT * FROM `self-tape-may.self_tape_may_data.tblInstagramData`"
    bq_df = client.query(query).to_dataframe()

    # Step 3: Compare and generate diffs
    existing_ids = set(bq_df['id'])
    diffs_df = filtered_df[~filtered_df['id'].isin(existing_ids)]

    # Save diffs to CSV
    formatted_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    diffs_output_path = f"/home/wesgelpi/Downloads/instagram_diffs_{formatted_now}.csv"
    diffs_df.to_csv(diffs_output_path, index=False)
    print(f"Diffs file saved as: {diffs_output_path}")

    dataset_table = 'self-tape-may.self_tape_may_data.tblInstagramData'  # Specify your dataset and table
    append_to_bigquery(diffs_output_path, dataset_table)
    
    return diffs_output_path

# Step 4: Append new data to BigQuery is handled outside this script
def append_to_bigquery(csv_file_path, dataset_table):
    client = bigquery.Client()
    table_id = dataset_table

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip the header row.
        autodetect=True,  # Autodetect schema and options.
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND)  # Append to existing table.

    with open(csv_file_path, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    load_job.result()  # Wait for the job to complete.

    print(f"Appended data to {table_id} from {csv_file_path}. Job ID: {load_job.job_id}")

'''
# Example usage
selftapemay_hashtag = 'selftapemay'
campaign_hashtag = 'asmr'  # Replace with your actual campaign hashtag
#processed_file_path = process_csv(csv_file_path, campaign_hashtag)
input_file_path = '/home/wesgelpi/Downloads/instagram_scrape_results_2024-03-04_21-28-23.csv'  # Update the path

processed_file_path = process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag)
print(f"Processed file saved as: {processed_file_path}")
'''