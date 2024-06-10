"""
apify_client.py
Functions to make requests to the Apify API using the requests library.
Handle API responses and extract relevant data.
"""

import requests
from apify_client import ApifyClient
import json
import pandas as pd
import os
from google.cloud import bigquery

# Constants
MEM_LIMIT = 32768
RESULTS_LIMIT = 20
FILE_PATH = "/home/wesgelpi/secrets/apifySecret.txt"
ACTOR_ID = "apify~instagram-post-scraper/run-sync"
SCHEMA_CSV_PATH = '/home/wesgelpi/self_tape_may/apify_post_scrape_schema.csv'

# Build the Apify API URL
with open(FILE_PATH, 'r') as file:
    api_token = file.read().strip()

api_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}?token={api_token}"

# Initialize the ApifyClient with the API Token
client = ApifyClient(api_token)


def scrape_instagram_posts(username):
    """
    Call the Apify API to scrape Instagram posts.

    Args:
        username (str): Instagram username to scrape data for.

    Returns:
        list: List of dictionaries containing scraped data.
    """
    run_input = {
        "username": username,
        "resultsLimit": RESULTS_LIMIT,
    }

    scraped_data = []

    try:
        # Run the Actor and wait for it to finish
        run = client.actor(ACTOR_ID).call(run_input=run_input, memory_mbytes=MEM_LIMIT)

        # Fetch and print Actor results from the run's dataset
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            data_entry = {
                'id': item.get('id'),
                'type': item.get('type'),
                'ownerUsername': item.get('ownerUsername'),
                'hashtags': item.get('hashtags'),
                'url': item.get('url'),
                'timestamp': item.get('timestamp'),
                'childPosts': item.get('childPosts', [])
            }
            scraped_data.append(data_entry)
        
        return scraped_data
    except requests.exceptions.RequestException as e:
        print(f"Error while calling Apify API: {e}")
        return None


def parse_post_with_hashtags(post, parent_id=None, inherited_hashtags=None, inherited_timestamp=None, inherited_ownerUsername=None):
    """
    Parse Instagram posts and extract hashtags, including inherited hashtags from parent posts.

    Args:
        post (dict): The Instagram post data.
        parent_id (str): ID of the parent post (if any).
        inherited_hashtags (list): List of inherited hashtags from the parent post.
        inherited_timestamp (str): Timestamp inherited from the parent post.
        inherited_ownerUsername (str): Owner username inherited from the parent post.
    """
    if inherited_hashtags is None:
        inherited_hashtags = []

    if not isinstance(inherited_hashtags, list):
        inherited_hashtags = [inherited_hashtags]
        
    hashtags = post.get("hashtags", inherited_hashtags) or inherited_hashtags
    timestamp = post.get("timestamp") or inherited_timestamp
    ownerUsername = post.get("ownerUsername") or inherited_ownerUsername

    if not isinstance(hashtags, list):
        hashtags = []

    record = {
        "id": post.get("id"),
        "type": post.get("type"),
        "shortCode": post.get("shortCode"),
        "caption": post.get("caption"),
        "hashtags": hashtags,
        "url": post.get("url"),
        "commentsCount": post.get("commentsCount"),
        "displayUrl": post.get("displayUrl"),
        "timestamp": timestamp,
        "ownerUsername": ownerUsername,
        "ownerId": post.get("ownerId"),
        "videoUrl": post.get("videoUrl"),
        "productType": post.get("productType")
    }

    if not post.get("childPosts"):
        records.append(record)

    for child in post.get("childPosts", []):
        child_record = child.copy()
        child_record["hashtags"] = hashtags  # Inherit parent's hashtags
        parse_post_with_hashtags(child_record, inherited_hashtags=hashtags, inherited_timestamp=timestamp, inherited_ownerUsername=ownerUsername)


def convert_json_to_csv(users, csv_file_path):
    """
    Convert JSON data from Instagram posts to a CSV file.

    Args:
        users (list): List of Instagram usernames to scrape data for.
        csv_file_path (str): Path to the CSV file where data will be saved.
    """
    global records
    records = []

    # Load the schema CSV to determine the required columns
    sample_csv = pd.read_csv(SCHEMA_CSV_PATH)
    required_columns = sample_csv.columns.tolist()

    for user in users:
        json_data = scrape_instagram_posts(user)
        if json_data:
            # Parse the main post and its child posts
            for post in json_data:
                parse_post_with_hashtags(post)
    
    # Convert records to DataFrame
    df = pd.DataFrame(records)
    # Filter the DataFrame to include only the required columns
    filtered_df = df[required_columns]
    
    # Check if the output CSV file exists
    if os.path.isfile(csv_file_path):
        # Read the existing CSV file
        existing_df = pd.read_csv(csv_file_path)
        # Get the set of existing URLs
        existing_urls = set(existing_df['url'].dropna().tolist())
        # Filter out rows in filtered_df where the URL already exists in existing_urls
        filtered_df = filtered_df[~filtered_df['url'].isin(existing_urls)]
    
    file_exists = os.path.isfile(csv_file_path)
    # Save the filtered DataFrame to the CSV file, appending if it exists
    filtered_df.to_csv(csv_file_path, mode='a', header=not file_exists, index=False)


if __name__ == "__main__":
    print('Starting manual run...')
    # Example usage:
    # convert_json_to_csv(['josephinecroft'], '/home/wesgelpi/Downloads/instagram_scrape_results_josephinecroft_2024-05-29.csv')
    print('Completed manual run...')
