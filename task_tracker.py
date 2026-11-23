import json
from pathlib import Path

DATA = Path(__file__).with_name("tasks.json")

def load():
    if not DATA.exists(): return []
    try: return json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("Could not read tasks file; starting fresh."); return []

def save(tasks): DATA.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

def main():
    tasks = load()
    print("Task Tracker — type help for commands")
    while True:
        try: line = input("> ").strip()
        except (EOFError, KeyboardInterrupt): print("\\nBye!"); break
        if not line: continue
        cmd, _, arg = line.partition(" "); cmd = cmd.lower(); arg = arg.strip()
        if cmd in ("quit", "exit"): break
        elif cmd == "help": print("add <task> | list | done <id> | delete <id> | help | quit")
        elif cmd == "add" and arg:
            tasks.append({"id": max([t["id"] for t in tasks], default=0)+1, "title": arg, "done": False}); save(tasks); print("Added.")
        elif cmd == "list":
            if not tasks: print("No tasks yet.")
            for t in tasks: print(f'[{"x" if t["done"] else " "}] {t["id"]}: {t["title"]}')
        elif cmd in ("done", "delete"):
            try: ident = int(arg)
            except ValueError: print(f"Usage: {cmd} <id>"); continue
            task = next((t for t in tasks if t["id"] == ident), None)
            if not task: print("Task not found."); continue
            if cmd == "done": task["done"] = True
            else: tasks.remove(task)
            save(tasks); print("Updated.")
        else: print("Unknown command or missing task. Type help.")

if __name__ == "__main__": main()
