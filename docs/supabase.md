# Supabase: o que é de quem

Um projeto só (`ydzqrfkcsrochzwegrig`), porque o plano grátis não tinha espaço para outro. Dois apps usam.

| Peça | Dono | Quem lê | Quem escreve | Chave |
|---|---|---|---|---|
| `fragment`, `template` | lore-enhancer | a API (`/lore`, `/fragments`) | a API (`/ingest`) e o workflow `ingestão` | secreta (`sb_secret_…`), só no servidor |
| `game_secrets` | secret-cultist (D138) | o app, só com login de `driver` (RLS) | à mão, no SQL Editor | publicável (`sb_publishable_…`) + token do login |
| Auth (usuários e `app_metadata.role`) | secret-cultist | o app, no login | à mão, em Authentication → Users | publicável |

## Migrações

Em `sql/migrations/`, numeradas e idempotentes: dá para rodar todas de novo, na ordem, no SQL Editor.

1. `001_lore.sql`: as tabelas da lore, a busca em português e a coluna `embedding` vazia.
2. `002_game_auth.sql`: a tabela `game_secrets` e a regra de que só o `driver` lê. Cópia de `secret-cultist/sql/auth.sql`; mudou lá, muda aqui no mesmo dia.

Depois das migrações, `sql/seed.sql` carrega o corpus (gerado por `scripts/seed_sql.py`).

## Regras

- Chave secreta nunca no app nem no chat; a publicável é pública por definição.
- Tabela nova entra como migração nova (`003_…`), nunca editando uma antiga já rodada.
