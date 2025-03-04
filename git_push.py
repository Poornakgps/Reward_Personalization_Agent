#!/usr/bin/env python3

import os
import sys
import git
import re

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
            try:
                repo.git.commit('-m', 'Initial commit')
            except git.GitCommandError as e:
                if "Please tell me who you are" in str(e):
                    print("Git requires user configuration. Setting up default user...")
                    repo.git.config('user.email', 'user@example.com')
                    repo.git.config('user.name', 'Git User')
                    repo.git.commit('-m', 'Initial commit')
                else:
                    raise
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
        
        # Check if the URL is HTTPS GitHub URL
        if "github.com" in repo_url and not repo_url.startswith("git@"):
            print("\nNOTE: Using HTTPS with GitHub requires a personal access token instead of password.")
            print("GitHub removed password authentication support on August 13, 2021.")
            print("Options for authentication:")
            print("1. Use a Personal Access Token (PAT) as your password")
            print("   - Create one at: https://github.com/settings/tokens")
            print("   - Use this token instead of your password when prompted")
            print("\n2. Use SSH instead of HTTPS:")
            username = re.search(r'github\.com/([^/]+)', repo_url)
            repo_name = re.search(r'github\.com/[^/]+/([^/\.]+)', repo_url)
            if username and repo_name:
                ssh_url = f"git@github.com:{username.group(1)}/{repo_name.group(1)}.git"
                print(f"   - Change remote URL to: {ssh_url}")
                print(f"   - Command: git remote set-url origin {ssh_url}")
            
            proceed = input("\nDo you want to proceed with the push anyway? (y/n): ")
            if proceed.lower() != 'y':
                print("Push aborted. Please set up authentication and try again.")
                return
        
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
        if "Authentication failed" in str(e) or "403 Forbidden" in str(e):
            print("\nAuthentication Error: GitHub no longer supports password authentication for HTTPS URLs.")
            print("\nSolutions:")
            print("1. Use a Personal Access Token (PAT):")
            print("   - Create one at: https://github.com/settings/tokens")
            print("   - Use the token as your password when prompted")
            print("   - Store it using: git config --global credential.helper store")
            print("\n2. Switch to SSH authentication:")
            username = re.search(r'github\.com/([^/]+)', repo_url)
            repo_name = re.search(r'github\.com/[^/]+/([^/\.]+)', repo_url)
            if username and repo_name:
                ssh_url = f"git@github.com:{username.group(1)}/{repo_name.group(1)}.git"
                print(f"   - Generate SSH key: ssh-keygen -t ed25519 -C \"your_email@example.com\"")
                print(f"   - Add to GitHub: https://github.com/settings/keys")
                print(f"   - Change remote URL: git remote set-url origin {ssh_url}")
            print("\n3. Use GitHub CLI:")
            print("   - Install GitHub CLI: https://cli.github.com/")
            print("   - Authenticate: gh auth login")
            print("   - Push using: gh repo create")
        elif "Permission denied" in str(e):
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