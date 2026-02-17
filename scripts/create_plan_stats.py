#!/usr/bin/env python
"""Create plan_stats table to track views and investors.
Run: python scripts/create_plan_stats.py
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
    CREATE TABLE IF NOT EXISTS plan_stats (
      plan_id INTEGER PRIMARY KEY,
      total_views INTEGER DEFAULT 0,
      total_investors INTEGER DEFAULT 0,
      FOREIGN KEY(plan_id) REFERENCES investment_plans(id)
    )
    ''')
    conn.commit()
    conn.close()
    print('plan_stats table ensured')

if __name__ == '__main__':
    main()
