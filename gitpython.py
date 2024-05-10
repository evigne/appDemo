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
    
    
import gitlab

# Replace with your GitLab server URL and personal access token
GITLAB_URL = 'https://gitlab.com'
ACCESS_TOKEN = 'your_personal_access_token'
PROJECT_ID = 'your_project_id'  # Replace with the numeric project ID

# Initialize the GitLab connection
gl = gitlab.Gitlab(url=GITLAB_URL, private_token=ACCESS_TOKEN)

# Retrieve the specific project
project = gl.projects.get(PROJECT_ID)

# Retrieve all branches in the project
branches = project.branches.list(all=True)

# Extract the branch names
branch_names = [branch.name for branch in branches]

# Print or use the list of branch names
print(branch_names)



import gitlab
from urllib.parse import urlparse

# Replace with your GitLab server URL and personal access token
GITLAB_URL = 'https://gitlab.com'
ACCESS_TOKEN = 'your_personal_access_token'
REPO_URL = 'https://gitlab.com/group/project-name'  # Replace with your repo URL

# Extract the group and project name from the URL
parsed_url = urlparse(REPO_URL)
_, group, project_name = parsed_url.path.strip('/').split('/')

# Initialize GitLab API connection
gl = gitlab.Gitlab(url=GITLAB_URL, private_token=ACCESS_TOKEN)

# Retrieve the project using the namespace (group/project-name format)
project_namespace = f"{group}/{project_name}"
project = gl.projects.get(project_namespace)

# Fetch all branches in the project
branches = project.branches.list(all=True)

# Extract the branch names
branch_names = [branch.name for branch in branches]

# Print or use the list of branch names
print(branch_names)


import subprocess

# Replace this with the HTTPS URL of your Git repository
repo_url = "https://github.com/user/repo.git"

# Use subprocess to execute the git command
try:
    output = subprocess.check_output(['git', 'ls-remote', '--heads', repo_url], text=True)
    # Parse the output to extract branch names
    branches = [line.split('\t')[1].replace('refs/heads/', '') for line in output.strip().split('\n')]

    # Print the list of branches
    print("Branches:")
    for branch in branches:
        print(branch)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running git command: {e}")
