import sqlite3
import datetime

DATABASE_FILE = "tasks.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('active', 'claimed', 'completed')),
        claimed_by INTEGER,
        claimed_by_username TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        completed_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def _get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_task(description: str) -> int:
    conn = _get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute(
        "INSERT INTO tasks (description, status, created_at, updated_at) VALUES (?, 'active', ?, ?)",
        (description, now, now)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def fetch_all_tasks():
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY CASE status WHEN 'active' THEN 1 WHEN 'claimed' THEN 2 WHEN 'completed' THEN 3 END, created_at ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def fetch_task_by_id(task_id: int):
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_task_claim(task_id: int, user_id: int, username: str) -> bool:
    conn = _get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = cursor.execute(
        "UPDATE tasks SET status = 'claimed', claimed_by = ?, claimed_by_username = ?, updated_at = ? WHERE id = ? AND status = 'active'",
        (user_id, username, now, task_id)
    )
    conn.commit()
    conn.close()
    return result.rowcount > 0

def update_task_completion(task_id: int, user_id: int) -> bool:
    conn = _get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = cursor.execute(
        "UPDATE tasks SET status = 'completed', updated_at = ?, completed_at = ? WHERE id = ? AND claimed_by = ?",
        (now, now, task_id, user_id)
    )
    conn.commit()
    conn.close()
    return result.rowcount > 0

def update_task_unclaim(task_id: int, user_id: int) -> bool:
    conn = _get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = cursor.execute(
        "UPDATE tasks SET status = 'active', claimed_by = NULL, claimed_by_username = NULL, updated_at = ? WHERE id = ? AND claimed_by = ?",
        (now, task_id, user_id)
    )
    conn.commit()
    conn.close()
    return result.rowcount > 0
