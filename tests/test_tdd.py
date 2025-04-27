
from datetime import datetime, timedelta
from tasks import add_task, get_overdue_tasks

def test_get_overdue_tasks():
    tasks = []
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    add_task(tasks, 'Past due', due_date=yesterday)
    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1 and overdue[0]['title'] == 'Past due'
