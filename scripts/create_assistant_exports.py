#!/usr/bin/env python
"""Create assistant_exports table to store CSV export history.
Run: python scripts/create_assistant_exports.py
"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

def main():
    if not os.path.exists(DB_PATH):
        print('Database not found at', DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS assistant_exports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filters TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()
    print('assistant_exports table ensured')

if __name__ == '__main__':
    main()
