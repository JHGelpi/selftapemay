# pip dependencies
'''
pip install apify
'''
import json
from apify import ApifyClient

filePath = "D:\\github_projects\\apifyAPISecret"
apiURL = ""

with open(filePath, 'r') as file:
    fileContent = file.read()

#client = ApifyClient()
apiURL = "https://api.apify.com/v2/acts/apify~instagram-api-scraper/runs?token="
apiURL = apiURL + fileContent

input_data = {}

actor_id = "apify/instagram-api-scraper"
#run = client.actor(actor_id).call(input=input_data)

#run.wait_for_finish()

#output_data = run.get_output()
