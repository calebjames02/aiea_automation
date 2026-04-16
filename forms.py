from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

# Path to your downloaded client_secret.json
CLIENT_SECRET_FILE = 'secrets/client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/forms.body.readonly']

# Step 1: Get credentials
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
creds = flow.run_local_server(port=0, open_browser=False)  # Opens a browser to authorize

# Step 2: Use the access token in your request
formId = "1CAFvAXgCLwEA1ltm_XZs3v2AyFY7pFi-4-JsaOjCRQI"
headers = {
    "Authorization": f"Bearer {creds.token}"
}

response = requests.get(f"https://forms.googleapis.com/v1/forms/{formId}", headers=headers)
print(response.status_code)
print(response.json())