# boss-battles
A Micro:bit based coding challenge game


## Development
### Clone the repo
- https: https://github.com/MrGallo/boss-battles.git
- ssh: git@github.com:MrGallo/boss-battles.git
- [GitHub CLI](https://cli.github.com/): gh repo clone MrGallo/boss-battles

### Install poetry package manager
- Install poetry: `$ curl -sSL https://install.python-poetry.org | python3 -`
    - Once done, you should be able to check the version with `$ poetry --version`.
    - If not, follow these steps:
        - Add poetry to pah: `$ echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc`
        - Refresh termitnal: `source ~/.bashrc`
        - `$ poetry --version` should work now. 

## Daily Operating Procedure

This guide provides a simple daily process for contributing to a Python project using Git and Poetry via the terminal. It's designed for people new to Git and Poetry.

### 1. Start Your Day: Sync with Remote

Before starting any work, make sure your local copy of the project is up-to-date.

```bash
# Navigate to your project directory
cd /path/to/your/project

# Ensure you're on the correct branch (usually 'main' or 'develop')
git checkout main

# Fetch the latest changes from the remote repository
git fetch origin

# Merge any changes that have been made to the remote branch into your local copy
git pull origin main
```

### 2. Install dependancies
```bash
# Install the dependencies listed in the pyproject.toml file
poetry install
```

### 3. Create a new branch to develop on
```bash
# Create and switch to a new branch
git checkout -b your-branch-name
```

### 4. If you already have an active branch...
```bash
# Switch to the main branch
git checkout main

# Fetch and pull any new changes
git fetch origin
git pull origin main

# Rebase your feature branch with the latest changes
git checkout your-branch-name
git rebase main

# If there are conflicts, resolve them, then continue the rebase
# After resolving conflicts:
git add .
git rebase --continue
```

### 5. Actually starting to code
```bash
# activate the poetry shell (virtual environment) to get working
poetry shell

# do some work, then run tests with
pytest
```

### 6. Stage your changes
```bash
# Stage all changes
git add .

# OR stage specific files
git add file1 file2
```

### 7. Commit your changes
```bash
# Commit with a message
git commit -m "Description of what you changed"
```

### 8. Push your changes
```bash
# Push the branch to the remote repository
git push origin your-branch-name
```
