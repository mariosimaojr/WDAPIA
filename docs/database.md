# Banco de dados

## Motor

SQLite, arquivo `db.sqlite3` na raiz do projeto (`core/settings.py` → `DATABASES['default']`). Sem serviços externos de banco.

## Modelos

### `produtos.Produto`

Definido em [`apps/produtos/models.py`](../apps/produtos/models.py).

| Campo | Tipo | Regras | Observações |
|-------|------|--------|-------------|
| `id` | `AutoField` | chave primária | gerado automaticamente pelo Django |
| `nome` | `CharField(max_length=100)` | obrigatório | rótulo "Nome" no `ProdutoForm`; unicidade case-insensitive garantida na camada de formulário (`clean_nome`), não no banco |
| `quantidade_estoque` | `PositiveIntegerField` | obrigatório, `>= 0` e `<= 1_000_000` (via `MaxValueValidator(1_000_000)`) | `verbose_name="quantidade em estoque"`; rótulo "Quantidade em estoque" no formulário |
| `criado_em` | `DateTimeField(auto_now_add=True)` | preenchido automaticamente na criação | não editável |

**Meta:**
- `ordering = ["-criado_em", "-id"]` — mais recentes primeiro; `-id` como critério de desempate para registros criados no mesmo instante (evita ordenação flaky em testes).

**Métodos:**
- `__str__` retorna `nome`.

**Validações que vivem fora do model:**
- Nome duplicado (case-insensitive) é rejeitado em `ProdutoForm.clean_nome`, não em uma `UniqueConstraint` do banco — logo, é possível ter nomes duplicados se o registro for criado fora do form (ex.: via shell ou Admin sem validação adicional).

## Migrations (`apps/produtos/migrations/`)

| Migration | Efeito |
|-----------|--------|
| `0001_initial.py` | Cria a tabela `produtos_produto` com os campos `nome`, `quantidade_estoque`, `criado_em`. |
| `0002_alter_produto_options.py` | Aplica `Meta.ordering = ["-criado_em", "-id"]` ao modelo. |

Para aplicar migrations: `python manage.py migrate` (ver [`README.md`](../README.md)). Após alterar `models.py`, gerar nova migration com `python manage.py makemigrations produtos`.

## Diagrama (único modelo atualmente)

```
Produto
├── id: AutoField (PK)
├── nome: CharField(100)
├── quantidade_estoque: PositiveIntegerField (max 1_000_000)
└── criado_em: DateTimeField (auto_now_add)
```

Não há relacionamentos (`ForeignKey`, `ManyToMany`, `OneToOne`) no projeto até o momento — `Produto` é o único modelo de domínio.

## Acesso administrativo

`apps/produtos/admin.py` registra `Produto` no Django Admin (`/admin/`) com `list_display = ("nome", "quantidade_estoque", "criado_em")` e `search_fields = ("nome",)`.
