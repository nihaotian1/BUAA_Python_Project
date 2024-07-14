# db_handler.py
import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('todo.db')

def close_db(conn):
    conn.close()

def register_user(username, password):
    with connect_db() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def update_user(user_id, username=None, password=None):
    with connect_db() as conn:
        c = conn.cursor()
        if username:
            c.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
        if password:
            c.execute("UPDATE users SET password = ? WHERE id = ?", (password, user_id))
        conn.commit()

def add_task(user_id, name, due_date, duration=1, task_type='default', weight=1.0, is_daily=False):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (uid, name, due_date, duration, type, weight, is_daily) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (user_id, name, due_date, duration, task_type, weight, int(is_daily)))
        conn.commit()

def delete_task(task_id):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

def update_task(task_id, **kwargs):
    updates = []
    params = []

    for key, value in kwargs.items():
        if key in ['name', 'due_date', 'duration', 'type', 'weight', 'is_daily']:
            updates.append(f"{key} = ?")
            params.append(value)

    if updates:
        query = "UPDATE tasks SET {} WHERE id = ?".format(", ".join(updates))
        params.append(task_id)

        with connect_db() as conn:
            c = conn.cursor()
            c.execute(query, params)
            conn.commit()

def get_expired_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE due_date <= ?", (today,))
        return c.fetchall()

def get_all_tasks():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        return c.fetchall()