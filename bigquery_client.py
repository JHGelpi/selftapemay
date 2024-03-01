
# bigquery_client.py
# Functions to connect to BigQuery, query the tblInstagramUsers table, and insert data into the tblInstagramData table.
# Use the Google Cloud Python SDK for BigQuery.

from datetime import datetime
import csv
# Get the current date and time
now = datetime.now()
# Format it as a string, e.g., "2024-02-21_17-51-57"
formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")

# Define a single CSV file name with the current date and timestamp
csv_file_name = f"instagram_scrape_results_{formatted_now}.csv"
# Define the CSV file path, e.g., "/mnt/data/" for saving in this environment
csv_file_path = f"/home/wesgelpi/Downloads/{csv_file_name}"

from google.cloud import bigquery

# Import the scrape_instagram function from apifyClient.py
from apifyClient import scrape_instagram
from data_processor import process_csv

# Initialize the BigQuery client
client = bigquery.Client()

def get_users():
    # Function to retrieve user data from BigQuery

    # Retrieve user data from the BigQuery table.
    query = """
        SELECT * FROM `self-tape-may.self_tape_may_data.tblInstagramUsers`
    """
    query_job = client.query(query)  # Make an API request.
    
    try:
        users = query_job.result()  # Waits for the query to finish
        return users
    except Exception as e:
        print("Error in get_users:", e)
        return None

users = get_users()

# Open the CSV file once before the loop
with open(csv_file_path, mode='w', newline='') as file:
    fieldnames = ['id', 'type', 'ownerUsername', 'hashtags', 'url', 'timestamp', 'childPosts']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    if users is not None:
        for user in users:
            # For every user I neeed to loop through and call the apify_client.py code
            #print(user['instagramHandle'])
            # Call the scrape_instagram function with the Instagram handle
            instagram_handle = user['instagramHandle']
            scrape_result = scrape_instagram(instagram_handle)
            # Write each item in the scrape_result to the CSV
            for item in scrape_result:
                writer.writerow(item)
    else:
        print("No users found or an error occurred.")

print(f"CSV file saved: {csv_file_path}")

selftapemay_hashtag = 'selftapemay'
campaign_hashtag = 'asmr'
processed_file_path = process_csv(csv_file_path, selftapemay_hashtag, campaign_hashtag)

print(f"Processed file saved as: {processed_file_path}")

