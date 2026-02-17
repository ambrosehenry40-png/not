import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_rate(currency_code):
    """Return rate as float: 1 USD = rate * currency_code. If not found, returns 1.0 for USD or None."""
    if not currency_code:
        return None
    if currency_code.upper() == 'USD':
        return 1.0
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('SELECT rate FROM exchange_rates WHERE currency_code = ?', (currency_code.upper(),))
        r = cur.fetchone()
        if r:
            return float(r['rate'])
    except Exception:
        pass
    finally:
        conn.close()
    return None


def convert_usd_to(currency_code, amount_usd):
    """Convert a USD amount to target currency using stored rate. Returns rounded float."""
    try:
        rate = get_rate(currency_code)
        if rate is None:
            return None
        return round(float(amount_usd) * float(rate), 2)
    except Exception:
        return None


def convert_to_usd(currency_code, amount_local):
    """Convert a local currency amount to USD using stored rate. Returns float USD or None."""
    try:
        rate = get_rate(currency_code)
        if rate is None or rate == 0:
            return None
        return round(float(amount_local) / float(rate), 6)
    except Exception:
        return None
