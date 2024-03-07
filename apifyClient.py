# apify_client.py
# Functions to make requests to the Apify API using the requests library.
# Handle API responses and extract relevant data.
# API Endpoint for synchronous execution:
# https://api.apify.com/v2/acts/apify~instagram-reel-scraper/run-sync?token=

import requests
from apify_client import ApifyClient
#from apify_client import ApifyClientAsync
#import asyncio

# Apify URL build
memLimit = 32768
resultsLimit = 10
filePath = "/home/wesgelpi/secrets/apifySecret.txt"
apiURL = "https://api.apify.com/v2/acts/"
actor_id = "apify~instagram-reel-scraper/run-sync"
apiURL = apiURL + actor_id + "?token="

with open(filePath, 'r') as file:
    fileContent = file.read().strip()

apiURL = apiURL + fileContent

# Initialize the ApifyClient with my API Token
client = ApifyClient(fileContent)

def scrape_instagram(user):
    # Function to call Apify API and scrape Instagram data
    # Build the Apify API Payload
    run_input = {
        "username": user,
        "resultsLimit": resultsLimit,
    }

    scraped_data = []  # List to hold the results

    try:
        # Run the Actor and wait for it to finish
        run = client.actor("xMc5Ga1oCONPmWJIa").call(run_input=run_input, memory_mbytes=memLimit)

        # Fetch and print Actor results from the run's dataset (if there are any)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            # Desired fields
            # item['id'], item['type'], item['ownerUsername'], item['hashtags'], item['url']
            # item['timestamp'], item['childPosts']
            # Extracting desired fields
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
