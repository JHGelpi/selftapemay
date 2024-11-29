import logging
from flask import Flask, request
import requests
from instagram_api import get_config_data

# Configure logging to write to a file
config_data = get_config_data()
log_file_path = config_data[12]  # Assuming the log file path is provided as a list, extract the first element
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

app = Flask(__name__)

@app.route('/selftapemay/callback')
def callback():
    """
    Endpoint for handling the callback from Instagram authorization flow.
    Extracts the authorization code and exchanges it for an access token.
    """
    # Extract the authorization code from the request
    code = request.args.get('code')
    if code:
        logging.debug("Authorization code received.")  # Debug log
        # Exchange the authorization code for an access token
        access_token = exchange_code_for_access_token(code)
        if access_token:
            logging.debug("Access token successfully obtained.")  # Debug log
            save_short_lived_token(access_token)
        else:
            logging.error("Failed to obtain access token.")  # Error log
    else:
        logging.error("Authorization code not received.")  # Error log
    return "Authorization process completed. You can close this window."

def exchange_code_for_access_token(code):
    """
    Exchange the authorization code for a short-lived access token using the Facebook Graph API.
    
    :param code: Authorization code obtained from the Instagram callback.
    :return: Short-lived access token if successful, otherwise None.
    """
    config = get_config_data()
    app_id = config[1]  # Facebook App ID
    app_secret = config[0]  # Facebook App Secret
    redirect_uri = config[6]  # Redirect URI
    api_version = config[5]  # API version

    # Construct the URL for the Facebook Graph API endpoint to exchange the code
    url = f"https://graph.facebook.com/{api_version}/oauth/access_token"
    logging.debug(f"Request URL: {url}")  # Debug log

    # Parameters needed for the token exchange request
    params = {
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    logging.debug(f"Request Parameters: {params}")  # Debug log

    # Make the request to the Facebook Graph API to exchange the code
    response = requests.get(url, params=params)
    logging.debug(f"Response Status Code: {response.status_code}")  # Debug log
    logging.debug(f"Response Content: {response.text}")  # Debug log

    # If the request is successful, extract and return the short-lived token
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        logging.debug(f"Access Token: {access_token}")  # Debug log
        return access_token
    else:
        logging.error(f"Error getting access token: {response.status_code}, {response.text}")  # Error log
        return None

def save_short_lived_token(token):
    """
    Save the short-lived token to a file.
    
    :param token: The short-lived token to be saved.
    """
    FILE_PATH = get_config_data()[9] + get_config_data()[10]  # Path to save the token
    try:
        with open(FILE_PATH, 'w') as file:
            file.write(token)
        logging.debug(f"Short-lived token saved to {FILE_PATH}")  # Debug log
    except Exception as e:
        logging.error(f"Error saving short-lived token: {e}")  # Error log

@app.route('/favicon.ico')
def favicon():
    """
    Handle requests for favicon.ico to prevent unnecessary errors.
    """
    return '', 204

if __name__ == "__main__":
    # Define the path for SSL certificates
    cert_path = "/home/wesgelpi/self_tape_may/flask_app/certs/"
    logging.debug("Starting Flask server with SSL context.")  # Debug log
    # Run the Flask server with SSL context for secure communication
    app.run(host='0.0.0.0', port=5000, ssl_context=(f'{cert_path}cert.pem', f'{cert_path}key.pem'))  # Make it accessible to the network
