import os
from summarizers import LANGUAGE_HANDLERS

def summarize_repo(path):
    IGNORED_DIRS = {".git", ".venv", "__pycache__"}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in IGNORED_DIRS]
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}• {os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}• {f}")
            file_summary = summarize_file(os.path.join(root, f), subindent)
            if file_summary:
                print(file_summary)

def summarize_file(path, indent):
    ext = None
    for extension in LANGUAGE_HANDLERS:
        if path.endswith(extension):
            ext = extension
            break
    if ext:
        handler = LANGUAGE_HANDLERS[ext]
        try:
            return handler(path, indent)
        except Exception as e:
            return f"{indent}{path}: Error while summarizing ({e})"
    else:
        return None  

if __name__=="__main__":
    repo_path = input("Enter the path of the repo: ")
    if os.path.exists(repo_path):
        summarize_repo(repo_path)
    else:
        print("Path not found! Please enter a valid repo path.")
