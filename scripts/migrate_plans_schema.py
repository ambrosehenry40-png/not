#!/usr/bin/env python
"""Migration script to add missing columns to investment_plans for existing DBs.
Run: python scripts/migrate_plans_schema.py
"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

def column_exists(cur, table, column):
    cur.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    return column in cols

def main():
    if not os.path.exists(DB_PATH):
        print('Database not found at', DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # columns to ensure
    additions = [
        ("investment_plans","plan_name","TEXT NOT NULL DEFAULT 'Plan'"),
        ("investment_plans","minimum_amount","REAL DEFAULT 0.0"),
        ("investment_plans","profit_amount","REAL DEFAULT 0.0"),
        ("investment_plans","total_return","REAL DEFAULT 0.0"),
        ("investment_plans","duration_days","INTEGER DEFAULT 1"),
        ("investment_plans","capital_back","INTEGER DEFAULT 1"),
        ("investment_plans","created_at","TEXT"),
        ("investment_plans","updated_at","TEXT"),
    ]
    for table, col, spec in additions:
        if not column_exists(cur, table, col):
            try:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {spec}")
                print(f"Added column {col} to {table}")
            except Exception as e:
                print('Failed to add', col, e)
    conn.commit()
    conn.close()
    print('Migration done')

if __name__ == '__main__':
    main()
