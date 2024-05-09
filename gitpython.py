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
    
    
from git import Repo

# Specify the path to your local git repository
repo_path = "/path/to/your/repo"
repo = Repo(repo_path)

# Check if the repository is valid and has remotes
if not repo.bare and repo.remotes:
    # Access the first remote (typically 'origin', but could be different)
    remote_name = 'origin' if 'origin' in repo.remotes else repo.remotes[0].name

    # Fetch the latest branches from the remote
    remote = repo.remotes[remote_name]
    remote.fetch()

    # Get all remote branches
    remote_branches = [ref.name for ref in remote.refs]

    # Print or use the list of remote branches
    print(remote_branches)
else:
    print("Could not load the repository or no remotes found.")