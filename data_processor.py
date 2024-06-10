"""
data_processor.py

Functions to process the raw data from Apify. Filter posts by video/reel type, date range, and check for duplicates.
"""

import csv
import ast
import pandas as pd
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
from datetime import datetime
import pytz

def parse_date(date_str):
    """
    Parse the date string to a datetime object with UTC timezone.

    Args:
        date_str (str): Date string to parse.

    Returns:
        datetime: Parsed datetime object with UTC timezone.
    """
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)

def process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag):
    """
    Process the input CSV file, filter the data, and save the differences to a new CSV file.

    Args:
        input_file_path (str): Path to the input CSV file.
        selftapemay_hashtag (list): List of hashtags for self-tape may campaign.
        campaign_hashtag (list): List of hashtags for the specific campaign.

    Returns:
        str: Path to the CSV file containing the differences.
    """
    # Initialize an empty DataFrame for diffs_df with the same columns as in your CSV
    diffs_df = pd.DataFrame(columns=['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType', 'hashtag_0', 'hashtag_1', 'campaignFlag', '_id', '_createdDate', '_updatedDate', '_owner'])

    # Step 1: Load and filter the initial CSV
    df = pd.read_csv(input_file_path)

    # Ensure the DataFrame includes all necessary columns, even if they are initially empty
    for column in ['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType', 'hashtag_0', 'hashtag_1', 'campaignFlag', '_id', '_createdDate', '_updatedDate', '_owner']:
        if column not in df.columns:
            df[column] = pd.NA  # Assign a missing value placeholder

    # Filter to only include rows where 'type' is 'Video'
    df = df[df['type'] == 'Video']

    # Safely evaluate the hashtags column, accounting for NaN values
    def safe_eval(x):
        try:
            return ast.literal_eval(x) if pd.notna(x) else []
        except (ValueError, SyntaxError):
            return []
    
    df['hashtags_list'] = df['hashtags'].apply(safe_eval)

    # Convert 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Define start and end of the date range
    utc = pytz.UTC
    start_end_date_file = '/home/wesgelpi/self_tape_may/start_end_dates.txt'
    with open(start_end_date_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "start_date:" in line:
            start_date_str = line.split(": ")[1].strip()  # Extract the date string
            start_date = parse_date(start_date_str)
        elif "end_date:" in line:
            end_date_str = line.split(": ")[1].strip()  # Extract the date string
            end_date = parse_date(end_date_str)

    # Filter df for posts within the specified date range
    filtered_df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]

    # Filter based on selftapemay_hashtag and campaign_hashtag
    filtered_df.loc[:, 'selftapemayFlag'] = filtered_df['hashtags_list'].apply(
        lambda x: any(hashtag.lower() in map(str.lower, x) for hashtag in selftapemay_hashtag)
    )
    filtered_df.loc[:, 'campaignFlag'] = filtered_df['hashtags_list'].apply(
        lambda x: any(campaign.lower() in map(str.lower, x) for campaign in campaign_hashtag)
    )

    filtered_df = filtered_df[filtered_df['selftapemayFlag']]

    # Export to CSV file - This is a validation step that should be omitted from final solution
    formatted_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    bigquery_output_path = f"/home/wesgelpi/Downloads/instagram_filteredresults_{formatted_now}.csv"
    filtered_df.to_csv(bigquery_output_path, index=False)

    # Step 2: Download BigQuery data and convert to DataFrame
    project_id = 'self-tape-may'
    client = bigquery.Client(project=project_id)
    query = "SELECT * FROM `self-tape-may.self_tape_may_data.tblInstagramData`"
    bq_df = client.query(query).to_dataframe()

    # Ensure 'id' column is string and trim whitespace in both DataFrames
    filtered_df['id'] = filtered_df['id'].astype(str).str.strip()
    bq_df['id'] = bq_df['id'].astype(str).str.strip()

    # Step 3: Compare and generate diffs
    existing_ids = set(bq_df['id'])
    diffs_df = filtered_df[~filtered_df['id'].isin(existing_ids)]

    # Reorder diffs_df columns to match the BigQuery schema order exactly
    schema_order = [
        "id",
        "ownerFullName",
        "ownerUsername",
        "type",
        "url",
        "hashtags",
        "timestamp",
        "productType",
        "hashtag_0",
        "hashtag_1",
        "campaignFlag",
        "_id",
        "_createdDate",
        "_updatedDate",
        "_owner",
    ]

    # Fill missing values for STRING fields with empty strings to avoid NULLs in BigQuery
    diffs_df = diffs_df.fillna("")

    # Filter and reorder the DataFrame columns
    diffs_df = diffs_df[schema_order]

    # Save diffs to CSV
    diffs_output_path = f"/home/wesgelpi/Downloads/instagram_diffs_{formatted_now}.csv"
    diffs_df.to_csv(diffs_output_path, index=False)
    print(f"Diffs file saved as: {diffs_output_path}")

    dataset_table = 'self-tape-may.self_tape_may_data.tblInstagramData'  # Specify your dataset and table
    append_to_bigquery(diffs_output_path, dataset_table)

    return diffs_output_path

def append_to_bigquery(csv_file_path, dataset_table):
    """
    Append new data to BigQuery table.

    Args:
        csv_file_path (str): Path to the CSV file containing new data.
        dataset_table (str): BigQuery dataset and table to append the data.
    """
    project_id = 'self-tape-may'
    client = bigquery.Client(project=project_id)
    table_id = dataset_table

    job_config = bigquery.LoadJobConfig(
        schema=[
            SchemaField("id", "STRING"),
            SchemaField("ownerFullName", "STRING"),
            SchemaField("ownerUsername", "STRING"),
            SchemaField("type", "STRING"),
            SchemaField("url", "STRING"),
            SchemaField("hashtags", "STRING"),
            SchemaField("timestamp", "TIMESTAMP"),
            SchemaField("productType", "STRING"),
            SchemaField("hashtag_0", "STRING"),
            SchemaField("hashtag_1", "STRING"),
            SchemaField("campaignFlag", "BOOLEAN"),
            SchemaField("_id", "FLOAT"),
            SchemaField("_createdDate", "TIMESTAMP"),
            SchemaField("_updatedDate", "TIMESTAMP"),
            SchemaField("_owner", "STRING"),
        ],
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )
    
    with open(csv_file_path, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    load_job.result()  # Wait for the job to complete.

    print(f"Appended data to {table_id} from {csv_file_path}. Job ID: {load_job.job_id}")

    activity_message = "Processed CSV and updated diffs."
    append_activity_log('self-tape-may.self_tape_may_data.tblActivityLog', activity_message)

def append_activity_log(dataset_table, activity_message):
    """
    Append an activity log entry to the BigQuery table.

    Args:
        dataset_table (str): BigQuery dataset and table to append the activity log.
        activity_message (str): Activity message to log.
    """
    project_id = 'self-tape-may'
    client = bigquery.Client(project=project_id)

    table_ref = dataset_table
    table = client.get_table(table_ref)  # Make an API request to fetch the table

    # Prepare the row to insert
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)  # Current timestamp in UTC
    rows_to_insert = [
        {"activityType" : 'updateData', "activityDTTM": utc_now.isoformat(), "activityDescription": activity_message},
    ]

    # Insert the row into the table
    errors = client.insert_rows_json(table, rows_to_insert)  # Make an API request
    if errors == []:
        print("New rows have been added.")
   
