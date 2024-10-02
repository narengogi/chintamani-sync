from github_sync import Github
from github_sync import Auth
import os

from chintamani.utils import create_chintamani_node
from chintamani.endpoints import insert_child


class GitHubSync:
    def __init__(self):
        self.auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
        self.g = Github(auth=self.auth)

    def sync_followers(self):
        followers = self.g.get_user().get_followers()
        for follower in followers:
            follower_node = create_chintamani_node(data=follower, key="login")
            insert_child(parent_id="GITHUB.USER", child_id=follower_node, child_type="FOLLOWER")
            print(follower.login)

    def sync_following(self):
        following = self.g.get_user().get_following()
        for follow in following:
            print(follow.login)

    def sync_repos(self):
        repos = self.g.get_user().get_repos()
        for repo in repos:
            print(repo.name)

    def sync_starred_repos(self):
        starred_repos = self.g.get_user().get_starred()
        for repo in starred_repos:
            print(repo.name)
