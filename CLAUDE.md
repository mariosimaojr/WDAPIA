# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This is a freshly generated Django 6.1.1 project (`django-admin startproject core .`) with no custom apps yet. Only Django's built-in contrib apps are installed, and the only route is `admin/`. There is no git repo, no `requirements.txt`, and no test/lint tooling configured.

## Environment

- Windows, Python 3.12 virtualenv in `venv/` (Django, asgiref, sqlparse, tzdata only).
- Run commands through the venv interpreter so you don't depend on activation:
  - PowerShell: `.\venv\Scripts\python.exe manage.py <command>`
  - Bash: `./venv/Scripts/python.exe manage.py <command>`
- `db.sqlite3` currently exists but is empty (migrations have not been applied).

## Common commands

```
python manage.py migrate                 # apply migrations (needed before first runserver/admin use)
python manage.py runserver               # dev server at http://127.0.0.1:8000
python manage.py startapp <name>         # new app; then add it to INSTALLED_APPS in core/settings.py
python manage.py makemigrations [app]
python manage.py createsuperuser
python manage.py check
python manage.py test                    # all tests (Django's unittest runner)
python manage.py test app.tests.MyTestCase.test_method   # a single test
```

## Architecture

- `core/` is the project package, not an app: `settings.py` (`DJANGO_SETTINGS_MODULE=core.settings`), root URLconf `core/urls.py`, and `wsgi.py`/`asgi.py` entry points. New functionality goes in separate apps at the repo root, wired in via `INSTALLED_APPS` and `include()` in `core/urls.py`.
- Settings are development defaults: `DEBUG = True`, hardcoded insecure `SECRET_KEY`, empty `ALLOWED_HOSTS`, SQLite database, `TEMPLATES` with `APP_DIRS = True` (templates live in `<app>/templates/`) and no project-level template or static dirs.
- Email is configured with Django 6.1's `MAILERS` setting (console backend), not the older `EMAIL_BACKEND` setting.
