import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify the directory you want to watch
path_to_watch = "/path/to/your/directory"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"{event.src_path} was created")

    def on_deleted(self, event):
        print(f"{event.src_path} was deleted")

    def on_modified(self, event):
        print(f"{event.src_path} has been modified")

    def on_moved(self, event):
        print(f"moved {event.src_path} to {event.dest_path}")

# Create an observer
observer = Observer()

# Attach the handler to the observer
event_handler = MyHandler()
observer.schedule(event_handler, path=path_to_watch, recursive=False)

# Start the observer
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()
