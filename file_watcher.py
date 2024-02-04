# file_watcher.py
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppChangeHandler(FileSystemEventHandler):
    def __init__(self, main_script_path):
        self.main_script_path = main_script_path
        self.proc = None

    def start_app(self):
        if self.proc is None or self.proc.poll() is not None:
            print("Starting the Tkinter app...")
            self.proc = subprocess.Popen(["python", self.main_script_path])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Changes detected in {event.src_path}")
            self.restart_app()

    def restart_app(self):
        if self.proc:
            print("Restarting the Tkinter app...")
            self.proc.terminate()  # Terminate gracefully
            self.proc.wait()  # Wait for the process to finish
        self.start_app()

def watch_app_changes(main_script_path):
    path = "."  # Monitor the current directory and its subdirectories recursively
    event_handler = AppChangeHandler(main_script_path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    event_handler.start_app()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main_script_path = "main.py"  # Provide the path to your main Tkinter script
    watch_app_changes(main_script_path)
