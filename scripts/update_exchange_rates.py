#!/usr/bin/env python
"""Fetch latest exchange rates (base USD) and store them in DB.
Uses https://api.exchangerate.host/latest?base=USD
Run: python scripts/update_exchange_rates.py
"""
import sqlite3
import os
import json
from datetime import datetime

try:
    import requests
except Exception:
    requests = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

API_URL = 'https://api.exchangerate.host/latest?base=USD'

SAMPLE_RATES = {
    'USD': 1.0,
    'NGN': 770.0,
    'GBP': 0.79,
    'EUR': 0.92,
    'CAD': 1.36,
    'PGK': 3.5
}

def main():
    if not os.path.exists(DB_PATH):
        print('Database not found at', DB_PATH)
        return
    rates = None
    if requests:
        try:
            resp = requests.get(API_URL, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                rates = data.get('rates')
        except Exception as e:
            print('Failed to fetch rates:', e)
    if not rates:
        print('Using sample fallback rates')
        rates = SAMPLE_RATES
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for code, rate in rates.items():
        try:
            cur.execute('INSERT OR REPLACE INTO exchange_rates (currency_code, rate, updated_at) VALUES (?, ?, ?)', (code.upper(), float(rate), datetime.utcnow().isoformat()))
        except Exception:
            pass
    conn.commit()
    conn.close()
    print('Exchange rates updated')

if __name__ == '__main__':
    main()
