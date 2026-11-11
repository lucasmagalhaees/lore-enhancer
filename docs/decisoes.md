# Decisões

## D1. Para que serve (2026-11-09)

Tirar a lore do código do secret-game para um serviço que qualquer campanha usa (Secret Cultist, Secret Hitler, Secret Stalin), com a ingestão por endpoint e as tabelas separadas por área de conhecimento. Vem da D135 e da D136 do secret-game (`docs/lore-api.md` de lá).

## D2. Sem modelo, por etiquetas (2026-11-09)

Rodar um modelo (Ollama) pede servidor ligado o tempo todo e não vale agora. A busca é por etiqueta e pela busca de texto do Postgres; a frase sai de moldes. A coluna `embedding` existe vazia, para ligar o vetor se a busca por etiqueta ficar pobre (de preferência com o embedding do próprio Supabase).

## D3. Supabase próprio (2026-11-09)

Projeto `lore-enhancer` no Supabase (us-east-1), separado do 8 lados. Tabelas no schema `public`, com RLS ligado e nenhuma política: só a chave de serviço, no servidor, lê e grava.

## D4. Corpus inicial (2026-11-09)

245 trechos e 26 moldes (depois, D6), escritos e traduzidos aqui. Para cada um dos 21 deuses do Secret Cultist: 3 presságios, 2 lugares, 2 objetos e 2 sussurros. Mais trechos gerais e 34 citações de domínio público, em tradução própria: Lovecraft (morto em 1937, domínio público no Brasil desde 2008), Robert W. Chambers (1895), Algernon Blackwood (1910), a Bíblia King James (1611, com os apócrifos), o Enuma Elish (L. W. King, 1902), A Descida de Ishtar (R. W. Rogers, 1912) e a Goécia (Mathers, 1904). Fora: Clark Ashton Smith (protegido no Brasil até 2032), a Chaosium e o Derleth. Algumas citações estão marcadas como "adaptado" porque juntam ou encurtam o texto.

## D5. Ingestão (2026-11-09)

Duas portas: `sql/seed.sql` (colar no SQL Editor, gerado do corpus) e o workflow `ingestão`, que manda o corpus ao Supabase a cada merge que muda `corpus/`. As duas ignoram o que já existe. O `POST /ingest` fica para quem quiser mandar texto avulso, com login do Supabase.

## D6. Corpus maior (2026-11-09)

Pedido: "enriqueça o máximo possível esse banco com fontes de domínio público". Agora são 434 trechos e 39 moldes. Cada deus ganhou mais 2 presságios, 1 lugar, 1 objeto e 1 sussurro. Há mais trechos gerais e relíquias, e 63 citações novas, sempre em tradução nossa: mais Lovecraft, Chambers, Ambrose Bierce (1886), Poe, Stoker, Mary Shelley, M. R. James, Shakespeare, Dante (Longfellow, 1867), Milton, o Livro de Enoque (R. H. Charles, 1912), mais King James e mais Goécia. Augusto dos Anjos (Eu, 1912) entra no original. Muitas citações têm momento (traição na rejeição e na investigação, morte na eliminação, Babilônia caída no fim), e o `compose` passa a preferir o que foi feito para o momento, depois o que é do deus, depois o geral. Só entrou o que eu sei citar com segurança; o resto fica para quando a ingestão buscar o texto na fonte.

## D7. Obras inteiras (2026-11-09)

Pedido: ingerir obras completas e o Python fazer o parse. Em vez de PDF, entra o texto puro do Project Gutenberg, que é mais limpo e não passa pelo limite de upload do Vercel. O `app/parse.py` corta a obra em frases e etiqueta deus e momento por palavras-chave. Entram todos os trechos etiquetados e só uma amostra dos outros (`untagged_max`), para a obra não afogar o resto. O tipo é `trecho`, e os moldes com `{trecho}` só usam um que combine com o deus ou o momento; se nenhum combinar, vale outro molde. Coluna nova `lang`: sem modelo não há tradução, então as obras em inglês (Lovecraft) entram como `en` e ficam fora do jogo em português. No jogo entram a Bíblia de Almeida (Gutenberg nº 62383) e os Contos Phantasticos de Teófilo Braga (nº 32646). Dois caminhos: o `POST /ingest/url` para uma obra avulsa e o workflow `ingestão de obras`, que roda o `corpus/sources.json`. Não foi testado contra os textos reais, porque o Gutenberg não abre daqui; o primeiro run do workflow mostra quantos trechos e de quais deuses saíram de cada obra.

## D8. Migrações numeradas e um mapa do Supabase (2026-11-11)

O mesmo projeto do Supabase serve a lore e o login do Secret Cultist. O `sql/schema.sql` virou `sql/migrations/001_lore.sql`, a parte do jogo entrou como `002_game_auth.sql`, e `docs/supabase.md` diz qual app usa qual tabela e qual chave. Tabela nova entra como migração nova.
