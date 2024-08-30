import requests
import json
import pandas as pd
import os
from google.cloud import bigquery
from flask import Flask, redirect, request, session, jsonify

# Constants
MEM_LIMIT = 32768
RESULTS_LIMIT = 20
SCHEMA_CSV_PATH = '/home/wesgelpi/self_tape_may/apify_post_scrape_schema.csv'

# Instagram API credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'your_redirect_uri'
ACCESS_TOKEN = 'your_access_token'  # Replace with your actual access token

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_user_media(username):
    """
    Call the Instagram API to get user media.

    Args:
        username (str): Instagram username to get media data for.

    Returns:
        list: List of dictionaries containing media data.
    """
    media_data = []

    try:
        profile_url = f'https://graph.instagram.com/{username}/media?fields=id,caption,media_url,timestamp,username,permalink,media_type,children&access_token={ACCESS_TOKEN}'
        response = requests.get(profile_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        media_data = response.json().get('data', [])
        return media_data
    except requests.exceptions.RequestException as e:
        print(f"Error while calling Instagram API: {e}")
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

    hashtags = post.get("caption", "").split()  # Extract hashtags from caption
    timestamp = post.get("timestamp") or inherited_timestamp
    ownerUsername = post.get("username") or inherited_ownerUsername

    record = {
        "id": post.get("id"),
        "type": post.get("media_type"),
        "shortCode": post.get("permalink").split('/')[-2],
        "caption": post.get("caption"),
        "hashtags": hashtags,
        "url": post.get("permalink"),
        "commentsCount": None,  # Not available in Basic Display API
        "displayUrl": post.get("media_url"),
        "timestamp": timestamp,
        "ownerUsername": ownerUsername,
        "ownerId": None,  # Not available in Basic Display API
        "videoUrl": post.get("media_url") if post.get("media_type") == 'VIDEO' else None,
        "productType": None  # Not available in Basic Display API
    }

    if not post.get("children"):
        records.append(record)

    for child in post.get("children", []):
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
        json_data = get_user_media(user)
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
