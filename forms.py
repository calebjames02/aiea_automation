import os.path
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone
from github import Github, Auth, Repository

TIME_FILE = "time.txt"

def load_time():
    # If TIME_FILE already exists, extract previous timestamp from it
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE, "r") as f:
            line = f.readline()
            return line.strip()

    # If TIME_FILE doesn't exist return default time
    # This should only happen the first time the program is run so the default time given should find all existing form responses
    date_string = "2000-01-01T00:00:00.000000Z"
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    datetime_object = datetime.strptime(date_string, date_format).replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
    print(datetime_object)

    return datetime_object

def save_time(time):
    # Save given timestamp back to TIME_FILE
    with open(TIME_FILE, "w") as f:
        f.write(time)

# Scope required to read form responses
SCOPES = ['https://www.googleapis.com/auth/forms.responses.readonly']

# TODO: Replace with your actual Form ID
FORM_ID = '1CAFvAXgCLwEA1ltm_XZs3v2AyFY7pFi-4-JsaOjCRQI'

class ResponseChecker():
    def __init__(self):
        self.creds = None

        with open("github_token.txt") as file:
            github_key = file.readline().strip()
        auth = Auth.Token(github_key)
        self.g = Github(auth=auth)
        self.org = self.g.get_organization("AIEA-Automation-Test-Org")
#        self.org = self.g.get_organization("aiea-lab")
        
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
        # Build the Forms API service
        service = build('forms', 'v1', credentials=self.creds)

        # Call the Forms API to retrieve all responses
        print(f"Fetching responses for Form ID: {FORM_ID}...")

        time = load_time()
        print(time)
        result = service.forms().responses().list(formId=FORM_ID, filter=f"timestamp > {time}").execute()
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

                for question_id in answers:
                    username = response.get('answers')[question_id].get('textAnswers')['answers'][0].get('value')

                try:
                    member = self.g.get_user(username)
                except:
                    print(f"User {username} is not a valid Github username")
                    save_time(datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
                    continue

                team_name = "Test"
                try:
                    team = self.org.get_team_by_slug(team_name)
                except:
                    print(f"Team name '{team_name}' does not exist in the {self.org.name} organization")
                    continue

                try:
                    team.add_membership(member, role="member")
                except Exception as e:
                    print(f"Assigning member '{member}' to team '{team_name}' failed")

                # Update time of most recent check
                save_time(datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))

check = ResponseChecker()
while 1:
    check.find_responses()
    time.sleep(5)