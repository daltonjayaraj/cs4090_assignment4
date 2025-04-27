import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from tasks import (
    add_task,
    delete_task,
    filter_tasks_by_completion,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    generate_unique_id,
    get_overdue_tasks,
    load_tasks,
    save_tasks,
    search_tasks,
    toggle_complete,
    update_task,
)

# CRUD + core logic

@pytest.fixture
def empty():
    return []


def test_add_and_id(empty):
    a = add_task(empty, "A")
    b = add_task(empty, "B")
    assert a["id"] == 1 and b["id"] == 2
    assert generate_unique_id(empty) == 3


def test_toggle_and_update(empty):
    t = add_task(empty, "Todo")
    assert not t["completed"]
    toggle_complete(t)
    assert t["completed"]
    update_task(t, title="Updated", priority="Low")
    assert t["title"] == "Updated" and t["priority"] == "Low"


def test_delete(empty):
    t1 = add_task(empty, "Keep")
    t2 = add_task(empty, "Delete")
    delete_task(empty, t2["id"])
    assert empty == [t1]


# Filters, search, overdue

def test_filters_and_search():
    tasks = []
    hi = add_task(tasks, "High prio", priority="High", category="Work")
    lo = add_task(tasks, "Low prio",  priority="Low",  category="Personal")
    lo["completed"] = True

    assert filter_tasks_by_priority(tasks, "High") == [hi]
    assert filter_tasks_by_category(tasks, "Personal") == [lo]
    assert filter_tasks_by_completion(tasks, completed=True) == [lo]
    assert search_tasks(tasks, "high") == [hi]           # case-insensitive
    assert search_tasks(tasks, "prio") == [hi, lo]


def test_overdue_and_ignore_unknown_key():
    tasks = []
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    past = add_task(tasks, "Past", due_date=yesterday)
    future = add_task(tasks, "Future", due_date="2999-01-01")
    assert get_overdue_tasks(tasks) == [past]

    update_task(past, imaginary="noop")   # unknown field ignored
    assert "imaginary" not in past

# load_tasks / save_tasks edge-cases

def test_load_tasks_file_not_found(tmp_path: Path):
    """If file is absent, load_tasks should return an empty list."""
    assert load_tasks(tmp_path / "does_not_exist.json") == []


def test_load_tasks_corrupt_json(tmp_path: Path):
    """If JSON is invalid, function returns [] and leaves a .bak backup."""
    bad = tmp_path / "corrupt.json"
    bad.write_text("{ definitely : not : json }")
    tasks = load_tasks(bad)
    assert tasks == []                                    # empty list returned
    assert (tmp_path / "corrupt.json.bak").exists()       # backup created


def test_load_and_save_roundtrip(tmp_path: Path):
    tasks = []
    add_task(tasks, "Round-trip")
    f = tmp_path / "tasks.json"
    save_tasks(tasks, f)
    assert load_tasks(f) == tasks


def test_filter_by_priority_hits_last_line():
    tasks = []
    a = add_task(tasks, "High",  priority="High")
    b = add_task(tasks, "Medium", priority="Medium")
    # this call exercises the remaining uncovered line 
    assert filter_tasks_by_priority(tasks, "High") == [a]


# Final “empty-input”
def test_filter_helpers_on_empty():
    """Call each tiny helper once with an empty list to hit line 52."""
    assert filter_tasks_by_priority([], "High") == []
    assert filter_tasks_by_category([], "Work") == []
    assert filter_tasks_by_completion([], True) == []
    assert get_overdue_tasks([]) == []

def test_filter_priority_with_match():
    """Ensure the list-comprehension in filter_tasks_by_priority is executed."""
    tasks = [
        {
            "id": 1,
            "title": "X",
            "description": "",
            "priority": "High",
            "category": "Misc",
            "due_date": "2100-01-01",
            "completed": False,
            "created_at": "",
        }
    ]
    assert filter_tasks_by_priority(tasks, "High") == tasks
