# Auditoria de performance

Estado do projeto na data desta auditoria: aplicação pequena, um único modelo (`Produto`), sem carga de produção real. Esta auditoria registra os pontos observados no código atual e recomendações para quando o volume de dados/tráfego crescer.

## Pontos observados

### 1. Listagem sem paginação (`apps/produtos/views.py::home`)

```python
produtos = Produto.objects.all()
```

Toda a tabela `produtos_produto` é carregada e renderizada em cada `GET /`. Não há `Paginator`, `LIMIT`/`OFFSET`, nem filtro. Com poucas dezenas de registros isso é irrelevante; a partir de centenas/milhares de produtos, o tempo de resposta e o uso de memória crescem linearmente com o tamanho da tabela.

**Recomendação:** introduzir `django.core.paginator.Paginator` (ou `ListView` com `paginate_by`) quando o volume esperado ultrapassar algumas centenas de registros.

### 2. Query extra a cada validação de nome (`apps/produtos/forms.py::ProdutoForm.clean_nome`)

```python
if Produto.objects.filter(nome__iexact=nome).exists():
```

Executa uma query adicional (`SELECT ... WHERE nome ILIKE ...` no SQLite via `iexact`) a cada submissão do formulário. Sem índice dedicado, o SQLite faz *table scan* nessa coluna. Aceitável no volume atual, mas escala linearmente com o número de produtos.

**Recomendação:** se a tabela crescer, considerar um índice (`db_index=True` em `nome`, ou `UniqueConstraint` com uma expressão case-insensitive) para tornar a verificação O(log n) em vez de O(n), e para mover a garantia de unicidade para o nível do banco (hoje ela só existe na camada de formulário — ver [`database.md`](./database.md)).

### 3. Ausência de índices explícitos

Nenhum campo do modelo `Produto` tem `db_index=True` ou `unique=True`. A única ordenação (`-criado_em`, `-id`) e o único filtro (`nome__iexact`) usados hoje não têm índice de suporte. Em SQLite com poucos registros isso não importa; vale revisitar ao adicionar filtros/ordenações novas ou ao crescer a base.

### 4. Sem cache

Não há uso de `django.core.cache` em nenhuma view. Como a página é dinâmica (formulário + dados sempre atuais), isso é esperado; não é um problema hoje, apenas registrado para referência caso a listagem se torne pesada.

### 5. Banco de dados: SQLite em desenvolvimento

`DATABASES` usa SQLite (`db.sqlite3`), adequado para desenvolvimento e volumes pequenos, mas com limitações de concorrência de escrita (lock de arquivo) sob múltiplos processos simultâneos. Não há configuração de produção (Postgres/MySQL) ainda.

**Recomendação:** ao planejar deploy real, migrar para um banco cliente-servidor (ex.: PostgreSQL) antes de qualquer carga concorrente significativa.

### 6. N+1 queries

Não se aplica no estado atual — `Produto` não possui relacionamentos (`ForeignKey`/`ManyToMany`), então não há risco de N+1 nas queries existentes. Reavaliar esta seção quando relacionamentos forem introduzidos (uso de `select_related`/`prefetch_related`).

## Resumo de prioridade

| Item | Impacto atual | Ação recomendada | Quando agir |
|------|----------------|-------------------|-------------|
| Paginação da listagem | Nenhum (poucos registros) | Adicionar `Paginator` | Ao ultrapassar ~algumas centenas de produtos |
| Índice/constraint em `nome` | Nenhum | `db_index` ou constraint de unicidade case-insensitive | Ao crescer a tabela ou exigir integridade no banco |
| Migrar de SQLite | Nenhum (dev) | Avaliar Postgres/MySQL | Antes de deploy com múltiplos usuários concorrentes |

Esta auditoria deve ser revisada sempre que o modelo de dados, as views ou o volume de uso do sistema mudarem significativamente — ver processo de sincronização de documentação em [`CLAUDE.md`](../CLAUDE.md).
