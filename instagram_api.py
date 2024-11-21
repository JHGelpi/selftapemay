import requests
import json

'''def main():
    CONFIG_FILE_PATH = "/home/wesgelpi/self_tape_may/"
    CONFIG_FILE = "config.json"

    with open(CONFIG_FILE_PATH + CONFIG_FILE, 'r') as file:
            config = json.load(file)
            FILE_PATH = config['secrets_folder'][0]
            
            # user ID token
            USER_TOKEN_FILE = config['user_token_file'][0]
            
            #instagram app ID
            APP_ID_FILE = config['app_id_file'][0]
            
            #instagram app secret
            APP_TOKEN_FILE = config['app_token_file'][0]
            API_VERSION = config['api_version'][0]

            #business account ID
            USER_ID = config['bus_acct_userID'][0]

            #hashtag
            HASHTAG = config['hashtag'][0]

    # Get instagram secrets
    with open(FILE_PATH + APP_TOKEN_FILE, 'r') as file:
        APP_TOKEN = file.read().strip()

    with open(FILE_PATH + APP_ID_FILE, 'r') as file:
        APP_ID = file.read().strip()

    with open(FILE_PATH + USER_TOKEN_FILE, 'r') as file:
        USER_TOKEN = file.read().strip()

    # Step 1: Get the hashtag ID for the hashtag "coke"
    hashtag_search_url = f"https://graph.facebook.com/{API_VERSION}/ig_hashtag_search"
    params = {
        "user_id": USER_ID,      # Instagram Business Account ID
        "q": HASHTAG,            # Hashtag to search for
        "access_token": USER_TOKEN
    }

    response = requests.get(hashtag_search_url, params=params)

    if response.status_code == 200:
        hashtag_data = response.json().get('data', [])
        if hashtag_data:
            hashtag_id = hashtag_data[0]['id']
            print(f"Hashtag ID for #{HASHTAG}: {hashtag_id}")
            
            # Step 2: Use the hashtag ID to get the recent posts for that hashtag
            get_recent_posts(hashtag_id, USER_ID, USER_TOKEN, API_VERSION)
        else:
            print("Hashtag not found.")
    else:
        print(f"Error: {response.status_code}, {response.text}")'''

# Step 2: Get recent posts for the hashtag
'''def get_recent_posts(hashtag_id, user_id, access_token, api_version):
    recent_media_url = f"https://graph.facebook.com/{api_version}/{hashtag_id}/recent_media"
    params = {
        "user_id": user_id,
        "fields": "id,caption,media_type,media_url,permalink,timestamp",
        "access_token": access_token
    }

    response = requests.get(recent_media_url, params=params)

    if response.status_code == 200:
        media_data = response.json().get('data', [])
        for media in media_data:
            print(f"Media ID: {media['id']}, Type: {media['media_type']}, Caption: {media.get('caption')}, Link: {media.get('permalink')}")
    else:
        print(f"Error getting media: {response.status_code}, {response.text}")'''
        
'''def getUserAccessToken():
     # Example URL:
     app_id = getConfigData()[1]
     redirect_uri = ''

     OAuthURL = f'https://www.facebook.com/v21.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope=instagram_basic,instagram_manage_insights,pages_show_list&response_type=code'
     print (OAuthURL)'''

def getConfigData():
    CONFIG_FILE_PATH = "/home/wesgelpi/self_tape_may/"
    CONFIG_FILE = "config.json"

    with open(CONFIG_FILE_PATH + CONFIG_FILE, 'r') as file:
            config = json.load(file)
            FILE_PATH = config['secrets_folder'][0]
            
            # user ID token
            USER_TOKEN_FILE = config['user_token_file'][0]
            
            #instagram app ID
            APP_ID_FILE = config['app_id_file'][0]
            
            #instagram app secret
            APP_TOKEN_FILE = config['app_token_file'][0]
            API_VERSION = config['api_version'][0]

            #business account ID
            USER_ID = config['bus_acct_userID'][0]

            #hashtag
            HASHTAG = config['hashtag'][0]
            
            #callback URI
            CALLBACK_URI = config['callback_uri'][0]

            API_SCOPE = config['scopes']
            

    # Get instagram secrets
    with open(FILE_PATH + APP_TOKEN_FILE, 'r') as file:
        APP_TOKEN = file.read().strip()

    with open(FILE_PATH + APP_ID_FILE, 'r') as file:
        APP_ID = file.read().strip()

    with open(FILE_PATH + USER_TOKEN_FILE, 'r') as file:
        USER_TOKEN = file.read().strip()
    
    return APP_TOKEN, APP_ID, USER_TOKEN, USER_ID, HASHTAG, API_VERSION, CALLBACK_URI, API_SCOPE
###################################################################################
###################################################################################
###################################################################################
import requests
import json

def get_user_access_token():
    """
    You should already have a valid User Access Token for the test user 'wgelpi'.
    Replace 'your_user_access_token_here' with the actual access token for 'wgelpi'.
    """
    return 'your_user_access_token_here'

def search_hashtag(hashtag, user_id, access_token, api_version='v16.0'):
    """
    Search for a hashtag ID using the Instagram Graph API.

    :param hashtag: Hashtag to search (without the '#').
    :param user_id: The Instagram Business Account ID.
    :param access_token: The User Access Token.
    :param api_version: API version to use.
    :return: Hashtag ID or None if the hashtag is not found.
    """
    hashtag_search_url = f"https://graph.facebook.com/{api_version}/ig_hashtag_search"
    params = {
        'user_id': user_id,
        'q': hashtag,
        'access_token': access_token
    }

    response = requests.get(hashtag_search_url, params=params)

    if response.status_code == 200:
        hashtag_data = response.json().get('data', [])
        if hashtag_data:
            return hashtag_data[0]['id']
        else:
            print("Hashtag not found.")
    else:
        print(f"Error searching hashtag: {response.status_code}, {response.text}")

    return None

def get_recent_media_for_hashtag(hashtag_id, user_id, access_token, api_version='v16.0'):
    """
    Get recent media for a given hashtag ID.

    :param hashtag_id: Hashtag ID obtained from the hashtag search.
    :param user_id: The Instagram Business Account ID.
    :param access_token: The User Access Token.
    :param api_version: API version to use.
    """
    recent_media_url = f"https://graph.facebook.com/{api_version}/{hashtag_id}/recent_media"
    params = {
        'user_id': user_id,
        'fields': 'id,caption,media_type,media_url,permalink,timestamp',
        'access_token': access_token
    }

    response = requests.get(recent_media_url, params=params)

    if response.status_code == 200:
        media_data = response.json().get('data', [])
        if media_data:
            for media in media_data:
                print(f"Media ID: {media['id']}, Type: {media['media_type']}, Caption: {media.get('caption')}, Link: {media.get('permalink')}")
        else:
            print("No media found for this hashtag.")
    else:
        print(f"Error getting recent media: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Step 1: Get User Access Token
    access_token = get_user_access_token()
    
    # Step 2: Define User ID and Hashtag
    user_id = 'your_instagram_business_user_id_here'  # Replace with the actual Instagram Business Account ID of 'wgelpi'
    hashtag = 'selftapemay'

    # Step 3: Search for Hashtag ID
    hashtag_id = search_hashtag(hashtag, user_id, access_token)

    if hashtag_id:
        # Step 4: Get Recent Media for Hashtag
        get_recent_media_for_hashtag(hashtag_id, user_id, access_token)
    else:
        print("Unable to find the hashtag ID.")

#if __name__ == "__main__":
#    main()