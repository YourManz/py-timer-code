import os
import git
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify the directory you want to watch
path_to_watch = "C:/Users/koben/Desktop/Coding Practice"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        file_location = event.src_path
        print(f"{event.src_path} was created")

    def on_deleted(self, event):
        file_location = event.src_path
        print(f"{event.src_path} was deleted")

    def on_modified(self, event):
        file_location = event.src_path
        print(f"{event.src_path} has been modified")

    def on_moved(self, event):
        file_location = event.src_path
        print(f"moved {event.src_path} to {event.dest_path}")

# Create an observer
observer = Observer()

# Attach the handler to the observer
event_handler = MyHandler()
observer.schedule(event_handler, path=path_to_watch, recursive=True)

# Start the observer
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()



def track_commits_in_directory(directory_path):
    # Check if the directory is a Git repository
    try:
        repo = git.Repo(directory_path)
    except git.exc.InvalidGitRepositoryError:
        return  # Not a Git repository

    # Get the list of commits
    commits = list(repo.iter_commits())

    # Print commit information
    for commit in commits:
        print("Commit:", commit.hexsha)
        print("Author:", commit.author.name)
        print("Date:", commit.committed_datetime)
        print("Message:", commit.message)
        print("-" * 50)

# Recursively iterate through child directories
for root, dirs, files in os.walk(parent_dir):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        track_commits_in_directory(dir_path)