# database.py
import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('.venv/bot_database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def add_qa_pair(conn, cursor, question, answer):
    cursor.execute("INSERT INTO qa_pairs (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()

def get_all_qa_pairs(conn):
    return pd.read_sql_query("SELECT question, answer FROM qa_pairs", conn)

def get_answers_for_question(cursor, question):
    cursor.execute("SELECT answer FROM qa_pairs WHERE question = ?", (question,))
    return cursor.fetchall()