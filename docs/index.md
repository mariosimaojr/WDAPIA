# Documentação do projeto WDAPIA

Índice da documentação técnica do projeto. Comece por aqui.

## Sobre o projeto

WDAPIA é um projeto Django com uma aplicação (`produtos`) para cadastro e listagem de produtos, além do Django Admin padrão.

## Documentos disponíveis

| Documento | Conteúdo |
|-----------|----------|
| [`architecture.md`](./architecture.md) | Visão geral da arquitetura: apps, camadas, fluxo de requisição, configurações, rotas. |
| [`database.md`](./database.md) | Modelos de dados, campos, validações, migrations e o esquema do banco SQLite. |
| [`performance-audit.md`](./performance-audit.md) | Auditoria de performance: consultas ao banco, pontos de atenção e recomendações. |

## Documentação por app

| Documento | Conteúdo |
|-----------|----------|
| [`apps/produtos.md`](./apps/produtos.md) | App `apps.produtos`: modelo, formulário, view, templates, admin e testes. |

## Outros documentos do repositório

- [`README.md`](../README.md) — instruções de setup, comandos comuns e estrutura do projeto.
- [`CLAUDE.md`](../CLAUDE.md) — guia para o Claude Code trabalhar neste repositório (ambiente, comandos, workflow de TDD, sincronização de docs).
- [`DESIGN.md`](../DESIGN.md) — design system visual (estilo "Nintendo.com 2001") aplicado à home de produtos.

## Como manter esta documentação atualizada

Toda alteração de código (models, views, forms, urls, settings, migrations, templates, tasks, etc.) deve ser seguida pela execução do agente `doc-sync-onboarding`, responsável por manter `CLAUDE.md` e os arquivos em `docs/` sincronizados com o estado real do código. Veja a seção "Sincronização de documentação" em [`CLAUDE.md`](../CLAUDE.md).
