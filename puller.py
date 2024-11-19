import os
import yaml
from git import Repo, GitCommandError

def clone_or_update_repo(repo_dict):
    repo_name = os.path.basename(repo_dict['url'].rstrip('/')).split('.git')[0]
    path = os.path.join('./', repo_name)

    if not os.path.exists(path):
        # Клонируем репозиторий, включая все ветки
        Repo.clone_from(repo_dict['url'], path)
        print(f"Cloned {repo_dict['url']} to {path}")
    else:
        try:
            repo = Repo(path)
            # Проверяем наличие в локальном репозитории удалённого репозитория с таким же именем
            if any(r.name == 'origin' and r.url == repo_dict['url'] for r in repo.remotes):
                # Обновляем репозиторий
                repo.git.fetch('--all')
                print(f"Updated {repo_dict['url']} in {path}")
            else:
                print(f"Remote origin mismatch for {repo_dict['url']}, skipping update")
        except GitCommandError as e:
            print(f"Error updating repository at {path}: {e}")

def main():
    with open('repos.yaml', 'r') as file:
        repos = yaml.safe_load(file)

    for repo in repos['repositories']:
        clone_or_update_repo(repo)

if __name__ == "__main__":
    main()
