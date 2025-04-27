# app.py  — drop-in replacement
import streamlit as st
import subprocess, sys
from datetime import datetime, date
from io import StringIO
from tasks import (
    load_tasks, save_tasks, generate_unique_id,
    filter_tasks_by_priority, filter_tasks_by_category,
    filter_tasks_by_completion, search_tasks, get_overdue_tasks
)

# Helper: run pytest in a subprocess and pipe results to Streamlit
def run_pytest(py_args):
    """
    Launch pytest as 'python -m pytest <args>'.

    • Captures combined stdout+stderr so Streamlit can display it.
    • Returns the exit code to decide pass/fail colouring.
    """
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", *py_args],
        text=True,
        capture_output=True,
    )
    st.code(completed.stdout + completed.stderr)
    if completed.returncode == 0:
        st.success("All tests passed ")
    else:
        st.error(f"Tests failed (exit={completed.returncode}) ")

# Streamlit UI

st.set_page_config(page_title="CS4090 To-Do", page_icon="📝", layout="centered")
st.title("📋 CS4090 – Streamlit To-Do App")

tasks = load_tasks()

st.sidebar.header("Add New Task")
with st.sidebar.form("new_task"):
    t_title = st.text_input("Task Title")
    t_desc  = st.text_area("Description")
    t_pri   = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
    t_cat   = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
    t_due   = st.date_input("Due Date", value=date.today())
    if st.form_submit_button("Add Task") and t_title.strip():
        tasks.append({
            "id": generate_unique_id(tasks),
            "title": t_title,
            "description": t_desc,
            "priority": t_pri,
            "category": t_cat,
            "due_date": t_due.strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        save_tasks(tasks)
        st.sidebar.success("Task added!")


st.header("📂 Filters & Search")
cat_options = ["All"] + sorted({t["category"] for t in tasks})
col1, col2, col3 = st.columns(3)
with col1:
    f_cat = st.selectbox("Category", cat_options)
with col2:
    f_pri = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
with col3:
    f_show_done = st.checkbox("Show Completed", value=False)
f_query = st.text_input("🔍 Search")

# Apply filters
filtered = tasks
if f_cat != "All":
    filtered = filter_tasks_by_category(filtered, f_cat)
if f_pri != "All":
    filtered = filter_tasks_by_priority(filtered, f_pri)
if not f_show_done:
    filtered = filter_tasks_by_completion(filtered, completed=False)
if f_query:
    filtered = search_tasks(filtered, f_query)


overdue = get_overdue_tasks(filtered)
if overdue:
    st.warning(f" {len(overdue)} task(s) overdue!")

# Task list
st.subheader(" Your Tasks")
for task in filtered:
    st.markdown("---")
    left, right = st.columns([6, 1])
    # Left: text
    with left:
        title_md = f"~~**{task['title']}**~~" if task["completed"] else f"**{task['title']}**"
        st.markdown(title_md)
        st.caption(
            f"Due: {task['due_date']} • Priority: {task['priority']} • Category: {task['category']}"
        )
        st.write(task["description"])
    # Right: buttons
    with right:
        if st.button("Check" if not task["completed"] else "BACK", key=f"done_{task['id']}"):
            task["completed"] = not task["completed"]
            save_tasks(tasks)
            st.rerun()  # <── new Streamlit API
        if st.button("DELETE", key=f"del_{task['id']}"):
            tasks[:] = [t for t in tasks if t["id"] != task["id"]]
            save_tasks(tasks)
            st.rerun()

# Sidebar: 

st.sidebar.header(" Run Tests")

if st.sidebar.button("Unit + Coverage"):
    run_pytest(["-q", "tests/test_basic.py", "--cov=tasks", "--cov=app", "--cov-report=term-missing"])

if st.sidebar.button("Param/Mock/HTML"):
    run_pytest(["-q", "tests/test_advanced.py", "--html=unit_report.html"])

if st.sidebar.button("TDD suite"):
    run_pytest(["-q", "tests/test_tdd.py"])

if st.sidebar.button("BDD features"):
    run_pytest(["-q", "tests/features"])

if st.sidebar.button("Hypothesis"):
    run_pytest(["-q", "tests/test_property.py"])
