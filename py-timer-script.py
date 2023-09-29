import os
import git
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify the directory you want to watch
path_to_watch = "C:/Users/koben/Desktop/Coding Practice"

file_location = ''
is_editing = False
editing_minutes=0

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        file_location = event.src_path
        is_editing = True #Toggles the is editing varable to true, activating a while loop that will add minutes to a variable
        print(f"{event.src_path} was created")

    def on_deleted(self, event):
        file_location = event.src_path
        is_editing = True #Toggles the is editing varable to true, activating a while loop that will add minutes to a variable
        print(f"{event.src_path} was deleted")

    def on_modified(self, event):
        file_location = event.src_path
        is_editing = True #Toggles the is editing varable to true, activating a while loop that will add minutes to a variable
        print(f"{event.src_path} has been modified")

    def on_moved(self, event):
        file_location = event.src_path
        is_editing = True #Toggles the is editing varable to true, activating a while loop that will add minutes to a variable
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

while is_editing == True:
    editing_minutes += 1
    time.sleep(60)

def track_commits_in_directory(file_location):
    try:
        repo = git.Repo(file_location + '/.git')
    except git.exc.InvalidGitRepositoryError:
        return False  # Not a Git repository

    commits = list(repo.iter_commits())
    return len(commits)

previous_commit_count = 0

while True:
    current_commit_count = track_commits_in_directory(file_location)

    if current_commit_count > previous_commit_count:
        # Commit detected, start your event here
        print("Commit detected!")

        is_editing = False

        # Update the previous commit count
        previous_commit_count = current_commit_count

    time.sleep(60)  # Sleep for 60 seconds before checking again