#!/usr/bin/env python
"""Create announcements table migration.
Run: python scripts/create_announcements_table.py
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
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        image_url TEXT,
        video_url TEXT,
        is_active INTEGER DEFAULT 0,
        start_date TEXT,
        end_date TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()
    print('announcements table ensured')

if __name__ == '__main__':
    main()
