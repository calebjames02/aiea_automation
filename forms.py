import os.path
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone
from github import Github, Auth

TIME_FILE = "time.txt"

def load_time():
    # If TIME_FILE already exists, extract previous timestamp from it
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE, "r") as f:
            line = f.readline()
            return line.strip()

    # If TIME_FILE doesn't exist return default time
    # This should only happen the first time the program is run so the default time given should find all existing form responses
    return "2000-01-01T00:00:00Z"

def save_time(timestamp):
    # Save given timestamp back to TIME_FILE
    with open(TIME_FILE, "w") as f:
        f.write(timestamp)

def get_github():
    with open("secrets/github_token.txt") as file:
        github_key = file.readline().strip()

    github = Github(auth=Auth.Token(github_key))
    return github

def get_google_credentials():
    creds = None

    # token.json stores your user's access and refresh tokens. It is created automatically when the authorization flow completes for the first time.
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

    return creds

def get_responses(service, timestamp):
    # Load responses that are more recent than the given timestamp
    result = service.forms().responses().list(
        formId=FORM_ID,
        filter=f"timestamp > {timestamp}"
    ).execute()

    return result.get("responses", [])

# Scope required to read form responses
# DON'T CHANGE THIS
SCOPES = ['https://www.googleapis.com/auth/forms.responses.readonly']

# Replace with your Form ID
FORM_ID = '1WFNOAAi5jgT7V7kpedc9P_D8xz6i4JYVIbJQ96WTa5Q'

def main():
    # Authenticate
    g = get_github()
    org = g.get_organization("AIEA-Automation-Test-Org")

    creds = get_google_credentials()
    service = build('forms', 'v1', credentials=creds)

    # Call the Forms API to retrieve all responses
    print(f"Fetching responses for Form ID: {FORM_ID}...")

    # Load timestamp
    timestamp = load_time()
    print(timestamp)

    responses = get_responses(service, timestamp)

    # Save time of most recent check
    save_time(datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))

    successful_usernames = []
    failed_usernames = []
    if not responses:
        print('No responses found.')
    else:
        print(f"Success! Found {len(responses)} response(s).")
        print("-" * 30)

        # Check that specified team exists
        team_name = "Test-Team"
        try:
            team = org.get_team_by_slug(team_name)
        except:
            sys.exit(f"Team name '{team_name}' does not exist in the {org.name} organization")
            return

        # Loop through each response and attempt to add the user
        for response in responses:
            print(response['lastSubmittedTime'])
            response_id = response.get('responseId')
            answers = response.get('answers')
            print(f"Response ID: {response_id}")

            # Extract username from answers
            for question_id in answers:
                username = response.get('answers')[question_id].get('textAnswers')['answers'][0].get('value')

            print(f"Username: {username}\n")

            # Check if given username is valid
            try:
                member = g.get_user(username)
            except:
                failed_usernames.append((username, response['lastSubmittedTime'], f"User {username} is not a valid Github username"))
                continue

            # Try adding user to organization
            try:
                team.add_membership(member, role="member")
            except Exception as e:
                failed_usernames.append((username, response['lastSubmittedTime'], f"Assigning member '{member}' to team '{team_name}' failed"))
                continue

            # If nothing has failed then the user was added successfully
            successful_usernames.append((username, response['lastSubmittedTime']))

    if successful_usernames:
        # Print successful invites
        print("\n------------------------------")
        print("Invite sent to:")

        for username, time in successful_usernames:
            print(f"Username: {username}. \nSubmitted at : {time}\n")

    if failed_usernames:
        # Print failed invites and the reason why they failed
        print("\n------------------------------")
        print("Failed usernames:")

        for username, time, reason in failed_usernames:
            print(f"Username: {username}. \nSubmitted at: {time}\nReason: {reason}\n")

if __name__ == "__main__":
    main()