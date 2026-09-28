#!/usr/bin/env python3
import subprocess
import sys
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def get_git_status():
    stdout, _, code = run_cmd("git status --porcelain")
    if code != 0:
        print("Error getting git status")
        sys.exit(1)
    
    files = []
    if not stdout:
        return files
        
    for line in stdout.split('\n'):
        if not line.strip():
            continue
        status_code = line[:2]
        filepath = line[3:].strip()

        # Handle quoted paths if any
        if filepath.startswith('"') and filepath.endswith('"'):
            filepath = filepath[1:-1]

        files.append((status_code, filepath))
    return files

def generate_commit_message(filepath, status_code):
    # Determine type of change
    if 'D' in status_code:
        action = "remove"
        prefix = "refactor"
    elif '?' in status_code:
        action = "add"
        prefix = "feat"
    else:
        action = "update"
        prefix = "chore"

    # Normalize module scope
    parts = filepath.split('/')
    
    if filepath in ['.env.example', '.gitignore', 'README.md', 'docker-compose.yml']:
        scope = "root"
    elif parts[0] == 'docker':
        scope = "docker"
        prefix = "chore"
    elif parts[0] == 'frontend':
        scope = "frontend"
        prefix = "feat" if action == "add" else "chore"
    elif parts[0] == 'backend':
        if len(parts) > 1:
            scope = parts[1]
        else:
            scope = "backend"
        if action == "add" and ("models" in filepath or "views" in filepath or "serializers" in filepath):
            prefix = "feat"
    else:
        scope = parts[0]

    filename = os.path.basename(filepath)
    msg = f"{prefix}({scope}): {action} {filename}"
    return msg

def main():
    files = get_git_status()
    if not files:
        print("No changes to commit!")
        return

    print(f"Found {len(files)} files to commit individually...\n")

    for status_code, filepath in files:
        commit_msg = generate_commit_message(filepath, status_code)
        
        # Stage file
        print(f"Staging: {filepath}")
        _, err, code = run_cmd(f'git add "{filepath}"')
        if code != 0:
            print(f"Error staging {filepath}: {err}")
            continue

        # Commit file
        print(f"Committing: {commit_msg}")
        _, err, code = run_cmd(f'git commit -m "{commit_msg}"')
        if code != 0:
            print(f"Error committing {filepath}: {err}")
        else:
            print(f"✓ Committed {filepath}\n")

    print("All individual commits completed successfully!")

if __name__ == '__main__':
    main()
