from github import Github, Auth, Repository

with open("github_token.txt") as file:
    github_key = file.readline().strip()

auth = Auth.Token(github_key)
g = Github(auth=auth)
org = g.get_organization("aiea-lab")

member = g.get_user("greektimtom")

team = org.get_team_by_slug("AIEA-auditors")
team.add_membership(member, role="member")   