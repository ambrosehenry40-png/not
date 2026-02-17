PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  balance REAL DEFAULT 0.0,
  policy_accepted INTEGER DEFAULT 0,
  is_admin INTEGER DEFAULT 0,
  country TEXT,
  currency_code TEXT,
  currency_symbol TEXT,
  currency_name TEXT,
  created_at TEXT
);

CREATE TABLE IF NOT EXISTS investment_plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plan_name TEXT NOT NULL,
  minimum_amount REAL NOT NULL DEFAULT 0.0,
  profit_amount REAL NOT NULL DEFAULT 0.0,
  total_return REAL NOT NULL DEFAULT 0.0,
  duration_days INTEGER NOT NULL DEFAULT 1,
  capital_back INTEGER DEFAULT 1,
  status TEXT DEFAULT 'active',
  created_at TEXT,
  updated_at TEXT
);

CREATE TABLE IF NOT EXISTS investments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  plan_id INTEGER NOT NULL,
  status TEXT DEFAULT 'pending',
  proof_image TEXT,
  created_at TEXT,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(plan_id) REFERENCES investment_plans(id)
);

CREATE TABLE IF NOT EXISTS withdrawal_settings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  min_amount REAL DEFAULT 0.0,
  max_amount REAL DEFAULT 1000000.0
);

CREATE TABLE IF NOT EXISTS withdrawals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  status TEXT DEFAULT 'pending',
  requested_at TEXT,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Seed a default withdrawal setting if none exists
INSERT INTO withdrawal_settings (min_amount, max_amount) SELECT 10.0, 10000.0 WHERE NOT EXISTS (SELECT 1 FROM withdrawal_settings);

-- Example plan
INSERT INTO investment_plans (plan_name, minimum_amount, profit_amount, total_return, duration_days, capital_back, status, created_at, updated_at)
SELECT 'Starter Plan', 100.0, 10.0, 110.0, 30, 1, 'active', datetime('now'), datetime('now') WHERE NOT EXISTS (SELECT 1 FROM investment_plans);
