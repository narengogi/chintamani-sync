from github_sync.api_sync import GitHubSync
from mozilla.sqlite_sync import SQLiteSync

def sync_github():
    github_sync = GitHubSync()
    github_sync.sync_followers()
    github_sync.sync_following()
    github_sync.sync_repos()
    github_sync.sync_starred_repos()

def sync_mozilla():
    mozilla_sync = SQLiteSync()
    mozilla_sync.sync_origins()
    mozilla_sync.exit()

if __name__ == "__main__":
    # sync_github()
    sync_mozilla()
