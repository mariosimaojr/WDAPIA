# Arquitetura

## Visão geral

WDAPIA é um projeto Django 6.1.1 monolítico clássico (sem DRF/API REST): o navegador faz requisições HTTP diretamente às views, que renderizam templates server-side com Django Template Language. Não há frontend separado, build de assets nem chamadas assíncronas (JS/Celery/etc.).

```
Browser
  │  HTTP request
  ▼
core/urls.py (ROOT_URLCONF)
  ├── /admin/  → django.contrib.admin
  └── /        → include("apps.produtos.urls")
                     │
                     ▼
              apps/produtos/views.py (home)
                 ├── GET  → renderiza form vazio + lista de produtos
                 └── POST → valida ProdutoForm, salva Produto, redirect (PRG)
                     │
                     ▼
              apps/produtos/templates/produtos/*.html
                 (base.html, home.html)
                     │
                     ▼
              apps/produtos/static/produtos/css/design.css
```

## Projeto vs. apps

- `core/` — pacote de configuração do projeto (não é um app Django). Contém:
  - `settings.py` — `DJANGO_SETTINGS_MODULE=core.settings`.
  - `urls.py` — URLconf raiz, inclui `admin/` e `apps.produtos.urls`.
  - `wsgi.py` / `asgi.py` — pontos de entrada para deploy.
- `apps/` — pacote (com `__init__.py`) que agrupa todos os apps Django de domínio do projeto. Cada app vive em `apps/<nome>/` e é registrado com o caminho pontuado `apps.<nome>`.
- `apps/produtos/` — único app de domínio do projeto até o momento. Responsável pelo cadastro e listagem de produtos na home (`/`).

**Convenção obrigatória para novos apps:** criar sempre dentro de `apps/`, nunca na raiz do repositório:

```
python manage.py startapp <nome> apps/<nome>
```

Depois, conectar o novo app:
- `core/settings.py` → adicionar `'apps.<nome>'` a `INSTALLED_APPS`.
- `apps/<nome>/apps.py` → definir `name = "apps.<nome>"` (o `label` do app — usado por migrations e admin — continua sendo `<nome>`, pois o Django o deriva automaticamente do último segmento de `name`).
- `core/urls.py` → `include('apps.<nome>.urls')`.

## App `apps.produtos`

Documentação detalhada do app em [`apps/produtos.md`](./apps/produtos.md).

| Arquivo | Responsabilidade |
|---------|-------------------|
| `models.py` | Modelo `Produto` (ver [`database.md`](./database.md)). |
| `forms.py` | `ProdutoForm` (ModelForm) — validação de campos e regra de nome duplicado (`clean_nome`). |
| `views.py` | View de função `home` — GET renderiza formulário + listagem; POST processa cadastro (padrão Post/Redirect/Get, com `django.contrib.messages` para feedback de sucesso). |
| `urls.py` | Mapeia `""` → `views.home`, nome de rota `home`. |
| `admin.py` | Registra `Produto` no Django Admin com `list_display` e `search_fields`. |
| `templates/produtos/` | `base.html` (layout) e `home.html` (formulário + listagem), usando o design system descrito em [`../DESIGN.md`](../DESIGN.md). |
| `static/produtos/css/design.css` | CSS do design system aplicado à home. |
| `migrations/` | `0001_initial.py` (criação do modelo `Produto`), `0002_alter_produto_options.py` (ordenação padrão). |
| `tests.py` | Testes de model, form e view (unittest via Django `TestCase`). |
| `apps.py` | `ProdutosConfig` — `name = "apps.produtos"`, `label` (implícito) = `produtos`. |

## Rotas

| Rota | View | Nome | Descrição |
|------|------|------|-----------|
| `/` | `apps.produtos.views.home` | `home` | Cadastro (POST) e listagem (GET) de produtos. |
| `/admin/` | `django.contrib.admin.site.urls` | — | Django Admin padrão. |

## Configurações relevantes (`core/settings.py`)

- `DEBUG = True` e `SECRET_KEY` inseguro fixo no código — apenas para desenvolvimento, nunca usar em produção sem alterar.
- `ALLOWED_HOSTS = []` — só funciona com `DEBUG = True`.
- `INSTALLED_APPS`: apps padrão do Django (`admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles`) + `apps.produtos`.
- `DATABASES`: SQLite em `db.sqlite3` na raiz do projeto (`BASE_DIR`).
- `TEMPLATES`: `APP_DIRS = True`, sem diretório de templates em nível de projeto — cada app mantém seus templates em `<app>/templates/<app>/`.
- `LANGUAGE_CODE = 'pt-br'`, `TIME_ZONE = 'UTC'`, `USE_TZ = True`.
- `STATIC_URL = 'static/'` — sem `STATICFILES_DIRS` de projeto; cada app serve seus estáticos de `<app>/static/<app>/`.
- E-mail configurado via `MAILERS` (setting introduzida no Django 6.1, substitui `EMAIL_BACKEND`), usando `django.core.mail.backends.console.EmailBackend` (imprime e-mails no console, não envia de verdade).

## Testes e cobertura

- Framework: `django.test.TestCase` (unittest runner do Django), sem pytest.
- Cobertura configurada via `.coveragerc` (fonte = todo o repositório, omitindo `venv/`, `migrations/`, `manage.py`, `core/asgi.py`, `core/wsgi.py`); relatório HTML gerado em `htmlcov/`.
- Workflow obrigatório de TDD para novas funcionalidades: ver skill [`django-tdd`](../.claude/skills/django-tdd) referenciada em [`CLAUDE.md`](../CLAUDE.md).

## Ambiente e execução

Ver [`README.md`](../README.md) e a seção "Environment"/"Common commands" de [`CLAUDE.md`](../CLAUDE.md) para os comandos de setup, migrate, runserver e testes (sempre via `venv/Scripts/python.exe`, sem depender de ativação do virtualenv).

## Dependências principais

Definidas em [`requirements.txt`](../requirements.txt): `Django==6.1.1`, `asgiref`, `sqlparse`, `tzdata` (runtime); `coverage` (cobertura de testes); `specify-cli` e dependências do Spec Kit (`typer`, `rich`, `readchar`, etc.) usadas pelos workflows em `.specify/`.
