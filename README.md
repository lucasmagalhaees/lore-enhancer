# lore-enhancer

API de lore para jogos de mesa: trechos de domínio público e originais, etiquetados por campanha, deus, momento e tipo, combinados em frases por moldes. Sem modelo de linguagem, sem custo por chamada.

```
GET /lore?campaign=secret-cultist&moment=eliminacao&god=moloque&seed=1&pres=Ana&target=Caio
→ {"text": "Caio cai numa fornalha de bronze em forma de touro. Ninguém sabe ainda se a mesa ficou mais segura.", ...}
```

Momentos: `abertura`, `lei-L`, `lei-F`, `rejeicao`, `caos`, `veto`, `investigacao`, `eliminacao`, `ato2`, `ato3`, `fim-L`, `fim-F`.

## Subir

1. Supabase, SQL Editor: rodar as migrações de `sql/migrations/` em ordem e depois `sql/seed.sql` (rodar de novo as migrações sempre que entrar uma nova: é idempotente).
2. Vercel: importar o repo e pôr `SUPABASE_URL`, `SUPABASE_SECRET_KEY` e `SUPABASE_PUBLISHABLE_KEY`.
3. GitHub, Settings → Secrets → Actions: `SUPABASE_URL` e `SUPABASE_SECRET_KEY`, para o workflow `ingestão` mandar o corpus novo a cada merge.

## Testes

```bash
pip install -r requirements.txt -r requirements-dev.txt
scripts/verify.sh
```
