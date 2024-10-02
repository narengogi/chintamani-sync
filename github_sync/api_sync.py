from github import Github
from github import Auth
import os
import json

from chintamani.utils import create_chintamani_node
from chintamani.endpoints import insert_child


class GitHubSync:
    def __init__(self):
        self.auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
        self.g = Github(auth=self.auth)

    def sync_followers(self):
        followers = self.g.get_user().get_followers()
        for follower in followers:
            print("syncing follower", follower.login)
            json_obj = {'email': follower.email, 'login': follower.login,
                         'name': follower.name, 'bio': follower.bio, 'location': follower.location,
                         'blog': follower.blog, 'company': follower.company, 'created_at': follower.created_at.isoformat()
                        }
            follower_node = create_chintamani_node(data=json_obj, label_key="login")
            insert_child(child_label="USER", child_json=follower_node, parent_path="GITHUB.FOLLOWERS", relationship="FOLLOWER")
            print("synced follower", follower.login)

    def sync_following(self):
        following = self.g.get_user().get_following()
        for follow in following:
            print("syncing following", follow.login)
            json_obj = {'email': follow.email, 'login': follow.login,
                         'name': follow.name, 'bio': follow.bio, 'location': follow.location,
                         'blog': follow.blog, 'company': follow.company, 'created_at': follow.created_at.isoformat()
                        }
            follower_node = create_chintamani_node(data=json_obj, label_key="login")
            insert_child(child_label="USER", child_json=follower_node, parent_path="GITHUB.FOLLOWING", relationship="FOLLOWING")
            print("synced following", follow.login)

    def sync_repos(self):
        repos = self.g.get_user().get_repos()
        for repo in repos:
            print("syncing repo", repo.name)
            json_obj = {'name': repo.name, 'description': repo.description, 'language': repo.language,
                        'created_at': repo.created_at.isoformat()}
            repo_node = create_chintamani_node(data=json_obj, label_key="name")
            insert_child(child_label="REPO", child_json=repo_node, parent_path="GITHUB.REPOS", relationship="REPO")
            print("synced repo", repo.name)

    def sync_starred_repos(self):
        print("syncing starred repos")
        starred_repos = self.g.get_user().get_starred()
        for repo in starred_repos:
            print("syncing starred repo", repo.name)
            json_obj = {'name': repo.name, 'description': repo.description, 'language': repo.language,
                        'created_at': repo.created_at.isoformat()}
            repo_node = create_chintamani_node(data=json_obj, label_key="name")
            insert_child(child_label="REPO", child_json=repo_node, parent_path="GITHUB.STARRED_REPOS", relationship="STARRED_REPO")
            print("synced starred repo", repo.name)
        print("synced starred repos")

# Usage:
# github_sync = GitHubSync()
# github_sync.sync_followers()
# github_sync.sync_following()
# github_sync.sync_repos()
# github_sync.sync_starred_repos()
