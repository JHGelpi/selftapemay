import requests
from instagram_api import get_config_data

def get_long_lived_access_token(app_id, app_secret, short_lived_token):
    api_version = get_config_data()[5]
    #print ("api_version: ", api_version)

    url = f"https://graph.facebook.com/{api_version}/oauth/access_token"
    #print ("url: ", url)

    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token
    }
    #print ("params: ", params)

    response = requests.get(url, params=params)
    #print ("response: ", response)
    
    if response.status_code == 200:
        long_lived_token = response.json().get('access_token')
        #print(f"Long-Lived Access Token: {long_lived_token}")
        return long_lived_token
    else:
        #print(f"Error getting long-lived token: {response.status_code}, {response.text}")
        return None

def save_long_lived_token(FILE_PATH, token):
    """
    Save the long-lived token to a file.

    :param token: The long-lived token to be saved.
    """
    

    with open(FILE_PATH, 'w') as file:
        file.write(token)

if __name__ == "__main__":
    # Replace with your app credentials and short-lived token
    config_data = get_config_data()
    app_id = config_data[1]
    app_secret = config_data[0]
    short_lived_token = config_data[2]
    FILE_PATH = config_data[9] + config_data[11]

    long_lived_token = get_long_lived_access_token(app_id, app_secret, short_lived_token)

    save_long_lived_token(FILE_PATH, long_lived_token)

#print("Long lived token: ", long_lived_token)