# data_processor.py

# Functions to process the raw data from Apify.
# Filter posts by video/reel type, date range, and check for duplicates.
# Tasks left to do:
    # - Filter out posts that were already uploaded to BigQuery
'''UPDATE FROM 3.7.2024:

I have been successful in downloading from Google BigQuery and uploading/appending a file back
to BigQuery.  However, the results are not filtering our appropriately so I need to look at
how the filter in the dataframe is actually filtering out already known values in the
id column of tbleInstagramData'''

import csv
import ast
import pandas as pd
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
from datetime import datetime
import pytz

def process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag):
    # Initialize an empty DataFrame for diffs_df with the same columns as in your CSV
    diffs_df = pd.DataFrame(columns=['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType', 'hashtag_0', 'hashtag_1', 'campaignFlag', '_id', '_createdDate', '_updatedDate', '_owner'])

    # Step 1: Load and filter the initial CSV
    df = pd.read_csv(input_file_path)

    # Ensure the DataFrame includes all necessary columns, even if they are initially empty
    for column in ['id', 'ownerFullName', 'ownerUsername', 'type', 'url', 'hashtags', 'timestamp', 'productType', 'hashtag_0', 'hashtag_1', 'campaignFlag', '_id', '_createdDate', '_updatedDate', '_owner']:
        if column not in df.columns:
            df[column] = pd.NA  # Assign a missing value placeholder

    # Safely evaluate the hashtags column, accounting for NaN values
    safe_eval = lambda x: ast.literal_eval(x) if pd.notna(x) else []
    df['hashtags_list'] = df['hashtags'].apply(safe_eval)

    # Convert 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Define start and end of the date range
    utc = pytz.UTC
    start_date = utc.localize(datetime(2024, 1, 1, 0, 0, 0))
    end_date = utc.localize(datetime(2024, 4, 30, 23, 59, 59))

    # Filter df for posts within the specified date range
    filtered_df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]

    # Filter based on selftapemay_hashtag and campaign_hashtag
    #df['selftapemayFlag'] = df['hashtags_list'].apply(lambda x: selftapemay_hashtag.lower() in x)
    #df['campaignFlag'] = df['hashtags_list'].apply(lambda x: campaign_hashtag.lower() in x)
    filtered_df['selftapemayFlag'] = df['hashtags_list'].apply(lambda x: selftapemay_hashtag.lower() in x)
    filtered_df['campaignFlag'] = df['hashtags_list'].apply(lambda x: campaign_hashtag.lower() in x)
    
    # filtered_df = df[df['selftapemayFlag']]
    filtered_df = filtered_df[filtered_df['selftapemayFlag']]

    # Export to CSV file - This is a validation step that should be omitted from final solution
    formatted_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    bigquery_output_path = f"/home/wesgelpi/Downloads/instagram_filteredresults_{formatted_now}.csv"
    filtered_df.to_csv(bigquery_output_path, index=False)

    # Step 2: Download BigQuery data and convert to DataFrame
    client = bigquery.Client()
    query = "SELECT * FROM `self-tape-may.self_tape_may_data.tblInstagramData`"
    bq_df = client.query(query).to_dataframe()

    # Export to CSV file - This is a validation step that should be omitted from final solution
    formatted_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    bigquery_output_path = f"/home/wesgelpi/Downloads/instagram_BigQuery_{formatted_now}.csv"
    bq_df.to_csv(bigquery_output_path, index=False)

    # Ensure 'id' column is string and trim whitespace in both DataFrames
    filtered_df['id'] = filtered_df['id'].astype(str).str.strip()
    bq_df['id'] = bq_df['id'].astype(str).str.strip()

    # Step 3: Compare and generate diffs (Existing logic)
    existing_ids = set(bq_df['id'])
    diffs_df = filtered_df[~filtered_df['id'].isin(existing_ids)]

    # Before saving, adjust diffs_df to match the schema exactly
    # Ensure all required fields are present or add them with default values
    diffs_df = diffs_df.assign(
        id=pd.NA,
        ownerFullName=pd.NA,
        ownerUsername=pd.NA,
        type=pd.NA,
        url=pd.NA,
        hashtags=pd.NA,
        timestamp=pd.NA,
        productType=pd.NA,
        hashtag_0=pd.NA,
        hashtag_1=pd.NA,
        campaignFlag=lambda x: x['campaignFlag'].astype(str),
        _id=pd.NA,
        _createdDate=pd.NA,
        _updatedDate=pd.NA,
        _owner=pd.NA,
    )
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

    '''job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip the header row.
        autodetect=True,  # Autodetect schema and options.
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND)  # Append to existing table.'''
    # Explicitly define the schema to match your BigQuery table's schema
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
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
    
    with open(csv_file_path, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    load_job.result()  # Wait for the job to complete.

    print(f"Appended data to {table_id} from {csv_file_path}. Job ID: {load_job.job_id}")

    # Call the function with your specific parameters
    #project_id = 'your-project-id'  # Google Cloud project ID
    #dataset_id = 'self-tape-may'  # Dataset ID
    dataset_table = 'self-tape-may.self_tape_may_data.tblActivityLog'  # Table ID
    activity_message = "Processed CSV and updated diffs."  # Example log message

    # Call the function at the end of the processing or wherever appropriate
    append_activity_log(dataset_table, activity_message)

def append_activity_log(dataset_table, activity_message):
    client = bigquery.Client()

    # Define the table you want to append to
    table_ref = dataset_table
    table = client.get_table(table_ref)  # Make an API request to fetch the table

    # Prepare the row to insert
    # Assuming the table has columns for a timestamp and a message
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)  # Current timestamp in UTC
    rows_to_insert = [
        {"activityType" : 'updateData', "activityDTTM": utc_now.isoformat(), "activityDescription": activity_message},
    ]

    # Insert the row into the table
    errors = client.insert_rows_json(table, rows_to_insert)  # Make an API request
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

'''
# Example usage
selftapemay_hashtag = 'selftapemay'
campaign_hashtag = 'asmr'  # Replace with your actual campaign hashtag
#processed_file_path = process_csv(csv_file_path, campaign_hashtag)
input_file_path = '/home/wesgelpi/Downloads/instagram_scrape_results_2024-03-04_21-28-23.csv'  # Update the path

processed_file_path = process_csv(input_file_path, selftapemay_hashtag, campaign_hashtag)
print(f"Processed file saved as: {processed_file_path}")
'''