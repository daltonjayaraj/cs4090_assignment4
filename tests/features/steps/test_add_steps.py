from pytest_bdd import given, when, then, scenarios, parsers
from tasks import add_task


scenarios('../add_task.feature')



@given("an empty task list", target_fixture="empty_list")
def empty_list():
    """Provide a fresh list that acts as our in-memory store."""
    return []

@when(parsers.parse('the user adds a task titled "{title}"'))
def add(title, empty_list):
    add_task(empty_list, title)

@then(parsers.parse('there should be {count:d} task in the list'))
def check_count(empty_list, count):
    assert len(empty_list) == count
