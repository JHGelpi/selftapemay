# apify_client.py
# Functions to make requests to the Apify API using the requests library.
# Handle API responses and extract relevant data.
# API Endpoint for synchronous execution:
# https://api.apify.com/v2/acts/apify~instagram-reel-scraper/run-sync?token=

import requests
import json
from apify_client import ApifyClient

# user variable from bigquery_client.py
#user = bigqueryUser
#user = "audreyhelpsactorspodcast"
user = "tikka.thedog"
jsonResult = ""

# Apify URL build
intResults = 5
filePath = "/home/wesgelpi/secrets/apifySecret.txt"
apiURL = "https://api.apify.com/v2/acts/"
#input_data = {}
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
        "username": [user],
        "resultsLimit": 10,
    }

    try:
        # Run the Actor and wait for it to finish
        run = client.actor("xMc5Ga1oCONPmWJIa").call(run_input=run_input)

        # Fetch and print Actor results from the run's dataset (if there are any)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            # Desired fields
            # id, type, ownerUsername, shortURL, timestamp, childPosts
            # print(item)
            print('====BEGIN====')
            print('id: ', item['id'])
            print('Type: ', item['type'])
            print('ownerUsername: ', item['ownerUsername'])
            print('hashtags: ', item['hashtags'])
            print('shortURL: ', item['url'])
            print('timestamp: ', item['timestamp'])
            print('childPosts[]: ', item['childPosts'])
            print('****END****')
        #response = requests.post(apiURL, json=payload, headers=headers)
        #response.raise_for_status()
        return run
    except requests.exceptions.RequestException as e:
        print(f"Error while calling Apify API: {e}")
        return None

jsonResult = scrape_instagram(user)
#print (jsonResult)