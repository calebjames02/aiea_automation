from github import Github, Auth, Repository

with open("github_token.txt") as file:
    github_key = file.readline().strip()

# Initialize the client with a Personal Access Token (requires 'admin:org' scope)
auth = Auth.Token(github_key)
g = Github(auth=auth)
org = g.get_organization("AIEA-Automation-Test-Org")
user = g.get_user("calebjames02")
repos = user.get_repos()
for repo in repos:
#    if repo.full_name == "aiea-lab/aiea-lab.github.io":
    print(repo)
#org = g.get_organization("YOUR_ORG_NAME")
#team = org.get_team("YOUR_TEAM_SLUG")


# Add a member by their username or NamedUser object
# The 'role' parameter can be 'member' or 'maintainer'
member = g.get_user("greektimtom")
print(member)
#print(team.id)
#team = org.get_team("Test Team")
team = org.get_team_by_slug("test-team")
team.add_membership(member, role="member")

#team.add_membership(member, role="member")   