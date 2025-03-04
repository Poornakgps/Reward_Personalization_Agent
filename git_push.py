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
        
        print(f"Initializing a new git repository in {current_dir}...")
        repo = git.Repo.init(current_dir)
        
        print("Adding all files to the repository...")
        repo.git.add(all=True)
        
        print("Committing changes...")
        repo.git.commit('-m', 'Initial commit')
        
        print("Setting remote repository URL...")
        origin = repo.create_remote('origin', repo_url)
        
        print(f"Setting up branch {branch_name}...")
        repo.git.branch('-M', branch_name)
        
        print("Pushing to remote repository...")
        repo.git.push('-u', 'origin', branch_name)
        
        print(f"Files have been successfully pushed to {repo_url} on branch {branch_name}")
        
    except git.GitCommandError as e:
        print(f"Git error: {e}")
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