import requests
import logging
from instagram_api import get_config_data

# Configure logging to write to a file
config_data = get_config_data()
log_file_path = config_data[12]  # Assuming the log file path is provided as a list, extract the first element
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

def get_long_lived_access_token(app_id, app_secret, short_lived_token):
    """
    Exchange a short-lived token for a long-lived access token using the Facebook Graph API.
    
    :param app_id: Facebook App ID.
    :param app_secret: Facebook App Secret.
    :param short_lived_token: Short-lived access token obtained from the user.
    :return: Long-lived access token if successful, otherwise None.
    """
    # Retrieve the API version from configuration data
    api_version = get_config_data()[5]
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

    # Make the request to the Facebook Graph API to exchange the token
    response = requests.get(url, params=params)
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

if __name__ == "__main__":
    # Load configuration data
    config_data = get_config_data()
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
    else:
        logging.debug("No long-lived token obtained.")  # Debug log