from git import Repo

# Specify the path to your local git repository
repo_path = "/path/to/your/repo"
repo = Repo(repo_path)

# Ensure the repository is valid
if not repo.bare:
    # Fetch the latest branches from the remote
    repo.remotes.origin.fetch()

    # Get all remote branches
    remote_branches = [ref.name for ref in repo.remotes.origin.refs]

    # Print or use the list of remote branches
    print(remote_branches)
else:
    print("Could not load the repository.")