import os
import git
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify the directory you want to watch
path_to_watch = "C:/Users/koben/Desktop/Coding Practice"

# Define a set of patterns to ignore (e.g., ignore .git and .vscode folders)
ignore_patterns = ["*/.git/* """, "*/.vscode/*"""]

file_location = ''
is_editing = False
editing_minutes = 0

class MyHandler(FileSystemEventHandler):
    def should_ignore(self, event):
        for pattern in ignore_patterns:
            if pattern in event.src_path:
                return True
        return False

    def on_created(self, event):
        global file_location, is_editing
        if not self.should_ignore(event):
            file_location = event.src_path
            is_editing = True
            print(f"{event.src_path} was created")

    # Add other event handlers here...

# Create an observer
observer = Observer()

# Attach the handler to the observer
event_handler = MyHandler()
observer.schedule(event_handler, path=path_to_watch, recursive=True)

# Start the observer in a separate thread
observer_thread = threading.Thread(target=observer.start)
observer_thread.daemon = True
observer_thread.start()

def editing_timer():
    global is_editing, editing_minutes
    while True:
        if is_editing:
            editing_minutes += 1
        time.sleep(60)

# Start the editing timer in a separate thread
editing_thread = threading.Thread(target=editing_timer)
editing_thread.daemon = True
editing_thread.start()

def track_commits_in_directory(directory_path):
    try:
        # Check if it's a directory with a .git folder or a file within a Git repository
        if os.path.isdir(directory_path):
            repo = git.Repo(directory_path)
        else:
            # If it's a file, get the directory containing the file
            repo = git.Repo(os.path.dirname(directory_path))
    except git.exc.InvalidGitRepositoryError:
        return False  # Not a Git repository

    commits = list(repo.iter_commits())
    return len(commits)

previous_commit_count = 0

def git_commit_tracker(previous_commit_count):
    global is_editing
    while True:
        current_commit_count = track_commits_in_directory(file_location)
        if current_commit_count > previous_commit_count:
            # Commit detected, start your event here
            print("Commit detected!")
            is_editing = False
            print(editing_minutes)
            previous_commit_count = current_commit_count
        time.sleep(60)

# Start the Git commit tracking in a separate thread
git_commit_thread = threading.Thread(target=git_commit_tracker, args=(previous_commit_count,))
git_commit_thread.daemon = True
git_commit_thread.start()

# Main thread can continue executing other tasks or waiting for user input

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()

#checking for watchdog interference