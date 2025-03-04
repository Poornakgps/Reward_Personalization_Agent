#!/usr/bin/env python3

import os
import sys
import git
import re

def push_to_new_repo(repo_url):
    """
    Initialize a new git repository and push all files to the 'master' branch.
    
    Args:
        repo_url (str): URL of the remote repository
    """
    try:
        # Get current directory
        current_dir = os.getcwd()
        
        # Check if the URL is SSH or HTTPS format
        is_ssh = repo_url.startswith("git@")
        
        # Convert HTTPS to SSH format if needed
        if not is_ssh and "github.com" in repo_url:
            username = re.search(r'github\.com/([^/]+)', repo_url)
            repo_name = re.search(r'github\.com/[^/]+/([^/\.]+)', repo_url)
            if username and repo_name:
                ssh_url = f"git@github.com:{username.group(1)}/{repo_name.group(1)}.git"
                print(f"Converting HTTPS URL to SSH format: {ssh_url}")
                repo_url = ssh_url
                is_ssh = True
        
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
            current_url = next(origin.urls)
            if current_url != repo_url:
                print(f"Remote 'origin' exists but with different URL. Updating from {current_url} to {repo_url}...")
                repo.git.remote('set-url', 'origin', repo_url)
            else:
                print(f"Remote 'origin' already exists with correct URL: {repo_url}")
        except ValueError:
            print("Setting remote repository URL...")
            origin = repo.create_remote('origin', repo_url)
        
        print("Switching to 'master' branch...")
        repo.git.checkout('master')
        
        print("Pulling latest changes from the remote repository...")
        try:
            repo.git.pull('origin', 'master')
        except git.GitCommandError as e:
            print("Failed to pull latest changes. Continuing anyway...")
        
        print("Pushing to remote repository using SSH authentication...")
        
        # Test SSH connection before pushing
        if is_ssh:
            print("Testing SSH connection...")
            github_domain = repo_url.split('@')[1].split(':')[0]
            try:
                import subprocess
                result = subprocess.run(['ssh', '-T', f'git@{github_domain}'], 
                                       capture_output=True, text=True)
                # GitHub returns non-zero status even on successful auth
                if "successfully authenticated" in result.stderr or "You've successfully authenticated" in result.stderr:
                    print("SSH authentication successful!")
                else:
                    print("SSH connection test result:")
                    print(result.stderr)
            except Exception as e:
                print(f"SSH test failed: {e}")
                print("Continuing anyway...")
        
        # Push to remote
        repo.git.push('-f', 'origin', 'master')
        
        print(f"Files have been successfully pushed to {repo_url} on branch 'master'")
        
    except git.GitCommandError as e:
        print(f"Git error: {e}")
        print("\nDetailed error information:")
        print(f"Command: {e.command}")
        print(f"Status: {e.status}")
        print(f"Stderr: {e.stderr}")
        
        # Provide helpful suggestions based on common errors
        if "Permission denied (publickey)" in str(e):
            print("\nSSH Authentication Error: Your SSH key was not accepted.")
            print("\nSolutions:")
            print("1. Verify your SSH key is added to the SSH agent:")
            print("   - Run: ssh-add -l")
            print("   - If empty, add your key: ssh-add ~/.ssh/id_ed25519 (or your key path)")
            print("\n2. Check your SSH key is added to your GitHub account:")
            print("   - View your public key: cat ~/.ssh/id_ed25519.pub")
            print("   - Add it to: https://github.com/settings/keys")
            print("\n3. Test your SSH connection:")
            print("   - Run: ssh -T git@github.com")
            print("\n4. Make sure the SSH key has the correct permissions:")
            print("   - Run: chmod 600 ~/.ssh/id_ed25519")
            print("   - Run: chmod 700 ~/.ssh")
        elif "rejected" in str(e) and "non-fast-forward" in str(e):
            print("\nSuggestion: The remote repository has commits that you don't have locally.")
            print("- Pull first: git pull --rebase origin master")
            print("- Or force push (caution!): git push -f origin master")
        elif "already exists" in str(e):
            print("\nSuggestion: The repository or branch may already exist. Try using a different name or force pushing if appropriate.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Repository URL is required")
        print("Usage: python git_push.py <repository_url>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    
    push_to_new_repo(repo_url)