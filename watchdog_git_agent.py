import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
from git import Repo

WATCH_FOLDER = "F:/linealert-sync-drive/agent_watch"
REPO_PATH = "F:/linealert-sync-drive"
GITHUB_REMOTE = "origin"

openai = OpenAI()

class WatchHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith((".log", ".md", ".proto")):
            return
        filename = os.path.basename(event.src_path)
        with open(event.src_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"🔍 File changed: {filename}")

        prompt = f"""This is a new file update from LineAlert USB cracking logs or notes:\n\n{content}\n\nPlease create a response script or summarized insights in code or markdown."""
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're an expert code/document assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        output = response.choices[0].message.content
        out_path = os.path.join(WATCH_FOLDER, f"gpt_output_{filename}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Output saved: {out_path}")

        repo = Repo(REPO_PATH)
        repo.git.add("--all")
        repo.index.commit(f"Auto-update: {filename}")
        print("✅ Git commit complete")

        try:
            repo.git.push(GITHUB_REMOTE, "main")
            print("🚀 Changes pushed to GitHub")
        except Exception as e:
            print(f"⚠️ Git push failed: {e}")

if __name__ == "__main__":
    print(f"👀 Watching folder: {WATCH_FOLDER}")
    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
