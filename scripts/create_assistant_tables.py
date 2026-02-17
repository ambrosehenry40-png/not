#!/usr/bin/env python
"""Create assistant tables: nodes, options, config.
Run: python scripts/create_assistant_tables.py
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
    CREATE TABLE IF NOT EXISTS assistant_nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        is_root INTEGER DEFAULT 0,
        created_at TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS assistant_options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id INTEGER NOT NULL,
        option_text TEXT NOT NULL,
        next_node_id INTEGER,
        action_type TEXT,
        action_payload TEXT,
        display_order INTEGER DEFAULT 0,
        FOREIGN KEY(node_id) REFERENCES assistant_nodes(id)
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS assistant_config (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        enabled INTEGER DEFAULT 1,
        button_label TEXT DEFAULT 'Help',
        assistant_name TEXT DEFAULT 'InvestPro Assistant',
        avatar_url TEXT
    )
    ''')
    # ensure single config row
    cur.execute('INSERT OR IGNORE INTO assistant_config (id, enabled, button_label, assistant_name) VALUES (1,1,'Help','InvestPro Assistant')')
    conn.commit()
    conn.close()
    print('assistant tables ensured')

if __name__ == '__main__':
    main()
