from flask import Flask, request

app = Flask(__name__)

@app.route('/selftapemay/callback')
def callback():
    # Extract the authorization code from the request
    code = request.args.get('code')
    if code:
        print(f"Authorization Code: {code}")
        # You can now use the authorization code to get the access token
        # Add your logic here to proceed
    else:
        print("Authorization code not received.")
    return "Authorization process completed. You can close this window."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Make it accessible to the network
