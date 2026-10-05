
# Project Title

This Python program is used to add users to a GitHub organization that have responded to a particular Google Form.




# Installation

Install all packages with pip. Use Python 3.12+

```bash
  pip install -r requirements.txt
```
    
# Setup

## Google Form

Create the Google Form that will be used by the application and retrieve its Form ID.

1. Create a new form in [Google Forms](https://forms.google.com/).
2. Add a question with a text entry box asking for the user's GitHub username.
3. Publish the form and open the form in your browser.
4. The **Form ID** can be found in the URL:

   ```text
   https://docs.google.com/forms/d/FORM_ID/edit
   ```

5. Copy the value between `/d/` and `/edit`. This is the **Form ID**.
6. Add the Form ID to the `FORM_ID` variable in the program.

> **Note:** The Form ID is not a secret and does not need to be treated as a credential.

## Google Developer Console

Follow these steps to configure the Google API credentials needed by the application.

### 1. Create a Google Cloud Project

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Select the newly created project before continuing.

### 2. Enable the Google Forms API

1. Navigate to **APIs & Services → Library**.
2. Search for **Google Forms API**.
3. Select it and click **Enable**.

### 3. Configure the OAuth Consent Screen

1. Go to **APIs & Services → OAuth consent screen**.
2. Click **Get started**.
3. Follow the setup steps and provide the requested application information.
4. Complete the consent screen configuration.

### 4. Create OAuth Client Credentials

1. Go to **APIs & Services → Credentials**.
2. Select **Create Credentials → OAuth client ID**.
3. Set the application type to **Desktop app**.
4. Create the OAuth client.
5. Download the resulting JSON credentials file.
6. Place the downloaded JSON credentials file in the project's `secrets` directory as `client_secrets.json`.

> **Important:** Do not commit the credentials JSON file to Git. Make sure the `secrets` directory is included in `.gitignore`.

### 5. Add Test Users

If the application is still in testing mode, users must be explicitly added as test users.

1. Go to **Google Auth Platform → Audience**.
2. Find the **Test users** section.
3. Click **Add users**.
4. Add the Google accounts that need access to the application.

## GitHub Personal Access Token

A GitHub Personal Access Token (PAT) is required for the application to authenticate with GitHub.

1. Sign in to [GitHub](https://github.com/).
2. Click your profile picture → **Settings**.
3. Select **Developer settings** at the bottom of the sidebar.
4. Select **Personal access tokens**.
5. Choose **Tokens (classic)**.
6. Create a new token.
7. Give the token an appropriate name and expiration date.
8. Grant only the permissions required by the application.
9. Click **Generate token**.
10. **Copy the token immediately.** GitHub will not show the full token again.
11. Store the token in the `secrets/github_token.txt` file.

> **Important:** Never commit the GitHub token to the repository or share it publicly. If a token is accidentally exposed, revoke it immediately and create a new one.
# Usage/Examples

Once you have created and configured the Google Form and Google Cloud project, and created a GitHub personal access token, you are ready to run the program.

Run the program with:

```bash
python3 forms.py
```

### First Run

The first time you run the program, you will be prompted to authenticate the application:

1. Open the link provided in the terminal.
2. Sign in with the Google account you are using.
3. Follow the prompts to authorize the application.

After authentication, the program will continue running normally.

### Subsequent Runs

Each time the program is run, it checks for new Google Form responses since the previous run and attempts to add the submitted GitHub usernames to the organization.
