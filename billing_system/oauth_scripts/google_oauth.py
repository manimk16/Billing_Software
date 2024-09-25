import requests
from requests_oauthlib import OAuth2Session
import os
import json

# Replace these with your actual credentials 
CLIENT_ID = "484398151029-lf22i1853m8ne6pffc4g68mdvnne3mdr.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8000/callback"  # Special URI for manual authorization code input
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPE = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]
TOKEN_FILE = "token.json"

def save_token(token):
    """Save the OAuth token to a JSON file."""
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token, f)
    print(f"Token saved to {TOKEN_FILE}")

def load_token():
    """Load the OAuth token from a JSON file if it exists."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            token = json.load(f)
        print(f"Token loaded from {TOKEN_FILE}")
        return token
    return None

def get_authorization_url():
    """Step 1: Get the Google authorization URL"""
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = oauth.authorization_url(AUTH_URI, access_type="offline", prompt="consent")
    print(f"Please go to this URL and authorize the app: {authorization_url}")
    return oauth

def get_access_token(oauth, authorization_response_code):
    """Step 2: Exchange authorization code for access token"""
    token = oauth.fetch_token(
        TOKEN_URI,
        code=authorization_response_code,  # Now passing the code directly
        client_secret=CLIENT_SECRET
    )
    save_token(token)  # Save the token for future use
    return token

if __name__ == "__main__": 
    # Step 0: Check if token.json already exists
    token = load_token()

    if not token:
        # Step 1: Direct the user to authenticate if no token exists
        oauth = get_authorization_url()

        # Step 2: After the user authorizes the app, they'll receive a code in the browser.
        authorization_response_code = input("Paste the authorization code here: ")

        # Step 3: Exchange the code for an access token
        token = get_access_token(oauth, authorization_response_code)
    
    print(f"Access token: {token}")
