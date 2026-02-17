#!/usr/bin/env python
import argparse
import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime
import getpass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app.db')


def create_admin(username, email, password, country, currency_code, currency_symbol, currency_name):
    pw_hash = generate_password_hash(password)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        try:
            cur.execute('INSERT INTO users (username, email, password_hash, balance, policy_accepted, is_admin, country, currency_code, currency_symbol, currency_name, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (username, email, pw_hash, 0.0, 1, 1, country, currency_code, currency_symbol, currency_name, datetime.utcnow()))
            conn.commit()
            print('Admin user created.')
        except sqlite3.OperationalError as oe:
            # fallback for legacy DB without currency columns
            if 'no column' in str(oe):
                try:
                    cur.execute('INSERT INTO users (username, email, password_hash, balance, policy_accepted, is_admin, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (username, email, pw_hash, 0.0, 1, 1, datetime.utcnow()))
                    conn.commit()
                    print('Admin user created (legacy DB).')
                except Exception as e:
                    raise
            else:
                raise
    except Exception as e:
        print('Error creating admin:', e)
    finally:
        conn.close()


def parse_args():
    p = argparse.ArgumentParser(description='Create admin user with optional currency settings')
    p.add_argument('--username', help='Admin username')
    p.add_argument('--email', help='Admin email')
    p.add_argument('--password', help='Admin password (if omitted will prompt)')
    p.add_argument('--country', default='US', help='Country code (e.g. US)')
    p.add_argument('--currency-code', dest='currency_code', default='USD', help='Currency code (e.g. USD)')
    p.add_argument('--currency-symbol', dest='currency_symbol', default='$', help='Currency symbol')
    p.add_argument('--currency-name', dest='currency_name', default='US Dollar', help='Currency full name')
    return p.parse_args()


def main():
    args = parse_args()
    username = args.username or input('Admin username [admin]: ') or 'admin'
    email = args.email or input('Email [admin@example.com]: ') or 'admin@example.com'
    if args.password:
        password = args.password
    else:
        while True:
            password = getpass.getpass('Password: ')
            confirm = getpass.getpass('Confirm password: ')
            if password == confirm:
                break
            print('Passwords do not match, try again.')

    country = args.country
    currency_code = args.currency_code
    currency_symbol = args.currency_symbol
    currency_name = args.currency_name

    resp = input(f"Use default currency {currency_code} ({currency_symbol}) for {country}? [Y/n]: ").strip().lower()
    if resp in ('n', 'no'):
        country = input('Country code (e.g. US): ').strip() or country
        currency_code = input('Currency code (e.g. USD): ').strip() or currency_code
        currency_symbol = input('Currency symbol (e.g. $): ').strip() or currency_symbol
        currency_name = input('Currency name (e.g. US Dollar): ').strip() or currency_name

    create_admin(username, email, password, country, currency_code, currency_symbol, currency_name)


if __name__ == '__main__':
    main()
