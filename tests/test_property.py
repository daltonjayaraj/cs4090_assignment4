from hypothesis import given, strategies as st
from tasks import add_task, generate_unique_id

non_blank = st.text(min_size=1, max_size=20).filter(lambda s: s.strip() != "")

@given(non_blank)
def test_create_task_property(title):
    task_list = []
    t = add_task(task_list, title)
    assert t["title"] == title

@given(st.lists(non_blank, min_size=1, max_size=20))
def test_unique_id_monotonic(titles):
    task_list = []
    for idx, title in enumerate(titles, start=1):
        add_task(task_list, title)
        assert task_list[-1]["id"] == idx
        assert generate_unique_id(task_list) == idx + 1
