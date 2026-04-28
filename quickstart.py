import os.path
import json
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone

TIME_FILE = "time.txt"

def load_time():
    # If SETTINGS_FILE already exists, extract current settings from it
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE, "r") as f:
#            current = json.load(f)
            line = f.readline()
            return line.strip()

def save_time(time):
    # Save current version of settings back to SETTINGS_FILE
    with open(TIME_FILE, "w") as f:
        f.write(time)
#        json.dump(settings, f, indent=4)

# Scope required to read form responses
SCOPES = ['https://www.googleapis.com/auth/forms.responses.readonly']

# TODO: Replace with your actual Form ID
FORM_ID = '1CAFvAXgCLwEA1ltm_XZs3v2AyFY7pFi-4-JsaOjCRQI'

class ResponseChecker():
    def __init__(self):
        self.creds = None
        
        # token.json stores your user's access and refresh tokens. It is created 
        # automatically when the authorization flow completes for the first time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If there are no valid credentials available, let the user log in.
        # This isn't working?????
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # This triggers a browser window asking you to grant permissions
                flow = InstalledAppFlow.from_client_secrets_file(
                    'secrets/client_secrets.json', SCOPES)
                self.creds = flow.run_local_server(port=8080, open_browser=False)
                
            # Save the credentials for the next run so you don't have to log in every time
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def find_responses(self):
        try:
            # Build the Forms API service
            service = build('forms', 'v1', credentials=self.creds)

            # Call the Forms API to retrieve all responses
            print(f"Fetching responses for Form ID: {FORM_ID}...")
            result = service.forms().responses().list(formId=FORM_ID, filter=f"timestamp > {load_time()}").execute()
            responses = result.get('responses', [])

            if not responses:
                print('No responses found.')
            else:
                print(f"Success! Found {len(responses)} response(s).")
                print("-" * 30)
                
                # Loop through and print the raw JSON of each response
                for response in responses:
                    print(response['lastSubmittedTime'])
                    response_id = response.get('responseId')
                    answers = response.get('answers')
                    print(f"Response ID: {response_id}")
                    print(f"Answers Data: {answers}\n")

            # Update time of most recent check
            save_time(datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))

        except Exception as e:
            print(f'An error occurred: {e}')

check = ResponseChecker()
while 1:
    check.find_responses()
    time.sleep(5)