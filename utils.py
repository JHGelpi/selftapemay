import logging
import json
import datetime
import webbrowser
import requests

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
            USER_ID = config['bus_acct_userID'][0] # 'wgelpi'
            HASHTAG = config['hashtag'][0] # 'coke'
            CALLBACK_URI = config['callback_uri'][0] # ''
            API_SCOPE = config['scopes'] # 'instagram_basic,instagram_manage_insights,pages_show_list'
            LOG_FILE = config['logging_file'][0]
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

    return APP_TOKEN, APP_ID, USER_SHORT_TOKEN, USER_ID, HASHTAG, API_VERSION, CALLBACK_URI, API_SCOPE, USER_LONG_TOKEN, FILE_PATH, USER_SHORT_TOKEN_FILE, USER_LONG_TOKEN_FILE, LOG_FILE

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
        
if __name__ == "__main__":
    config_data = get_config_data()
    '''
    print("Running process to obtain short access token...")
    getUserShortAccessToken()
    '''
    print("Running the get_pages_show_list API call")
    get_pages_show_list(config_data[8], config_data[5])