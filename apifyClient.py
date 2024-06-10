"""
apify_client.py
Functions to make requests to the Apify API using the requests library.
Handle API responses and extract relevant data.
API Endpoint for synchronous execution: https://api.apify.com/v2/acts/apify~instagram-reel-scraper/run-sync?token=
"""

import requests
from apify_client import ApifyClient

# Constants
MEM_LIMIT = 32768
RESULTS_LIMIT = 40
FILE_PATH = "/home/wesgelpi/secrets/apifySecret.txt"
API_URL = "https://api.apify.com/v2/acts/"
ACTOR_ID = "apify~instagram-reel-scraper/run-sync"

# Build the Apify API URL
with open(FILE_PATH, 'r') as file:
    api_token = file.read().strip()

api_url = f"{API_URL}{ACTOR_ID}?token={api_token}"

# Initialize the ApifyClient with the API Token
client = ApifyClient(api_token)


def scrape_instagram(username):
    """
    Call the Apify API to scrape Instagram data.

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
                'timestamp': item.get('timestamp')
            }
            scraped_data.append(data_entry)
        
        return scraped_data
    except requests.exceptions.RequestException as e:
        print(f"Error while calling Apify API: {e}")
        return None
