import os
import sys
import git
import subprocess

def push_to_github(repo_path, branch_name, repo_url, is_ssh=True):
    try:
        repo = git.Repo(repo_path)
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: The specified path '{repo_path}' is not a valid Git repository.")
        sys.exit(1)
    
    # Add all changes
    print("Adding changes to staging area...")
    repo.git.add(all=True)
    
    # Commit changes
    commit_message = "Auto-commit"
    try:
        repo.git.commit('-m', commit_message)
        print("Changes committed successfully.")
    except git.GitCommandError as e:
        print("No changes to commit or error while committing.")
        print(e)
    
    # Ensure correct branch is checked out
    if repo.active_branch.name != branch_name:
        print(f"Switching to branch '{branch_name}'")
        try:
            repo.git.checkout(branch_name)
        except git.GitCommandError as e:
            print(f"Error switching to branch {branch_name}: {e}")
            sys.exit(1)
    
    # Authenticate SSH if needed
    if is_ssh:
        print("Testing SSH connection...")
        github_domain = repo_url.split('@')[1].split(':')[0]
        try:
            result = subprocess.run(['ssh', '-T', f'git@{github_domain}'], capture_output=True, text=True)
            if "successfully authenticated" in result.stderr or "You've successfully authenticated" in result.stderr:
                print("SSH authentication successful!")
            else:
                print("SSH connection test result:")
                print(result.stderr)
        except Exception as e:
            print(f"SSH test failed: {e}")
            print("Continuing anyway...")
    
    # Pull latest changes before pushing
    try:
        print("Pulling latest changes before pushing...")
        repo.git.pull('--rebase', 'origin', branch_name)
    except git.GitCommandError as e:
        print("Error while pulling. If there are conflicts, resolve them manually before pushing.")
        print(e)
        sys.exit(1)
    
    # Push to remote repository
    try:
        print("Pushing to remote repository...")
        repo.git.push('-u', 'origin', branch_name)
        print(f"Files have been successfully pushed to {repo_url} on branch {branch_name}")
    except git.GitCommandError as e:
        print("Push failed! If the error suggests a non-fast-forward push, you may need to force push.")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    repo_path = os.getcwd()  # Current working directory
    branch_name = "main"  # Change if using a different branch
    repo_url = "git@github.com:username/repository.git"  # Replace with your repo URL
    is_ssh = True  # Set to False if using HTTPS authentication
    
    push_to_github(repo_path, branch_name, repo_url, is_ssh)
