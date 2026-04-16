import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope required to read form responses
SCOPES = ['https://www.googleapis.com/auth/forms.responses.readonly']

# TODO: Replace with your actual Form ID
FORM_ID = '1CAFvAXgCLwEA1ltm_XZs3v2AyFY7pFi-4-JsaOjCRQI'

def main():
    creds = None
    
    # token.json stores your user's access and refresh tokens. It is created 
    # automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This triggers a browser window asking you to grant permissions
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=False)
            
        # Save the credentials for the next run so you don't have to log in every time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Build the Forms API service
        service = build('forms', 'v1', credentials=creds)

        # Call the Forms API to retrieve all responses
        print(f"Fetching responses for Form ID: {FORM_ID}...")
        result = service.forms().responses().list(formId=FORM_ID).execute()
        responses = result.get('responses', [])

        if not responses:
            print('No responses found.')
        else:
            print(f"Success! Found {len(responses)} response(s).")
            print("-" * 30)
            
            # Loop through and print the raw JSON of each response
            for response in responses:
                response_id = response.get('responseId')
                answers = response.get('answers')
                print(f"Response ID: {response_id}")
                print(f"Answers Data: {answers}\n")

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()