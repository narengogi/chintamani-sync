from github_sync.api_sync import GitHubSync

if __name__ == "__main__":
    github_sync = GitHubSync()
    github_sync.sync_followers()
    github_sync.sync_following()
    github_sync.sync_repos()
    github_sync.sync_starred_repos()