import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = "F:/linealert-sync-drive/agent_watch"

class GitAutoCommitHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.handle_event(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.handle_event(event.src_path)

    def handle_event(self, file_path):
        # Only act on .md or .log files
        if file_path.endswith((".md", ".log", ".txt", ".py")):
            os.chdir("F:/linealert-sync-drive")
            subprocess.run(["git", "add", file_path])
            subprocess.run(["git", "commit", "-m", f"Auto-commit: updated {os.path.basename(file_path)}"])
            subprocess.run(["git", "push"])

if __name__ == "__main__":
    event_handler = GitAutoCommitHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    observer.start()
    print(f"✅ Watching folder: {WATCH_DIR}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
