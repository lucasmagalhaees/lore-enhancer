# Decisões

## D1. Para que serve (2026-11-09)

Tirar a lore do código do secret-game para um serviço que qualquer campanha usa (Secret Cultist, Secret Hitler, Secret Stalin), com a ingestão por endpoint e as tabelas separadas por área de conhecimento. Vem da D135 e da D136 do secret-game (`docs/lore-api.md` de lá).

## D2. Sem modelo, por etiquetas (2026-11-09)

Rodar um modelo (Ollama) pede servidor ligado o tempo todo e não vale agora. A busca é por etiqueta e pela busca de texto do Postgres; a frase sai de moldes. A coluna `embedding` existe vazia, para ligar o vetor se a busca por etiqueta ficar pobre (de preferência com o embedding do próprio Supabase).

## D3. Supabase próprio (2026-11-09)

Projeto `lore-enhancer` no Supabase (us-east-1), separado do 8 lados. Tabelas no schema `public`, com RLS ligado e nenhuma política: só a chave de serviço, no servidor, lê e grava.

## D4. Corpus inicial (2026-11-09)

245 trechos e 26 moldes, escritos e traduzidos aqui. Para cada um dos 21 deuses do Secret Cultist: 3 presságios, 2 lugares, 2 objetos e 2 sussurros. Mais trechos gerais e 34 citações de domínio público, em tradução própria: Lovecraft (morto em 1937, domínio público no Brasil desde 2008), Robert W. Chambers (1895), Algernon Blackwood (1910), a Bíblia King James (1611, com os apócrifos), o Enuma Elish (L. W. King, 1902), A Descida de Ishtar (R. W. Rogers, 1912) e a Goécia (Mathers, 1904). Fora: Clark Ashton Smith (protegido no Brasil até 2032), a Chaosium e o Derleth. Algumas citações estão marcadas como "adaptado" porque juntam ou encurtam o texto.

## D5. Ingestão (2026-11-09)

Duas portas: `sql/seed.sql` (colar no SQL Editor, gerado do corpus) e o workflow `ingestão`, que manda o corpus ao Supabase a cada merge que muda `corpus/`. As duas ignoram o que já existe. O `POST /ingest` fica para quem quiser mandar texto avulso, com login do Supabase.
