# Feature Specification: Cadastro e Listagem de Produtos na Home

**Feature Branch**: `001-product-registration`

**Created**: 2026-09-26

**Status**: Draft

**Input**: User description: "O usuário na home pode cadastrar produtos, o usuario digita o nome e quantidade em estoque. Na mesma página os produtos são listados."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cadastrar um produto na home (Priority: P1)

Ao acessar a página inicial, o usuário encontra um formulário com os campos "Nome" e "Quantidade em estoque". Ele preenche os dois campos, confirma o cadastro e o produto passa a fazer parte do estoque registrado.

**Why this priority**: Sem o cadastro não existe nenhum produto para listar; é a capacidade central da funcionalidade e já entrega valor sozinha (registrar o estoque).

**Independent Test**: Acessar a home, preencher nome e quantidade válidos, confirmar e verificar que o sistema informa sucesso e que o produto foi guardado (por exemplo, recarregando a página).

**Acceptance Scenarios**:

1. **Given** o usuário está na home, **When** informa o nome "Caneta azul" e a quantidade 50 e confirma, **Then** o produto é cadastrado, o usuário vê uma mensagem de sucesso e continua na home com o formulário limpo para um novo cadastro.
2. **Given** o usuário está na home, **When** tenta confirmar com o nome vazio, **Then** o produto não é cadastrado e é exibida uma mensagem indicando que o nome é obrigatório.
3. **Given** o usuário está na home, **When** informa uma quantidade negativa, não numérica ou fracionária, **Then** o produto não é cadastrado e é exibida uma mensagem indicando que a quantidade deve ser um número inteiro maior ou igual a zero.
4. **Given** já existe um produto "Caneta azul", **When** o usuário tenta cadastrar "caneta azul" (mesmo nome, ignorando maiúsculas/minúsculas e espaços nas pontas), **Then** o cadastro é recusado com uma mensagem informando que o produto já existe.
5. **Given** o cadastro foi recusado por um erro de validação, **When** a mensagem de erro é exibida, **Then** os valores digitados pelo usuário permanecem nos campos para correção.

---

### User Story 2 - Ver a lista de produtos na home (Priority: P2)

Na mesma página inicial, abaixo (ou ao lado) do formulário, o usuário vê a lista de todos os produtos cadastrados, com o nome e a quantidade em estoque de cada um.

**Why this priority**: Permite consultar o estoque e confirmar visualmente os cadastros; depende de existirem produtos, por isso vem depois do cadastro.

**Independent Test**: Com alguns produtos já cadastrados, acessar a home e verificar que todos aparecem com nome e quantidade corretos.

**Acceptance Scenarios**:

1. **Given** existem produtos cadastrados, **When** o usuário acessa a home, **Then** vê todos os produtos com seu nome e quantidade em estoque, do mais recente para o mais antigo.
2. **Given** não existe nenhum produto cadastrado, **When** o usuário acessa a home, **Then** vê uma mensagem informando que ainda não há produtos cadastrados.
3. **Given** o usuário acabou de cadastrar um produto, **When** o cadastro é concluído, **Then** o novo produto aparece imediatamente no topo da lista, sem que o usuário precise sair da página ou navegar para outro lugar.

---

### Edge Cases

- Nome contendo apenas espaços em branco: tratado como vazio e recusado.
- Espaços no início/fim do nome: removidos antes de salvar e de comparar duplicidade.
- Nome muito longo (acima de 100 caracteres): recusado com mensagem indicando o limite.
- Quantidade zero: aceita (produto cadastrado sem estoque).
- Quantidade muito grande (acima de 1.000.000): recusada com mensagem indicando o limite.
- Nomes com acentos e caracteres especiais (ex.: "Açúcar 1kg"): aceitos e exibidos corretamente.
- Reenvio do formulário (ex.: atualizar a página logo após cadastrar): não deve criar um produto duplicado.
- Muitos produtos cadastrados: a lista continua exibindo todos e a página permanece utilizável.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A página inicial (home) MUST exibir um formulário de cadastro de produto com os campos "Nome" e "Quantidade em estoque".
- **FR-002**: Os campos nome e quantidade MUST ser obrigatórios.
- **FR-003**: O sistema MUST aceitar como quantidade apenas números inteiros entre 0 e 1.000.000 (inclusive).
- **FR-004**: O sistema MUST aceitar nomes com 1 a 100 caracteres, após remover espaços no início e no fim.
- **FR-005**: O sistema MUST recusar o cadastro de um produto cujo nome já exista, comparando sem diferenciar maiúsculas/minúsculas e ignorando espaços no início/fim.
- **FR-006**: Ao recusar um cadastro, o sistema MUST exibir, na própria home, uma mensagem clara junto ao campo com problema e manter os valores digitados.
- **FR-007**: Ao cadastrar com sucesso, o sistema MUST guardar o produto de forma permanente (ele continua existindo após recarregar a página ou reabrir o sistema), exibir uma mensagem de sucesso e limpar o formulário.
- **FR-008**: A home MUST listar todos os produtos cadastrados, mostrando nome e quantidade em estoque, ordenados do cadastro mais recente para o mais antigo.
- **FR-009**: Quando não houver produtos, a home MUST exibir uma mensagem de lista vazia.
- **FR-010**: O cadastro e a listagem MUST acontecer na mesma página; após um cadastro o usuário permanece na home com a lista já atualizada.
- **FR-011**: Atualizar a página após um cadastro bem-sucedido MUST NOT gerar um novo cadastro do mesmo produto.

### Key Entities

- **Produto**: Item mantido em estoque. Atributos: nome (texto, único sem diferenciar maiúsculas/minúsculas, 1–100 caracteres), quantidade em estoque (inteiro, 0 a 1.000.000) e data/hora de cadastro (usada para ordenar a lista).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um usuário consegue cadastrar um produto em menos de 30 segundos a partir do momento em que abre a home.
- **SC-002**: 95% dos usuários conseguem cadastrar seu primeiro produto na primeira tentativa, sem ajuda.
- **SC-003**: 100% dos produtos cadastrados com sucesso aparecem na lista imediatamente após o cadastro, com nome e quantidade exatamente como informados.
- **SC-004**: 100% das tentativas com dados inválidos (nome vazio, nome duplicado, quantidade inválida) são recusadas com uma mensagem que indica o que corrigir.
- **SC-005**: Com até 1.000 produtos cadastrados, a home carrega e exibe a lista completa em até 2 segundos.

## Assumptions

- Não há login nem perfis de usuário nesta funcionalidade: qualquer pessoa que acessa a home pode cadastrar e ver os produtos, e todos veem a mesma lista compartilhada.
- Apenas os campos nome e quantidade são coletados; preço, descrição, categoria, código e imagem estão fora do escopo.
- Edição, exclusão e ajuste de estoque de produtos já cadastrados estão fora do escopo desta funcionalidade.
- Busca, filtros e paginação da lista estão fora do escopo; todos os produtos são exibidos em uma única lista.
- Nomes duplicados são recusados para evitar que o mesmo item apareça duas vezes no estoque com quantidades divergentes.
- Os limites de 100 caracteres para o nome e 1.000.000 para a quantidade são padrões razoáveis adotados na ausência de requisitos específicos.
- A interface e as mensagens são exibidas em português do Brasil.
