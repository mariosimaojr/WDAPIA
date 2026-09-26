# WDAPIA

Projeto Django com uma aplicação de cadastro e listagem de produtos.

## Requisitos

- Python 3.12
- Windows (ambiente virtual em `venv/`)

## Configuração do ambiente

O ambiente virtual já está criado em `venv/`. Para instalar/atualizar as dependências:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Comandos comuns

Execute os comandos sempre pelo interpretador da venv, para não depender de ativação do ambiente.

PowerShell:

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py test
```

Bash:

```bash
./venv/Scripts/python.exe manage.py migrate
./venv/Scripts/python.exe manage.py runserver
```

Após rodar `migrate`, o servidor de desenvolvimento fica disponível em http://127.0.0.1:8000.

## Estrutura do projeto

- `core/` — pacote do projeto Django (`settings.py`, URLconf raiz em `core/urls.py`, `wsgi.py`/`asgi.py`).
- `apps/` — pacote que agrupa todos os apps Django do projeto. Novos apps devem ser sempre criados aqui dentro, com `python manage.py startapp <nome> apps/<nome>` e registrados em `INSTALLED_APPS` como `apps.<nome>`.
  - `produtos/` — app responsável pelo cadastro e listagem de produtos na home (`/`).
    - `models.py` — modelo `Produto` (nome, quantidade em estoque, data de criação).
    - `views.py` / `forms.py` — formulário de cadastro e listagem na página inicial.
    - `templates/produtos/` — templates da aplicação.
- `admin/` — painel administrativo padrão do Django, disponível em `/admin/`.

## Rotas

| Rota      | Descrição                              |
|-----------|-----------------------------------------|
| `/`       | Cadastro e listagem de produtos          |
| `/admin/` | Django Admin                             |

## Configurações relevantes

- `DEBUG = True` e `SECRET_KEY` inseguro — apenas para desenvolvimento.
- Banco de dados: SQLite (`db.sqlite3`).
- E-mail configurado via `MAILERS` (Django 6.1), usando o backend de console.

## Documentação

Documentação técnica detalhada em [`docs/`](./docs/index.md):

- [`docs/index.md`](./docs/index.md) — índice geral.
- [`docs/architecture.md`](./docs/architecture.md) — arquitetura, apps, rotas e configurações.
- [`docs/database.md`](./docs/database.md) — modelos, campos e migrations.
- [`docs/performance-audit.md`](./docs/performance-audit.md) — auditoria de performance e recomendações.
- [`docs/apps/produtos.md`](./docs/apps/produtos.md) — documentação do app `apps.produtos`.
