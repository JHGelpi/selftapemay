"""
bigquery_client.py
Functions to connect to BigQuery, query the tblInstagramUsers table, and insert data into the tblInstagramData table.
Use the Google Cloud Python SDK for BigQuery.
"""

from datetime import datetime
import csv
import json
from google.cloud import bigquery
from apifyClient import scrape_instagram
from data_processor import process_csv
from apify_post_scraper import scrape_instagram_posts, convert_json_to_csv

# Initialize the BigQuery client
project_id = 'self-tape-may'
client = bigquery.Client(project=project_id)

# Get the current date and time
now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")

# Define the CSV file path
csv_file_path = f"/home/wesgelpi/Downloads/instagram_scrape_results_{formatted_now}.csv"


def get_users():
    """
    Retrieve user data from the BigQuery table.
    
    Returns:
        users (google.cloud.bigquery.table.RowIterator): Iterator over rows of the query result.
    """
    sql_file = '/home/wesgelpi/self_tape_may/sql_query.txt'
    with open(sql_file, 'r') as file:
        query = file.read().strip()

    try:
        query_job = client.query(query)  # Make an API request.
        users = query_job.result()  # Waits for the query to finish
        return users
    except Exception as e:
        print("Error in get_users:", e)
        return None


def write_to_csv(file_path, data, fieldnames):
    """
    Write data to a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        data (list of dict): Data to write to the CSV file.
        fieldnames (list of str): List of field names for the CSV file.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def main():
    # Retrieve users from BigQuery
    users = get_users()
    if users is None:
        return

    # Collect Instagram handles
    instagram_handles = [user['instagram'] for user in users]

    # Scrape Instagram data
    print("Scraping results starting at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    scrape_result = scrape_instagram(instagram_handles)
    print("Completed scraping results at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "writing data to csv...")

    # Write scraping results to CSV
    fieldnames = ['id', 'type', 'ownerUsername', 'hashtags', 'url', 'timestamp']
    write_to_csv(csv_file_path, scrape_result, fieldnames)
    print("Results Apify reel scraper written to csv at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Scrape Instagram posts and convert JSON to CSV
    scrape_result = convert_json_to_csv(instagram_handles, csv_file_path)
    print("Results from Apify post scraper written to csv at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Process CSV file with hashtags
    json_file = '/home/wesgelpi/self_tape_may/hashtags.json'
    with open(json_file, 'r') as file:
        hashtags = json.load(file)
        selftapemay_hashtag = hashtags['selftapemay_hashtag']
        campaign_hashtag = hashtags['campaign_hashtag']

    processed_file_path = process_csv(csv_file_path, selftapemay_hashtag, campaign_hashtag)
    print(f"Processed file saved as: {processed_file_path}")


if __name__ == "__main__":
    main()
