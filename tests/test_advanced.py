
import pytest
from tasks import add_task, filter_tasks_by_priority, filter_tasks_by_category

@pytest.fixture
def tasks():
    arr = []
    add_task(arr, 'Task high', priority='High', category='Work')
    add_task(arr, 'Task medium', priority='Medium', category='Personal')
    add_task(arr, 'Task low', priority='Low', category='School')
    return arr

@pytest.mark.parametrize('priority,expected', [
    ('High', 1),
    ('Medium', 1),
    ('Low', 1),
])
def test_filter_by_priority(tasks, priority, expected):
    assert len(filter_tasks_by_priority(tasks, priority)) == expected

def test_filter_by_category_mock(monkeypatch, tasks):
    monkeypatch.setattr('tasks.datetime', __import__('datetime').datetime)
    result = filter_tasks_by_category(tasks, 'Work')
    assert len(result) == 1 and result[0]['category'] == 'Work'
