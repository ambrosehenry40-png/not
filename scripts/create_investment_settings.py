#!/usr/bin/env python
"""Create investment_settings table to store platform-wide investment min/max.
Run: python scripts/create_investment_settings.py
"""
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

def main():
    if not os.path.exists(DB_PATH):
        print('Database not found at', DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS investment_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        min_amount REAL DEFAULT 10.0,
        max_amount REAL DEFAULT 100000.0,
        updated_at TEXT
    )
    ''')
    # seed default if empty
    cur.execute('SELECT COUNT(*) FROM investment_settings')
    cnt = cur.fetchone()[0]
    if cnt == 0:
        cur.execute('INSERT INTO investment_settings (min_amount, max_amount, updated_at) VALUES (?, ?, ?)', (10.0, 100000.0, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    print('investment_settings ensured')

if __name__ == '__main__':
    main()
