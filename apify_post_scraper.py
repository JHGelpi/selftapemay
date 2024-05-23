import requests
from apify_client import ApifyClient
import json
import pandas as pd
import os
from google.cloud import bigquery

def scrape_instagram_posts(user):
    # Apify API details
    memLimit = 32768
    resultsLimit = 20
    filePath = "/home/wesgelpi/secrets/apifySecret.txt"
    apiURL = "https://api.apify.com/v2/acts/apify~instagram-post-scraper/run-sync?token="
    
    with open(filePath, 'r') as file:
        fileContent = file.read().strip()

    apiURL = apiURL + fileContent
    client = ApifyClient(fileContent)

    run_input = {
        "username": user,
        "resultsLimit": resultsLimit,
    }

    scraped_data = []

    #try:
    run = client.actor("nH2AHrwxeTRJoN5hX").call(run_input=run_input, memory_mbytes=memLimit)
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

'''def format_child_posts(child_posts):
    if not child_posts:
        return ""
    formatted = []
    for child in child_posts:
        child_info = {
            "id": child.get("id"),
            "type": child.get("type"),
            "shortCode": child.get("shortCode"),
            "url": child.get("url"),
            "timestamp": child.get("timestamp")
        }
        formatted.append(child_info)
    return json.dumps(formatted)  # Convert list of dicts to JSON string
'''
def parse_post_with_hashtags(post, parent_id=None, inherited_hashtags=None, post_type=None):

    if inherited_hashtags is None:
        inherited_hashtags = []

    if not isinstance(inherited_hashtags, list):
        inherited_hashtags = [inherited_hashtags]
        
    hashtags = post.get("hashtags", inherited_hashtags) or inherited_hashtags

    if not isinstance(hashtags, list):
        hashtags = []
    record = {
        "id": post.get("id"),
        "type": post.get("type") if not post.get("childPosts") else post.get("childPosts")[0].get("type", post.get("type")),
        "shortCode": post.get("shortCode"),
        "caption": post.get("caption"),
        "hashtags": hashtags,
        "url": post.get("url"),
        "commentsCount": post.get("commentsCount"),
        "displayUrl": post.get("displayUrl"),
        "timestamp": post.get("timestamp"),
        "ownerUsername": post.get("ownerUsername"),
        "ownerId": post.get("ownerId"),
        "videoUrl": post.get("videoUrl"),
        "productType": post.get("productType")
    }
    records.append(record)

    for child in post.get("childPosts", []):
        child_record = child.copy()
        child_record["hashtags"] = hashtags  # Inherit parent's hashtags
        parse_post_with_hashtags(child_record, inherited_hashtags=hashtags)

def convert_json_to_csv(users, csv_file_path):
    schema_csv_path = '/home/wesgelpi/self_tape_may/apify_post_scrape_schema.csv'

    # Initialize a list to hold the records
    global records
    records = []

    # Load the schema CSV to determine the required columns
    sample_csv = pd.read_csv(schema_csv_path)
    required_columns = sample_csv.columns.tolist()

    json_data = scrape_instagram_posts(users)
        
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
    #project_id = 'self-tape-may'
    #client = bigquery.Client(project=project_id)
    #users = get_users()
    # Assuming 'users' is an iterable of user information
    #instagram_handles = [user['instagram'] for user in users]  # Collect all handles
    #print (instagram_handles)
    #if instagram_handles:
    #    convert_json_to_csv(instagram_handles, '/home/wesgelpi/Downloads/instagram_scrape_results_2024-05-20_06-00-01.csv')
    #print('Completed...')
