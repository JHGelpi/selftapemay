from flask import Flask, request
import requests
#import json
from instagram_api import get_config_data

app = Flask(__name__)

@app.route('/selftapemay/callback')
def callback():
    # Extract the authorization code from the request
    code = request.args.get('code')
    if code:
        #print(f"Authorization Code: {code}")

        # Exchange the authorization code for an access token
        access_token = exchange_code_for_access_token(code)
        if access_token:
            save_short_lived_token(access_token)
            #print(f"Access Token: {access_token}")
    else:
        print("Authorization code not received.")
    return "Authorization process completed. You can close this window."

def exchange_code_for_access_token(code):
    """
    Exchange the authorization code for a short-liged access token.
    """
    config = get_config_data()
    app_id = config[1]
    app_secret = config[0]
    redirect_uri = config[6]
    api_version = config[5]

    """
    print("app_id: ", app_id)
    print("app_secret: ", app_secret)
    print("redirect_uri: ", redirect_uri)
    print("api_version: ", api_version)
    """

    url = f"https://graph.facebook.com/{api_version}/oauth/access_token"
    # print("url: ", url)
    # https://graph.facebook.com/v21.0/oauth/access_token

    params = {
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Error getting access token: {response.status_code}, {response.text}")
        return None
def save_short_lived_token(token):
    """
    Save the short-lived token to a file.

    :param token: The short-lived token to be saved.
    """
    FILE_PATH = get_config_data()[9] + get_config_data()[10]

    with open(FILE_PATH, 'w') as file:
        file.write(token)

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == "__main__":
    cert_path = "/home/wesgelpi/self_tape_may/flask_app/certs/"
    app.run(host='0.0.0.0', port=5000, ssl_context=(f'{cert_path}cert.pem', f'{cert_path}key.pem'))  # Make it accessible to the network
