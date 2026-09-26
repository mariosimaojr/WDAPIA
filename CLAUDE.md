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

## Documentação detalhada

Além deste arquivo, consulte [`docs/index.md`](docs/index.md) para a documentação técnica completa:

- [`docs/architecture.md`](docs/architecture.md) — arquitetura, apps, rotas, fluxo de requisição e configurações.
- [`docs/database.md`](docs/database.md) — modelos, campos, validações e migrations.
- [`docs/performance-audit.md`](docs/performance-audit.md) — auditoria de performance e recomendações.
- [`docs/apps/produtos.md`](docs/apps/produtos.md) — documentação do app `apps.produtos`.

## Architecture

- `core/` is the project package, not an app: `settings.py` (`DJANGO_SETTINGS_MODULE=core.settings`), root URLconf `core/urls.py`, and `wsgi.py`/`asgi.py` entry points.
- All Django apps live under `apps/<name>/` (not at the repo root), imported and registered with the dotted path `apps.<name>` (e.g. `apps.produtos`). Create a new app with:
  ```
  python manage.py startapp <name> apps/<name>
  ```
  Then wire it in:
  - `core/settings.py` → add `'apps.<name>'` to `INSTALLED_APPS`.
  - `apps/<name>/apps.py` → set `name = "apps.<name>"` (its `label`, used by migrations/admin, still defaults to `<name>`).
  - `core/urls.py` → `include('apps.<name>.urls')`.
- Settings are development defaults: `DEBUG = True`, hardcoded insecure `SECRET_KEY`, empty `ALLOWED_HOSTS`, SQLite database, `TEMPLATES` with `APP_DIRS = True` (templates live in `<app>/templates/`) and no project-level template or static dirs.
- Email is configured with Django 6.1's `MAILERS` setting (console backend), not the older `EMAIL_BACKEND` setting.


## TDD workflow (mandatory for every new feature)

Para cada nova funcionalidade, siga obrigatoriamente a skill

[`.claude/skills/django-tdd`](.claude/skills/django-tdd) — escreva os testes **antes** da

implementação (Red → Green → Refactor).

Cobertura mínima exigida por funcionalidade:

- **Models** — campos, validações, métodos, `__str__`, constraints.
- **Forms** — validação de campos, `clean_*`, mensagens de erro.
- **Views** — status codes, contexto, permissões, redirecionamentos.
- **Templates** — renderização, blocos, presença de elementos esperados.
- **Integração** — fluxo end-to-end cobrindo a jornada do usuário.

Só marque a funcionalidade como concluída depois que todos esses níveis de testes estiverem
verdes.

## ⚠️ OBRIGATÓRIO: Sincronização de documentação

**Ao finalizar QUALQUER alteração de código neste repositório, é OBRIGATÓRIO executar,
como última etapa, o agente `doc-sync-onboarding` para atualizar a documentação
(`CLAUDE.md` e arquivos em `docs/`) refletindo as mudanças feitas.**
Isso vale para toda e qualquer modificação: novos modelos/campos, migrations, views, rotas,
tasks assíncronas, signals, middlewares, integrações, variáveis de ambiente, scripts de
infraestrutura, etc. Nenhuma tarefa de código é considerada concluída antes de a
documentação ter sido sincronizada por esse agente.