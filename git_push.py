import sys
import git
import os
import re

def convert_https_to_ssh(url):
    """Convert HTTPS GitHub URL to SSH format."""
    match = re.match(r'https://github.com/(.*)', url)
    if match:
        return f'git@github.com:{match.group(1)}.git'
    return url

def push_to_new_repo(repo_url, branch_name):
    """Pushes code to the specified remote repository and branch."""
    repo_url = convert_https_to_ssh(repo_url)
    print(f"Converting HTTPS URL to SSH format: {repo_url}")

    repo_path = os.getcwd()
    print(f"Using existing git repository in {repo_path}...")

    try:
        repo = git.Repo(repo_path)
    except git.exc.InvalidGitRepositoryError:
        print("Error: No Git repository found. Initialize one first.")
        sys.exit(1)

    print("Adding all files to the repository...")
    repo.git.add('--all')

    print("Committing changes...")
    repo.git.commit('-m', 'Automated commit')

    remote_name = 'origin'

    if remote_name in [remote.name for remote in repo.remotes]:
        remote = repo.remote(remote_name)
        print(f"Remote '{remote_name}' already exists with correct URL: {repo_url}")
    else:
        remote = repo.create_remote(remote_name, repo_url)
        print(f"Added remote '{remote_name}' with URL: {repo_url}")

    print(f"Setting up branch {branch_name}...")
    if branch_name not in repo.heads:
        repo.git.checkout('-b', branch_name)
    else:
        repo.git.checkout(branch_name)

    print("Fetching latest changes from remote repository...")
    try:
        repo.git.fetch('origin', branch_name)
        print("Merging remote changes into the local branch...")
        repo.git.pull('origin', branch_name, '--rebase')
    except git.GitCommandError as e:
        print("\nError while pulling remote changes: ", e)
        print("Possible solutions:")
        print("- If you have uncommitted changes, stash them: git stash")
        print("- Try pulling again: git pull --rebase origin", branch_name)
        print("- If there are merge conflicts, resolve them manually.")
        sys.exit(1)

    print("Pushing to remote repository using SSH authentication...")
    try:
        repo.git.push('-u', 'origin', branch_name)
        print(f"Files have been successfully pushed to {repo_url} on branch {branch_name}")
    except git.GitCommandError as e:
        print(f"Git push failed: {e}")
        print("Try resolving conflicts or force pushing with caution: git push -f origin", branch_name)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 git_push.py <repository_url> <branch_name>")
        sys.exit(1)

    repo_url = sys.argv[1]
    branch_name = sys.argv[2]
    push_to_new_repo(repo_url, branch_name)
