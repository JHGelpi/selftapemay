import requests
import json

CONFIG_FILE_PATH = "/home/wesgelpi/self_tape_may/"
CONFIG_FILE = "config.json"

with open(CONFIG_FILE_PATH + CONFIG_FILE, 'r') as file:
        config = json.load(file)
        FILE_PATH = config['secrets_folder'][0]
        
        # meta app ID
        USER_TOKEN_FILE = config['user_token_file'][0]
        
        #instagram app ID
        APP_ID_FILE = config['app_id_file'][0]
        
        #instagram app secret
        APP_TOKEN_FILE = config['app_token_file'][0]
        API_VERSION = config['api_version'][0]

# Get instagram secrets
with open(FILE_PATH + APP_TOKEN_FILE, 'r') as file:
    APP_TOKEN = file.read().strip()

with open(FILE_PATH + APP_ID_FILE, 'r') as file:
    APP_ID = file.read().strip()

with open(FILE_PATH + USER_TOKEN_FILE, 'r') as file:
    USER_TOKEN = file.read().strip()

#API_VERSION = ''
APP_ENDPOINT = ''
#HASHTAG = 'selftapemay'

# Searching for the hashtag ID
# url = f"https://graph.facebook.com/v16.0/ig_hashtag_search?user_id={USER_TOKEN}&q={HASHTAG}&access_token={APP_TOKEN}"
#endpoint_url = f"https://graph.facebook.com/{API_VERSION}/user_id=wgelpi"
#endpoint_url = f"https://graph.facebook.com/{API_VERSION}/USER-ID?access_token={APP_ID}|{APP_TOKEN}"
#print ('endpoint URL: ', endpoint_url)

#endpoint_url = f"https://graph.facebook.com/oauth/access_token?client_id={USER_TOKEN}&client_secret={APP_TOKEN}&grant_type=client_credentials"

endpoint_url = f"https://graph.facebook.com/ig_hashtag_search?user_id={USER_TOKEN}&access_token={APP_ID}&q=coke"

print (endpoint_url)

response = requests.get(endpoint_url)

'''url = f"https://graph.facebook.com/{APP_ENDPOINT}&access_token={APP_TOKEN}"
response = requests.get(url)
'''
# curl -i -X GET "https://graph.facebook.com/{api-endpoint}&access_token={your-app_id}|{your-app_secret}"   

if response.status_code == 200:
    hashtag_id = response.json().get('data', [])[0].get('id')
    print(f"Hashtag ID: {hashtag_id}")
else:
    print(f"Error: {response.status_code}, {response.text}")