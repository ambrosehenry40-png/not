# Manual Investment & Withdrawal Platform

Run a dev server:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Notes:
- SQLite DB is created automatically from `schema.sql` on first run.
- Change `app.config['SECRET_KEY']` in `app.py` before production.
