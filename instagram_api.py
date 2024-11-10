import requests

FILE_PATH = "/home/wesgelpi/secrets/"
APP_TOKEN_FILE = "instaAppToken.txt"
USER_TOKEN_FILE = "instaUserToken.txt"

# Get instagram secrets
with open(FILE_PATH + APP_TOKEN_FILE, 'r') as file:
    APP_TOKEN = file.read().strip()

with open(FILE_PATH + USER_TOKEN_FILE, 'r') as file:
    USER_TOKEN = file.read().strip()

HASHTAG = 'selftapemay'

# Searching for the hashtag ID
url = f"https://graph.facebook.com/v16.0/ig_hashtag_search?user_id={USER_TOKEN}&q={HASHTAG}&access_token={APP_TOKEN}"
response = requests.get(url)

if response.status_code == 200:
    hashtag_id = response.json().get('data', [])[0].get('id')
    print(f"Hashtag ID: {hashtag_id}")
else:
    print(f"Error: {response.status_code}, {response.text}")