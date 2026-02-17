#!/usr/bin/env python
"""Migration to add currency columns to investments table.
Run: python scripts/migrate_investments_currency.py
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
    # check existing columns
    cur.execute("PRAGMA table_info(investments)")
    cols = [r[1] for r in cur.fetchall()]
    changes = False
    if 'amount_usd' not in cols:
        try:
            cur.execute('ALTER TABLE investments ADD COLUMN amount_usd REAL')
            changes = True
        except Exception as e:
            print('Failed to add amount_usd:', e)
    if 'amount_local' not in cols:
        try:
            cur.execute('ALTER TABLE investments ADD COLUMN amount_local REAL')
            changes = True
        except Exception as e:
            print('Failed to add amount_local:', e)
    if 'currency_code' not in cols:
        try:
            cur.execute('ALTER TABLE investments ADD COLUMN currency_code TEXT')
            changes = True
        except Exception as e:
            print('Failed to add currency_code:', e)
    if changes:
        conn.commit()
        print('investments table altered with currency columns')
    else:
        print('No changes needed')
    conn.close()

if __name__ == '__main__':
    main()
