# lore-enhancer

API de lore para jogos de mesa (Secret Cultist e os outros temas do secret-game): trechos etiquetados por campanha, área, deus, momento e tipo, e frases montadas por moldes. **Sem modelo de linguagem** (D2): é busca por etiqueta e recombinação.

Idioma: respostas e textos em português do Brasil, informal. Comentários no código: inglês.

## Fluxo (obrigatório)

1. Nunca commitar na `main`: branch a partir da `main` atualizada (`feat/`, `fix/`, `docs/`, `chore/`) e PR.
2. Rodar `scripts/verify.sh` antes de enviar e colar a saída no PR.
3. Commits em Conventional Commits, em português.

## Peças

| Arquivo | O que faz |
|---|---|
| `index.py` | Entrada do Vercel: só reexporta o `app` de `app/main.py` (o Vercel acha o FastAPI sozinho, sem `vercel.json`) |
| `app/main.py` | FastAPI: `GET /health`, `GET /lore`, `GET /fragments`, `POST /ingest` e `POST /ingest/url` (só com login do Supabase) |
| `app/compose.py` | `compose`: escolhe um molde do momento e preenche as lacunas com trechos do deus (depois os gerais); `tidy` junta preposições e põe maiúscula |
| `app/parse.py` | Obras inteiras em trechos (D7): tira o invólucro do Gutenberg, corta em frases de 60 a 280 caracteres e etiqueta deus e momento por palavras-chave (`GOD_WORDS`, `MOMENT_WORDS`) |
| `app/store.py` | `MemoryStore` (testes, local) e `SupabaseStore` (REST do Supabase com a chave de serviço) |
| `corpus/build.py` | O corpus como dados; gera `corpus/fragments.json` e `corpus/templates.json` |
| `scripts/seed_sql.py` | Gera `sql/seed.sql` do corpus (colar uma vez no SQL Editor) |
| `corpus/sources.json` | As obras inteiras de domínio público para ingerir (URL do texto puro, fonte, área, língua) |
| `scripts/ingest_works.py` | Baixa e ingere as obras de `sources.json`; roda no workflow `ingestão de obras` (`--dry` não grava) |
| `scripts/ingest.py` | Manda o corpus ao Supabase; roda no workflow `ingestão` depois do merge |
| `sql/schema.sql` | Tabelas `fragment` e `template`, busca de texto em português, coluna `embedding` vazia |

## Regras do corpus

- Só domínio público ou texto original. Toda citação diz a obra e o ano, e a tradução é nossa (`source`, `source_date` com a data em que o domínio público foi conferido). Fora: Chaosium (o RPG), August Derleth, Clark Ashton Smith (protegido no Brasil até 2032) e qualquer tradução moderna protegida.
- Mudou `corpus/build.py`: rode `scripts/verify.sh`, que regenera os JSON e o `sql/seed.sql`; commite os gerados juntos.
- Todo deus tem presságio, lugar, objeto e sussurro, e todo momento compõe para todo deus sem lacuna (os testes conferem).

## Línguas

Cada trecho tem `lang` (D7). O `/lore` e o `/fragments` usam `pt` se não disser outra. Sem modelo não há tradução: obra em inglês entra como `en` e não aparece no jogo em português.

## Configuração (no Vercel e nos secrets do GitHub)

`SUPABASE_URL` (https://ydzqrfkcsrochzwegrig.supabase.co), `SUPABASE_SECRET_KEY` (a chave secreta `sb_secret_…`, só no servidor), `SUPABASE_PUBLISHABLE_KEY` (a `sb_publishable_…`, para conferir o login do `/ingest`); as antigas `SUPABASE_SERVICE_KEY`/`SUPABASE_ANON_KEY` também valem. Sem elas a API usa a memória, vazia. Nunca colar chave no chat ou no código.
