from github_sync import Github
from github_sync import Auth
import os

# Importing create_node from the chintamani folder relative to this file
from ..chintamani.utils import create_chintamani_node
from ..chintamani.endpoints import insert_child

auth = Auth.Token(os.getenv("GITHUB_TOKEN"))

g = Github(auth=auth)

followers = g.get_user().get_followers()

for follower in followers:
    follower_node = create_chintamani_node(follower, "login")
    insert_child("FOLLOWER", follower_node, "GITHUB.FOLLOWERS", "USER")
    print(follower.login)

# following = g.get_user().get_following()

# for follow in following:
#     print(follow.login)

# repos = g.get_user().get_repos()

# for repo in repos:
#     print(repo.name)

# starred_repos = g.get_user().get_starred()

# for repo in starred_repos:
#     print(repo.name)
