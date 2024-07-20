import requests
import json
import os

# GitHub user
username = 'Harxhit'  # replace with your GitHub username

# GitHub API URLs
repos_url = f'https://api.github.com/users/{username}/repos'
user_url = f'https://api.github.com/users/{username}'

try:
    # Fetch repository data
    response = requests.get(repos_url)
    response.raise_for_status()  # Check if request was successful
    repos = response.json()

    # Fetch user data
    user_response = requests.get(user_url)
    user_response.raise_for_status()
    user_data = user_response.json()
    
    total_commits = 0
    latest_commit = ''
    repo_sizes = []

    # Process repository data
    for repo in repos:
        commits_url = repo['commits_url'].replace('{/sha}', '')
        commits_response = requests.get(commits_url)
        commits_response.raise_for_status()
        commits = commits_response.json()
        
        # Check if commits are available
        if isinstance(commits, list):
            total_commits += len(commits)
            if commits:
                latest_commit = commits[0].get('commit', {}).get('committer', {}).get('date', '')

        repo_sizes.append(repo.get('size', 0))

    # Calculate repo size
    average_size = sum(repo_sizes) / len(repo_sizes) if repo_sizes else 0

    # Generate README section
    readme_content = f"""
# Project Info

![Repositories](https://img.shields.io/badge/Repositories-{len(repos)}-blue?style=for-the-badge&logo=github)
![Total Commits](https://img.shields.io/badge/Total%20Commits-{total_commits}-green?style=for-the-badge&logo=github)
![Latest Commit](https://img.shields.io/badge/Last%20Commit-{latest_commit[:10]}-orange?style=for-the-badge&logo=github)
![Repo Size](https://img.shields.io/badge/Repo%20Size-{average_size:.2f}KB-yellow?style=for-the-badge&logo=github)

## Animated Project Info

<img src="https://media.giphy.com/media/26FPxguF3TWe3FZyY/giphy.gif" alt="Project Animation" width="500" />

This section dynamically displays the current project statistics.

## How to Update

1. **Run the update script:**
    ```sh
    python update_readme.py
    ```
2. **Commit and push the updated README file.**
"""

    # Save to README.md
    with open('README.md', 'w') as f:
        f.write(readme_content)

    print("README.md updated successfully!")

except requests.RequestException as e:
    print(f"HTTP Request failed: {e}")
except KeyError as e:
    print(f"KeyError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
