
"""Core task‑management logic for the Streamlit to‑do app.

The API is intentionally framework‑agnostic so it can be exercised by
pytest, pytest‑bdd, Hypothesis, or the Streamlit UI.
"""
from __future__ import annotations
import json
import os
from datetime import datetime
from typing import List, Dict


DEFAULT_TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks(file_path: str = DEFAULT_TASKS_FILE) -> List[Dict]:
    """Load tasks from JSON on disk.  Returns empty list if file missing/corrupt."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Corrupted file – start fresh but keep a backup just in case
        backup = str(file_path) + ".bak"
        os.rename(file_path, backup)
        print(f"⚠️ {file_path} was corrupt; backed up to {backup}")
        return []



def save_tasks(tasks: List[Dict], file_path: str = DEFAULT_TASKS_FILE) -> None:
    """Write tasks to disk in a pretty‑printed JSON format."""
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=2, sort_keys=True)



def generate_unique_id(tasks: List[Dict]) -> int:
    """Return the next available integer ID (1‑based)."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def add_task(tasks: List[Dict], title: str, description: str = "", priority: str = "Medium",
             category: str = "Other", due_date: str | None = None) -> Dict:
    """Append a new task to the given list and return it."""
    if not title.strip():
        raise ValueError("Title cannot be empty")
    task = {
        "id": generate_unique_id(tasks),
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "due_date": due_date or datetime.now().strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    return task


def update_task(task: Dict, **updates) -> Dict:
    """In‑place update of a task dict; returns the reference for chaining."""
    for key, value in updates.items():
        if key in task:
            task[key] = value
    return task


def delete_task(tasks: List[Dict], task_id: int) -> None:
    """Remove a task from the list by ID."""
    tasks[:] = [t for t in tasks if t["id"] != task_id]


def toggle_complete(task: Dict) -> Dict:
    task["completed"] = not task["completed"]
    return task



def filter_tasks_by_priority(tasks: List[Dict], priority: str) -> List[Dict]:
    return [t for t in tasks if t["priority"] == priority]


def filter_tasks_by_category(tasks: List[Dict], category: str) -> List[Dict]:
    return [t for t in tasks if t["category"] == category]


def filter_tasks_by_completion(tasks: List[Dict], completed: bool = True) -> List[Dict]:
    return [t for t in tasks if t["completed"] == completed]


def search_tasks(tasks: List[Dict], query: str) -> List[Dict]:
    q = query.lower()
    return [t for t in tasks if q in t["title"].lower() or q in t["description"].lower()]


def get_overdue_tasks(tasks: List[Dict]) -> List[Dict]:
    today_str = datetime.now().strftime("%Y-%m-%d")
    return [t for t in tasks if not t["completed"] and t["due_date"] < today_str]
