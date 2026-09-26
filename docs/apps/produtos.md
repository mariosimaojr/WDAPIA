# App `produtos`

Localização: [`apps/produtos/`](../../apps/produtos/). Registrado em `INSTALLED_APPS` como `apps.produtos` (ver [`../architecture.md`](../architecture.md)).

## Responsabilidade

Único app de domínio do projeto até o momento. Implementa o cadastro e a listagem de produtos na home (`/`): um formulário de criação e uma tabela com os produtos já cadastrados, do mais recente para o mais antigo.

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| [`models.py`](../../apps/produtos/models.py) | Modelo `Produto`. |
| [`forms.py`](../../apps/produtos/forms.py) | `ProdutoForm` (`ModelForm`). |
| [`views.py`](../../apps/produtos/views.py) | View de função `home`. |
| [`urls.py`](../../apps/produtos/urls.py) | Rota `""` → `home`, nome `home`. |
| [`admin.py`](../../apps/produtos/admin.py) | Registro de `Produto` no Django Admin. |
| [`apps.py`](../../apps/produtos/apps.py) | `ProdutosConfig` (`name = "apps.produtos"`). |
| [`migrations/`](../../apps/produtos/migrations/) | `0001_initial.py`, `0002_alter_produto_options.py`. |
| [`templates/produtos/`](../../apps/produtos/templates/produtos/) | `base.html` (layout) e `home.html` (formulário + listagem). |
| [`static/produtos/css/design.css`](../../apps/produtos/static/produtos/css/design.css) | CSS do design system aplicado à home. |
| [`tests.py`](../../apps/produtos/tests.py) | Testes de model, form, view e template. |

## Modelo `Produto`

Ver detalhes completos de campos e validações em [`../database.md`](../database.md#produtosproduto).

- `nome` (`CharField`, obrigatório, único na prática via validação de formulário).
- `quantidade_estoque` (`PositiveIntegerField`, 0 a 1.000.000).
- `criado_em` (`DateTimeField`, preenchido automaticamente).
- Ordenação padrão: mais recente primeiro (`-criado_em`, `-id`).

## Formulário `ProdutoForm`

`ModelForm` sobre `Produto` com os campos `nome` e `quantidade_estoque`.

- Rótulos customizados: "Nome" e "Quantidade em estoque".
- Todos os widgets recebem `class="text-input"` (usada pelo CSS do design system).
- `clean_nome`: rejeita cadastro se já existir um produto com o mesmo nome, ignorando maiúsculas/minúsculas (`nome__iexact`). Não faz `.strip()` explícito, mas o `CharField` do Django já normaliza espaços nas extremidades antes da validação.

## View `home`

Função única que atende `GET` e `POST` na mesma rota (`/`), seguindo o padrão Post/Redirect/Get:

- **GET**: instancia `ProdutoForm()` vazio e lista todos os `Produto` (`Produto.objects.all()`, sem paginação — ver [`../performance-audit.md`](../performance-audit.md)). Renderiza `produtos/home.html` com `form` e `produtos` no contexto.
- **POST**: valida `ProdutoForm(request.POST)`.
  - Se válido: salva o produto, adiciona mensagem de sucesso via `django.contrib.messages` ("Produto cadastrado com sucesso.") e redireciona para `home` (evita reenvio do formulário ao atualizar a página).
  - Se inválido: re-renderiza a mesma página com o formulário preenchido e os erros de validação (status 200).

## Templates

- `base.html` — layout base: cabeçalho (`nav-bar`), faixa de subnavegação, blocos `hero` e `content`, rodapé (`footer-bar`). Carrega `produtos/css/design.css` via `{% load static %}`.
- `home.html` — estende `base.html`:
  - Bloco `hero`: título "Produtos" em `hero-panel`.
  - Bloco `content`: mensagens do Django (`messages`), painel de formulário (`form-panel`) renderizando cada campo com label/erros, e painel de listagem (`list-panel`) com uma tabela (`produtos-table`, linhas `news-row`) ou a mensagem "Ainda não há produtos cadastrados." quando vazio.

O visual segue o design system documentado em [`../../DESIGN.md`](../../DESIGN.md) (estilo "Nintendo.com 2001").

## Admin

`ProdutoAdmin` registra `Produto` com:
- `list_display = ("nome", "quantidade_estoque", "criado_em")`
- `search_fields = ("nome",)`

## Testes (`tests.py`)

16 testes, organizados em quatro classes:

| Classe | Cobertura |
|--------|-----------|
| `ProdutoModelTests` | `__str__` retorna o `nome`. |
| `HomeViewTests` | Mensagem de lista vazia; criação e redirecionamento em POST válido; rejeição de nome vazio, quantidade negativa, quantidade acima do limite (1.000.001) e nome duplicado (case-insensitive); ordenação da listagem (mais recente primeiro). |
| `HomeTemplateDesignTests` | Presença dos elementos do design system: link para `design.css`, `nav-bar`, `hero-panel`, `form-panel`/`button-submit`, `news-row` na listagem, `footer-bar`. |
| `ProdutoFormWidgetTests` | Widgets de `nome` e `quantidade_estoque` recebem `class="text-input"`. |

Rodar apenas os testes deste app:

```
python manage.py test apps.produtos
```

## Pontos de atenção

- Não há paginação na listagem nem constraint de unicidade de `nome` no banco (a duplicidade é bloqueada só pelo formulário) — detalhado em [`../performance-audit.md`](../performance-audit.md) e [`../database.md`](../database.md).
