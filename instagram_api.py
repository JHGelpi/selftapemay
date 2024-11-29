import requests
import json
import logging
import datetime

def get_config_data():
    """
    Load configuration data from the config file.
    
    :return: Tuple containing APP_TOKEN, APP_ID, USER_TOKEN, USER_ID, HASHTAG, API_VERSION, CALLBACK_URI, API_SCOPE
    """
    CONFIG_FILE_PATH = "/home/wesgelpi/self_tape_may/"
    CONFIG_FILE = "config.json"

    logging.debug("Loading configuration data from the config file.")
    try:
        with open(CONFIG_FILE_PATH + CONFIG_FILE, 'r') as file:
            config = json.load(file)
            FILE_PATH = config['secrets_folder'][0]

            # Extract configuration details from JSON
            USER_SHORT_TOKEN_FILE = config['user_short_token_file'][0] # facebook/FBUserShortOAuthToken.txt - Obtained with the flask app
            USER_LONG_TOKEN_FILE = config['user_long_token_file'][0] # facebook/FBUserLongOAuthToken.txt
            APP_ID_FILE = config['app_id_file'][0] # 'facebookAppID.txt'
            APP_TOKEN_FILE = config['app_token_file'][0] # 'facebookAppsecret.txt'
            API_VERSION = config['api_version'][0] # 'v21.0'
            USER_ID = config['bus_acct_userID'][0] # 'wgelpi'
            HASHTAG = config['hashtag'][0] # 'coke'
            CALLBACK_URI = config['callback_uri'][0] # ''
            API_SCOPE = config['scopes'] # 'instagram_basic,instagram_manage_insights,pages_show_list'
            LOG_FILE = config['logging_file'][0]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading configuration file: {e}")
        raise

    # Get Instagram secrets
    logging.debug("Reading Instagram secrets from files.")
    try:
        with open(FILE_PATH + APP_TOKEN_FILE, 'r') as file:
            APP_TOKEN = file.read().strip()

        with open(FILE_PATH + APP_ID_FILE, 'r') as file:
            APP_ID = file.read().strip()

        with open(FILE_PATH + USER_SHORT_TOKEN_FILE, 'r') as file:
            USER_SHORT_TOKEN = file.read().strip()
        with open(FILE_PATH + USER_LONG_TOKEN_FILE, 'r') as file:
            USER_LONG_TOKEN = file.read().strip()
    except FileNotFoundError as e:
        logging.error(f"Error reading Instagram secrets: {e}")
        raise

    return APP_TOKEN, APP_ID, USER_SHORT_TOKEN, USER_ID, HASHTAG, API_VERSION, CALLBACK_URI, API_SCOPE, USER_LONG_TOKEN, FILE_PATH, USER_SHORT_TOKEN_FILE, USER_LONG_TOKEN_FILE, LOG_FILE

def configure_logging():
    """
    Configure logging to write to a file and to the console.
    """
    config_data = get_config_data()
    log_file_base = config_data[12]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = f"{log_file_base}{__file__.split('/')[-1].replace('.py', '')}_log_{timestamp}.log"

    logging.basicConfig(
        filename=log_file_path,
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
    )

    # Adding a stream handler to also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)

def get_user_access_token():
    """
    Retrieve a valid User Access Token from the config data.
    
    :return: The User Access Token.
    """
    logging.debug("Retrieving user access token from configuration data.")
    return get_config_data()[8] # USER_LONG_TOKEN which is in facebook/FBUserLongOAuthToken.txt

def get_instagram_business_user_id(access_token):
    """
    Retrieve the Instagram Business Account User ID.

    :param access_token: The User Access Token.
    :return: Instagram Business Account User ID or None if not found.
    """
    api_version = get_config_data()[5] # API_VERSION
    url = f'https://graph.facebook.com/{api_version}/me/accounts'
    params = {
        'access_token': access_token # This needs to be the long-lived access token
    }

    logging.debug(f"Making request to get Instagram Business User ID with URL: {url} and params: {params}")
    response = requests.get(url, params=params)
    logging.debug(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        accounts_data = response.json().get('data', [])
        if len(accounts_data) > 0:
            return accounts_data[0]['id']
        else:
            logging.error("No linked Instagram accounts found.")
    else:
        logging.error(f"Error retrieving accounts: {response.status_code}, {response.text}")

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

    logging.debug(f"Searching for hashtag with URL: {hashtag_search_url} and params: {params}")
    response = requests.get(hashtag_search_url, params=params)
    logging.debug(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        hashtag_data = response.json().get('data', [])
        if hashtag_data:
            return hashtag_data[0]['id']
        else:
            logging.error("Hashtag not found.")
    else:
        logging.error(f"Error searching hashtag: {response.status_code}, {response.text}")

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

    logging.debug(f"Getting recent media for hashtag with URL: {recent_media_url} and params: {params}")
    response = requests.get(recent_media_url, params=params)
    logging.debug(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        media_data = response.json().get('data', [])
        if media_data:
            for media in media_data:
                logging.info(f"Media ID: {media['id']}, Type: {media['media_type']}, Caption: {media.get('caption')}, Link: {media.get('permalink')}")
        else:
            logging.error("No media found for this hashtag.")
    else:
        logging.error(f"Error getting recent media: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Configure logging
    configure_logging()

    logging.debug("Starting main program to interact with Instagram API.")
    
    # Step 1: Get User Access Token
    try:
        access_token = get_user_access_token()
    except Exception as e:
        logging.error(f"Error retrieving user access token: {e}")
        raise

    # Step 2: Define User ID and Hashtag
    try:
        user_id = get_instagram_business_user_id(access_token)
    except Exception as e:
        logging.error(f"Error retrieving Instagram Business User ID: {e}")
        raise
    
    if not user_id:
        logging.error("Instagram Business Account User ID not found.")
    else:
        hashtag = get_config_data()[4]

        # Step 3: Search for Hashtag ID
        try:
            hashtag_id = search_hashtag(hashtag, user_id, access_token, api_version=get_config_data()[5])
        except Exception as e:
            logging.error(f"Error searching for hashtag ID: {e}")
            raise

        if hashtag_id:
            # Step 4: Get Recent Media for Hashtag
            try:
                get_recent_media_for_hashtag(hashtag_id, user_id, access_token)
            except Exception as e:
                logging.error(f"Error getting recent media for hashtag: {e}")
                raise
        else:
            logging.error("Unable to find the hashtag ID.")
