#!/usr/bin/env python3

import os
import sys
import git

def push_to_new_repo(repo_url, branch_name='main'):
    """
    Initialize a new git repository and push all files to it.
    
    Args:
        repo_url (str): URL of the remote repository
        branch_name (str): Name of the branch (default: 'main')
    """
    try:
        # Get current directory
        current_dir = os.getcwd()
        
        # Check if git is already initialized
        try:
            repo = git.Repo(current_dir)
            print(f"Using existing git repository in {current_dir}...")
        except git.exc.InvalidGitRepositoryError:
            print(f"Initializing a new git repository in {current_dir}...")
            repo = git.Repo.init(current_dir)
        
        print("Adding all files to the repository...")
        repo.git.add(all=True)
        
        # Check if there are changes to commit
        if repo.is_dirty() or len(repo.untracked_files) > 0:
            print("Committing changes...")
            repo.git.commit('-m', 'Initial commit')
        else:
            print("No changes to commit.")
        
        # Check if remote 'origin' already exists
        try:
            origin = repo.remote('origin')
            print("Remote 'origin' already exists. Updating URL...")
            repo.git.remote('set-url', 'origin', repo_url)
        except ValueError:
            print("Setting remote repository URL...")
            origin = repo.create_remote('origin', repo_url)
        
        print(f"Setting up branch {branch_name}...")
        # Check if branch exists
        try:
            repo.git.branch('-M', branch_name)
        except git.GitCommandError:
            # If renaming fails, create the branch
            repo.git.checkout('-b', branch_name)
        
        print("Pushing to remote repository...")
        repo.git.push('-u', 'origin', branch_name)
        
        print(f"Files have been successfully pushed to {repo_url} on branch {branch_name}")
        
    except git.GitCommandError as e:
        print(f"Git error: {e}")
        print("\nDetailed error information:")
        print(f"Command: {e.command}")
        print(f"Status: {e.status}")
        print(f"Stderr: {e.stderr}")
        
        # Provide helpful suggestions based on common errors
        if "Permission denied" in str(e):
            print("\nSuggestion: Check your authentication credentials. You might need to set up SSH keys or use a personal access token.")
        elif "already exists" in str(e):
            print("\nSuggestion: The repository or branch may already exist. Try using a different name or force pushing if appropriate.")
        elif "rejected" in str(e) and "non-fast-forward" in str(e):
            print("\nSuggestion: The remote repository has commits that you don't have locally. You might need to pull first or use --force if appropriate.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Repository URL is required")
        print("Usage: python git_push.py <repository_url> [branch_name]")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    branch_name = sys.argv[2] if len(sys.argv) > 2 else 'main'
    
    push_to_new_repo(repo_url, branch_name)