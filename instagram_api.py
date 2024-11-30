import requests
#import logging
from utils import get_config_data, configure_logging

def get_instagram_business_user_id(api_version, access_token):
    """
    Retrieve the Instagram Business Account User ID.

    :param access_token: The User Access Token.
    :return: Instagram Business Account User ID or None if not found.
    """
    #api_version = get_config_data()[5] # API_VERSION
    url = f'https://graph.facebook.com/{api_version}/me/accounts'
    params = {
        'access_token': access_token # This needs to be the long-lived access token
    }

    print(f"Making request to get Instagram Business User ID with URL: {url} and params: {params}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        accounts_data = response.json().get('data', [])
        if len(accounts_data) > 0:
            return accounts_data[0]['id']
        else:
            print("No linked Instagram accounts found.")
    else:
        print(f"Error retrieving accounts: {response.status_code}, {response.text}")

    return None

def search_hashtag(hashtag, user_id, access_token, api_version):
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

    print(f"Searching for hashtag with URL: {hashtag_search_url} and params: {params}")
    try:
        response = requests.get(hashtag_search_url, params=params)
        print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
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

    print(f"Getting recent media for hashtag with URL: {recent_media_url} and params: {params}")
    response = requests.get(recent_media_url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

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
    # Configure logging
    configure_logging()

    # Config data from utils.py
    config_data = get_config_data()
    #check_and_refresh_token()
    
    print("Starting main program to interact with Instagram API.")
    
    # Step 1: Get User Access Token
    try:
        print("Retrieving user access token from configuration data.")
        access_token = config_data[8]
    except Exception as e:
        print(f"Error retrieving user access token: {e}")
        raise

    # Step 2: Define User ID and Hashtag
    try:
        user_id = get_instagram_business_user_id(config_data[5], access_token)
    except Exception as e:
        print(f"Error retrieving Instagram Business User ID: {e}")
        raise
    
    if not user_id:
        print("Instagram Business Account User ID not found.")
    else:
        hashtag = config_data[4]

        # Step 3: Search for Hashtag ID
        try:
            hashtag_id = search_hashtag(hashtag, user_id, access_token, api_version=config_data[5])
        except Exception as e:
            print(f"Error searching for hashtag ID: {e}")
            raise

        if hashtag_id:
            # Step 4: Get Recent Media for Hashtag
            try:
                get_recent_media_for_hashtag(hashtag_id, user_id, access_token)
            except Exception as e:
                print(f"Error getting recent media for hashtag: {e}")
                raise
        else:
            print("Unable to find the hashtag ID.")
