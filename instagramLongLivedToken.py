import requests
import logging
import datetime
import os
#from instagram_api import get_config_data
from utils import get_config_data
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging to write to a file
#config_data = get_config_data()
# Load configuration data
config_data = get_config_data()

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_long_lived_access_token(app_id, app_secret, short_lived_token):
    """
    Exchange a short-lived token for a long-lived access token using the Facebook Graph API.
    
    :param app_id: Facebook App ID.
    :param app_secret: Facebook App Secret.
    :param short_lived_token: Short-lived access token obtained from the user.
    :return: Long-lived access token if successful, otherwise None.
    """
    # Retrieve the API version from configuration data
    #api_version = get_config_data()[5]
    api_version = config_data[5]
    logging.debug(f"API Version: {api_version}")  # Debug log

    # Construct the URL for the Facebook Graph API endpoint to exchange the token
    url = f"https://graph.facebook.com/{api_version}/oauth/access_token"
    logging.debug(f"Request URL: {url}")  # Debug log

    # Parameters needed for the token exchange request
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token
    }
    logging.debug(f"Request Parameters: {params}")  # Debug log

    # Make the request to the Facebook Graph API to exchange the token with retries
    try:
        response = requests_retry_session().get(url, params=params)
        logging.debug(f"Response Status Code: {response.status_code}")  # Debug log
        logging.debug(f"Response Content: {response.text}")  # Debug log

        # If the request is successful, extract and return the long-lived token
        if response.status_code == 200:
            long_lived_token = response.json().get('access_token')
            logging.debug(f"Long-Lived Access Token: {long_lived_token}")  # Debug log
            return long_lived_token
        else:
            logging.debug("Failed to get long-lived access token.")  # Debug log
            return None
    except requests.RequestException as e:
        logging.error(f"Error during request: {e}")
        return None

def save_long_lived_token(FILE_PATH, token):
    """
    Save the long-lived token to a file.
    
    :param FILE_PATH: The path to the file where the token will be saved.
    :param token: The long-lived token to be saved.
    """
    # Write the long-lived token to the specified file path
    try:
        with open(FILE_PATH, 'w') as file:
            file.write(token)
        logging.debug(f"Long-lived token saved to {FILE_PATH}")  # Debug log
    except Exception as e:
        logging.debug(f"Error saving long-lived token: {e}")  # Debug log

def check_and_refresh_token():
    """
    Check if the long-lived token needs to be refreshed based on the last refresh date.
    If more than 50 days have passed since the last refresh, refresh the token.
    """
    # Path to the file storing the last refresh date
    LAST_REFRESH_FILE = config_data[9] + "last_refresh_date.txt"
    logging.debug(f"Checking last refresh date from: {LAST_REFRESH_FILE}")

    # Determine if the token needs to be refreshed
    try:
        if os.path.exists(LAST_REFRESH_FILE):
            with open(LAST_REFRESH_FILE, 'r') as file:
                last_refresh_str = file.read().strip()
                last_refresh_date = datetime.datetime.strptime(last_refresh_str, "%Y-%m-%d")
                days_since_refresh = (datetime.datetime.now() - last_refresh_date).days
                logging.debug(f"Days since last token refresh: {days_since_refresh}")

                if days_since_refresh < 50:
                    logging.info("Token refresh not needed.")
                    return
        else:
            logging.debug("Last refresh date file not found. Proceeding with token refresh.")
    except Exception as e:
        logging.error(f"Error reading last refresh date: {e}")

    # Refresh the long-lived token
    logging.info("Refreshing long-lived token.")
    long_lived_token = config_data[8]  # Existing long-lived access token
    app_id = config_data[1]  # Facebook App ID
    refreshed_token = get_long_lived_access_token(long_lived_token, app_id)

    if refreshed_token:
        save_long_lived_token(config_data[9] + config_data[11], refreshed_token)
        # Update the last refresh date
        try:
            with open(LAST_REFRESH_FILE, 'w') as file:
                file.write(datetime.datetime.now().strftime("%Y-%m-%d"))
            logging.debug(f"Last refresh date updated to: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        except Exception as e:
            logging.error(f"Error updating last refresh date: {e}")
    else:
        logging.error("Failed to refresh long-lived token.")

def long_token_main_function():
    # Load configuration data
    config_data = get_config_data()

    # Extract the log file path and ensure it's a string
    log_file_path = config_data[12] if isinstance(config_data[12], list) else config_data[12]
    log_file_path = log_file_path + f"instagramLongLivedToken_logs_{datetime.datetime.now().strftime('%y%m%d%H%M%S')}.log"
    print(f"Log file path: {log_file_path}")  # Print for debugging purposes

    # Configure logging to write to a file
    logging.basicConfig(
        filename=log_file_path, 
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s', 
        filemode='w'
    )
    
    logging.debug(f"Configuration Data Loaded: {config_data}")  # Debug log
    
    # Extract app credentials and short-lived token from configuration
    app_id = config_data[1]  # Facebook App ID
    app_secret = config_data[0]  # Facebook App Secret
    short_lived_token = config_data[2]  # Short-lived access token
    logging.debug(f"App ID: {app_id}, App Secret: {app_secret}, Short-Lived Token: {short_lived_token}")  # Debug log
    
    # Define the path to save the long-lived token
    FILE_PATH = config_data[9] + config_data[11]
    logging.debug(f"File Path for Long-Lived Token: {FILE_PATH}")  # Debug log

    # Get the long-lived access token by exchanging the short-lived token
    long_lived_token = get_long_lived_access_token(app_id, app_secret, short_lived_token)
    
    # If a long-lived token is obtained, save it to the specified file
    if long_lived_token:
        save_long_lived_token(FILE_PATH, long_lived_token)
        logging.getLogger().handlers[0].flush()  # Force flush
    else:
        logging.debug("No long-lived token obtained.")  # Debug log
        logging.getLogger().handlers[0].flush()  # Force flush

if __name__ == "__main__":
    long_token_main_function()