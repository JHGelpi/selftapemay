import webbrowser
from instagram_api import get_config_data
def getUserAccessToken():
    # Replace with your actual App ID and redirect URI
    app_id = get_config_data()[1]
    redirect_uri = get_config_data()[6]  # This should match your app settings in the Facebook Developer Console
    scopes = ','.join(get_config_data()[7])  # Join the list into a single comma-separated string
    api_version = get_config_data()[5]

    auth_url = f'https://www.facebook.com/{api_version}/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code'

    # Open the authorization URL in a browser to let the user grant permissions
    webbrowser.open(auth_url)


if __name__ == "__main__":
    getUserAccessToken()