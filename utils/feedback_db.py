# utils/feedback_db.py
import sqlite3
import datetime
import os

# Define database file path inside /data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def _ensure_table_exists():
    """
    Ensures the feedback table exists before any read/write operation.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            question TEXT,
            answer TEXT,
            feedback TEXT
        )
    """)
    conn.commit()
    conn.close()


def store_feedback_db(question: str, answer: str, feedback: str):
    """
    Store chatbot feedback in a local SQLite database.
    """
    _ensure_table_exists()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO feedback (timestamp, question, answer, feedback) VALUES (?, ?, ?, ?)",
        (datetime.datetime.now().isoformat(), question, answer, feedback)
    )
    conn.commit()
    conn.close()


def get_feedback_entries(limit: int = 25):
    """
    Retrieve recent feedback entries for analytics display.
    If the database or table is missing, it will auto-create and return [].
    """
    _ensure_table_exists()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, question, feedback FROM feedback ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows