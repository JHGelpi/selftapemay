import logging
import json
import datetime
import webbrowser
import requests
import re
#from instagramLongLivedToken import long_token_main_function

def get_config_data():
    
    '''
    Load configuration data from the config file.
    
    :return: Tuple containing APP_TOKEN, APP_ID, USER_TOKEN, USER_ID, HASHTAG, API_VERSION, CALLBACK_URI, API_SCOPE
    '''
    
    CONFIG_FILE_PATH = '/home/wesgelpi/self_tape_may/'
    CONFIG_FILE = 'config.json'

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
            USER_ID = config['bus_acct_userID'][0] # '17841457196827849'
            HASHTAG = config['hashtag'][0] # 'coke'
            CAMPAIGN_HASHTAG = config['campaign_hashtag'][0]
            CALLBACK_URI = config['callback_uri'][0] # ''
            API_SCOPE = config['scopes'] # 'instagram_basic,instagram_manage_insights,pages_show_list'
            LOG_FILE = config['logging_file'][0]
            PAGE_ID = config['page_id'][0] # '#########'
            APP_SCOPE_USER_ID = config['app_scoped_user_id'][0] # '#########'

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f'Error loading configuration file: {e}')
        raise

    # Get Instagram secrets
    logging.debug('Reading Instagram secrets from files.')
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
        logging.error(f'Error reading Instagram secrets: {e}')
        raise

    return APP_TOKEN, APP_ID, USER_SHORT_TOKEN, USER_ID, HASHTAG, API_VERSION, CALLBACK_URI, API_SCOPE, USER_LONG_TOKEN, FILE_PATH, USER_SHORT_TOKEN_FILE, USER_LONG_TOKEN_FILE, LOG_FILE, PAGE_ID, CAMPAIGN_HASHTAG

def configure_logging():
    
    '''
    Configure logging to write to a file and to the console.
    '''
    
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

def getUserShortAccessToken():
    # Replace with your actual App ID and redirect URI
    app_id = get_config_data()[1]
    redirect_uri = get_config_data()[6]  # This should match your app settings in the Facebook Developer Console
    scopes = ','.join(get_config_data()[7])  # Join the list into a single comma-separated string
    api_version = get_config_data()[5]

    auth_url = f'https://www.facebook.com/{api_version}/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code'

    # Open the authorization URL in a browser to let the user grant permissions
    webbrowser.open(auth_url)

def get_page_token(user_access_token, page_id, api_version):
    # Use the user access token to get the page token for D2I
    url = f"https://graph.facebook.com/{api_version}/{page_id}"
    params = {
        'fields': 'access_token',
        'access_token': user_access_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        page_data = response.json()
        page_token = page_data.get('access_token')
        if page_token:
            print(f"Page Token: {page_token}")
            return page_token
        else:
            print("Page token not found.")
    else:
        print(f"Error getting page token: {response.status_code}, {response.text}")

    return None

import requests

def get_pages(user_access_token, api_version):
    """
    Retrieve the list of pages the user has access to.

    :param user_access_token: The User Access Token.
    :param api_version: API version to use.
    :return: None
    """
    # URL to access the /me/accounts endpoint
    url = f"https://graph.facebook.com/{api_version}/me/accounts"
    # Parameters with access token
    params = {
        'access_token': user_access_token
    }

    # Make the request to the API
    response = requests.get(url, params=params)
    
    # Log the response status and content for debugging
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    # If the request is successful, process the pages data
    if response.status_code == 200:
        pages_data = response.json().get('data', [])
        if pages_data:
            # Iterate through pages and print their details
            print("Pages found:")
            for page in pages_data:
                print(f"Page Name: {page['name']}, Page ID: {page['id']}")
        else:
            print("No pages found.")
    else:
        # Print error details if the request fails
        print(f"Error getting pages: {response.status_code}, {response.text}")

def get_pages_show_list(access_token, api_version):
    """
    Retrieve the list of pages the user has access to.

    :param access_token: The User Access Token.
    :param api_version: API version to use.
    :return: List of pages or None if not found.
    """
    url = f'https://graph.facebook.com/{api_version}/me/accounts'
    params = {
        'access_token': access_token
    }

    print(f"Making request to get pages with URL: {url} and params: {params}")
    response = requests.get(url, params=params)
    print(f"Response Status Code: {response.status_code}, Response Content: {response.text}")

    if response.status_code == 200:
        pages_data = response.json().get('data', [])
        if pages_data:
            print("Pages found:")
            for page in pages_data:
                print(f"Page ID: {page['id']}, Page Name: {page['name']}")
        else:
            print("No pages found.")
    else:
        print(f"Error retrieving pages: {response.status_code}, {response.text}")

def extract_hashtags(caption, stmhashtag, campaign_hashtag):
    '''
    Extract foundational and campaign hashtags from a given caption.

    :param caption: The text caption of the Instagram post.
    :param campaign_hashtag: The campaign hashtag from the configuration.
    :return: A tuple of (foundational_hashtag, campaign_hashtag) or (None, None) if not found.
    '''
    if not caption:
        print("Caption is empty. No hashtags to extract.")
        return None, None

    # Find all hashtags in the caption
    hashtags = re.findall(r"#\w+", caption)
    print(f"Extracted hashtags: {hashtags}")

    foundational_hashtag = None
    extracted_campaign_hashtag = None

    # Check for specific hashtags
    for tag in hashtags:
        tag_value = tag[1:]  # Remove the '#' symbol
        if tag_value == stmhashtag:
            foundational_hashtag = tag_value
        elif tag_value == campaign_hashtag:
            extracted_campaign_hashtag = tag_value

    return foundational_hashtag, extracted_campaign_hashtag

def format_timestamp(timestamp):
    '''Format ISO 8601 timestamp to BigQuery-compatible format.'''
    from datetime import datetime
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(f"Error formatting timestamp: {e}")
        return timestamp
    
if __name__ == "__main__":
    config_data = get_config_data()
    
    print("Running process to obtain short access token...")

    get_pages(config_data[8], config_data[5])
