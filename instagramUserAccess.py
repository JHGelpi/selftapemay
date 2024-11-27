import webbrowser
from instagram_api import getConfigData
def getUserAccessToken():
    # Replace with your actual App ID and redirect URI
    app_id = getConfigData()[1]
    redirect_uri = getConfigData()[6]  # This should match your app settings in the Facebook Developer Console
    #scopes = getConfigData()[7]
    scopes = ','.join(getConfigData()[7])  # Join the list into a single comma-separated string
    api_version = getConfigData()[5]

    auth_url = f'https://www.facebook.com/{api_version}/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code'

    # Open the authorization URL in a browser to let the user grant permissions
    print (auth_url)
    webbrowser.open(auth_url)


if __name__ == "__main__":
    getUserAccessToken()