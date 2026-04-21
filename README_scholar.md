# Scholar — Week 1 scaffold

This is a minimal Flask scaffold for the Scholar personal study app (Week 1).

Quick start (Windows PowerShell):

1. create a venv and activate it

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. install requirements

```powershell
pip install -r requirements.txt
```

3. initialize the database

```powershell
$env:FLASK_APP = 'app.py'
flask --app app.py init-db
```

4. run the app

```powershell
flask --app app.py --debug run
```

Notes:
- Database defaults to `sqlite:///scholar.db`. Copy `.env.example` to `.env` to override settings.
- Week 1 implemented: Flask project setup, SQLite schema, Subject CRUD and base templates.
- Next: Assignments, Pomodoro timer, grade tracking, Anthropic quiz integration.
