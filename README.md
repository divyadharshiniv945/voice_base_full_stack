# Ulavi Auth System

A production-style authentication and authorization project built with Flask, SQLite, HTML5, CSS3, and vanilla JavaScript.

## Features

- User registration, login, logout
- Session-based authentication with `Flask-Login`
- Strong password hashing with `Flask-Bcrypt`
- Role-based authorization for `admin` and `user`
- CSRF protection with `Flask-WTF`
- SQLite database integration via `Flask-SQLAlchemy`
- Responsive dark UI with modern dashboard layout
- Profile image upload, last login tracking, account active status
- Admin user management table, search, pagination
- Error pages for 403 and 404

## Installation

1. Create a Python virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Create the database and run migrations:

```powershell
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

4. Run the application:

```powershell
& .venv\Scripts\python.exe run.py
```

5. Open the app in your browser at `http://localhost:5000`

## Environment Variables

Copy `.env` and update values for production:

- `SECRET_KEY`
- `DATABASE_URL`
- `FLASK_ENV`

## Example Accounts

- Admin: `admin@example.com` / `AdminPass123!`
- User: `user@example.com` / `UserPass123!`

## Deployment Notes

- Use a production WSGI server such as Gunicorn or Waitress.
- Set `SESSION_COOKIE_SECURE=True` in production.
- Use HTTPS and a strong `SECRET_KEY`.
- Store large static assets behind a CDN or reverse proxy.
- Keep `.env` out of version control.
