#!/usr/bin/env python
"""Create exchange_rates table.
Run: python scripts/create_exchange_rates.py
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
    CREATE TABLE IF NOT EXISTS exchange_rates (
        currency_code TEXT PRIMARY KEY,
        rate REAL,
        updated_at TEXT
    )
    ''')
    conn.commit()
    conn.close()
    print('exchange_rates table ensured')

if __name__ == '__main__':
    main()
