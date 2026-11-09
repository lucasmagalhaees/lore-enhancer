"""The corpus of lore, as data: writes corpus/*.json, which scripts/ingest.py and sql/seed.sql are made from.
Every quoted line is from a public-domain work, in our own translation; lines marked 'original' are written for this
project. Dates are when the public-domain status was checked."""
import json, pathlib
OUT = pathlib.Path(__file__).parent
C = 'secret-cultist'
CHECK = '2026-11-09'
ORIG = 'lore-enhancer (original)'
F = []
def add(area, kind, text, source=ORIG, god=None, moment=None, date=None):
    F.append({'campaign': C, 'area': area, 'kind': kind, 'text': text, 'source': source, 'god': god, 'moment': moment, 'source_date': date})

# ---- per god: omens (pressagio), places (lugar), objects (objeto), whispers (sussurro) -----------------------------
GODS = {
 'cthulhu': ('cthulhu', ['o cheiro de maresia entra por baixo da porta, longe de qualquer mar', 'um escultor da cidade acorda gritando o mesmo nome, noite após noite', 'a lua nasce verde e baixa sobre o porto'],
             ['uma ilha de pedra verde que subiu do mar com ângulos errados', 'o porão alagado da igreja velha'], ['um ídolo de pedra-sabão com cabeça de polvo', 'um diário de bordo encharcado'],
             ['Ph’nglui mglw’nafh Cthulhu R’lyeh wgah’nagl fhtagn', 'na casa dele em R’lyeh, o morto Cthulhu espera sonhando']),
 'nyarlathotep': ('cthulhu', ['um homem alto, de pele escura como ônix, sorri no fim da rua', 'os aparelhos elétricos da casa acendem sozinhos', 'um palestrante de feira mostra maravilhas que ninguém consegue esquecer'],
             ['uma tenda de espetáculos montada sem licença na praça', 'uma pirâmide negra numa fotografia que ninguém tirou'], ['um cartaz rasgado do Homem de Preto', 'um trapezoedro brilhante numa caixa de metal'],
             ['o Caos Rastejante tem mil máscaras', 'o Faraó Negro voltou do Egito']),
 'hastur': ('cthulhu', ['um farrapo de tecido amarelo preso na maçaneta', 'alguém deixou um programa de teatro na sua cadeira', 'as nuvens se rasgam em ondas, como se fossem mar'],
             ['as margens do lago de Hali', 'um teatro fechado desde a estreia de uma peça proibida'], ['o Signo Amarelo bordado num lenço', 'o segundo ato de uma peça que ninguém deveria ler'],
             ['você encontrou o Signo Amarelo?', 'Carcosa está perdida, e o Rei espera']),
 'shub': ('cthulhu', ['cascos do tamanho de rodas marcam o jardim', 'balidos na mata, de um rebanho que ninguém cria', 'as árvores se mexem sem vento'],
             ['uma clareira com pedras em círculo', 'uma fazenda onde os bichos nascem com olhos demais'], ['uma estatueta de uma cabra com mil filhotes', 'uma faca cerimonial de pedra'],
             ['Iä! Shub-Niggurath! A Cabra Negra dos Bosques com Mil Filhotes!', 'a mãe da floresta tem fome']),
 'yog': ('cthulhu', ['os relógios da casa marcam horas diferentes ao mesmo tempo', 'uma luz de muitas cores sai pela fresta da porta', 'pegadas enormes aparecem no meio da estrada e somem'],
             ['uma colina com pedras de pé no topo', 'a biblioteca de uma universidade, na seção trancada'], ['uma fórmula escrita em latim ao contrário', 'a chave de uma porta que não existe na planta'],
             ['Yog-Sothoth conhece o portal', 'Yog-Sothoth é a chave e o guardião do portal']),
 'dagon': ('cthulhu', ['pegadas molhadas, com membranas entre os dedos, sobem do porto', 'um cheiro de peixe podre nas roupas de quem voltou da pesca', 'olhos que não piscam espiam da água'],
             ['uma cidade de pescadores onde todos têm o mesmo rosto', 'um recife negro além do quebra-mar'], ['uma tiara de ouro de feitio estranho', 'uma rede cheia de algo que ninguém quer olhar'],
             ['o Pai Dagon e a Mãe Hidra chamam', 'quem nasceu do mar volta para o mar']),
 'azathoth': ('cthulhu', ['uma flauta fina toca de lugar nenhum, sem parar', 'as estrelas parecem mais perto do que deviam', 'um zumbido no ouvido que todos ouvem juntos'],
             ['o observatório no alto da colina', 'um quarto onde o teto parece infinito'], ['uma partitura impossível de tocar', 'um telescópio virado para o vazio entre as estrelas'],
             ['no centro de tudo, o sultão demônio dorme e sonha', 'se ele acordar, nada mais existe']),
 'tsathoggua': ('cthulhu', ['o chão está morno, como se algo dormisse logo embaixo', 'um sapo enorme de pedra apareceu na entrada da mina', 'um cheiro de terra úmida e preguiça'],
             ['N’kai, o abismo escuro sob a montanha', 'uma mina abandonada que desce mais do que devia'], ['uma oferenda de carne deixada na pedra', 'uma estatueta de um deus gordo, de olhos fechados'],
             ['ele não tem pressa', 'deixe a oferenda e não acorde quem dorme']),
 'ithaqua': ('cthulhu', ['o vento uiva para dentro da casa com as janelas fechadas', 'pegadas na neve que ficam cada vez mais distantes umas das outras', 'um frio que não sai dos ossos perto da lareira'],
             ['uma floresta do norte onde as árvores não dão sombra', 'um posto de caça isolado pela nevasca'], ['uma bota encontrada no alto de uma árvore', 'um amuleto de osso dos caçadores do norte'],
             ['olhe para cima quando o vento mudar', 'os meus pés de fogo, os meus pés que queimam']),
 'cthugha': ('cthulhu', ['as velas acendem sozinhas, com uma chama azul', 'a madeira queima de dentro para fora, sem fumaça', 'o ar treme de calor em pleno inverno'],
             ['uma casa queimada onde nada se perdeu', 'um morro onde a estrela Fomalhaut passa logo acima das árvores'], ['uma pedra que nunca esfria', 'uma página chamuscada com palavras de chamado'],
             ['quando Fomalhaut estiver sobre as árvores, diga as palavras e se afaste', 'o fogo vivo não perdoa']),
 'hydra': ('cthulhu', ['os barcos voltam vazios e as redes cheias', 'as crianças cantam uma canção que ninguém ensinou', 'a maré sobe e não desce'],
             ['uma vila de pescadores com igreja sem santo', 'uma gruta que só aparece na maré baixa'], ['uma concha que repete o seu nome', 'uma coroa de algas trançadas'],
             ['a Mãe vem buscar', 'a Mãe Hidra conhece todos os seus filhos']),
 'glaaki': ('cthulhu', ['um vizinho sorri demais, com um espinho de cristal no pescoço', 'um lago parado reflete o que não está na margem', 'gente que devia estar doente anda sem sentir dor'],
             ['as casas abandonadas perto do lago', 'o fundo de um lago que ninguém mede'], ['um volume das Revelações escrito à mão', 'um espinho de cristal guardado num lenço'],
             ['venha para o lago, aqui nada dói', 'os servos não envelhecem']),
 'baal': ('biblia', ['um trovão estoura num céu sem nuvens', 'raios caem sempre no mesmo carvalho', 'um touro de bronze aparece na praça'],
             ['um altar de pedra no alto do monte', 'um templo fenício em ruínas, ainda quente'], ['uma estatueta de um deus com raio na mão', 'uma tabuleta fenícia com o nome do senhor da tempestade'],
             ['o senhor da tempestade pede o primogênito', 'Baal cavalga as nuvens']),
 'mamon': ('biblia', ['moedas antigas aparecem nos bolsos de quem não as tinha', 'um banco abre um cofre que não está na planta', 'quem era pobre na semana passada agora compra a cidade'],
             ['o cofre de um banco centenário', 'a bolsa de valores numa manhã de pânico'], ['um contrato em letra miúda, assinado com tinta escura', 'um saco de moedas que nunca esvazia'],
             ['todos têm um preço', 'ninguém pode servir a dois senhores']),
 'moloque': ('biblia', ['um cheiro de bronze quente vem da rua, junto com tambores', 'as crianças da vila somem uma por semana', 'a fornalha da fábrica não apaga há dias'],
             ['o tofete de Cartago, cheio de urnas', 'uma fornalha de bronze em forma de touro'], ['uma urna de cinzas pequena demais', 'um tambor de couro que ninguém quer tocar'],
             ['a fornalha tem fome', 'quem alimenta prospera']),
 'tiamat': ('babilonia', ['a água do copo fica salgada', 'serpentes de muitas cabeças vistas no estuário', 'o rio corre ao contrário à noite'],
             ['as ruínas da Babilônia, junto ao rio', 'o mar raso onde dois rios se encontram'], ['uma tábua de argila com a criação do mundo', 'uma escama do tamanho de um escudo'],
             ['antes do céu ter nome, Tiamat era o mar', 'a mãe do caos quer o mundo de volta']),
 'pazuzu': ('babilonia', ['um vento quente traz febre e o zumbido de asas', 'gafanhotos cobrem o céu ao meio-dia', 'uma estatueta com asas e garras foi achada na escavação'],
             ['as ruínas de Nínive, perto de Mossul', 'um caminho no deserto onde o vento nunca para'], ['um amuleto de bronze com cara de cão e asas', 'uma cabeça de demônio pendurada na porta'],
             ['eu sou Pazuzu, filho de Hanbi, rei dos maus espíritos do ar', 'o rei dos ventos sopra']),
 'ereshkigal': ('babilonia', ['batidas no chão, vindas de baixo, sete de cada vez', 'os mortos da cidade não ficam nos túmulos', 'o pó dos túmulos aparece dentro de casa'],
             ['o cemitério real de Ur', 'uma escadaria que desce além dos sete portões'], ['uma coroa tirada no primeiro portão', 'um colar de lápis-lazúli de uma rainha morta'],
             ['mais um portão se abriu', 'os mortos vão subir e comer os vivos']),
 'marduque': ('babilonia', ['os olhos de uma estátua de ouro viraram na direção de vocês', 'alguém recita nomes na praça, um atrás do outro', 'um dragão-serpente pintado aparece nas paredes'],
             ['o templo de Esagila, na Babilônia', 'a porta de Ishtar, de tijolos azuis'], ['uma estátua de ouro de quatro olhos', 'uma tábua com os cinquenta nomes'],
             ['os cinquenta nomes estão sendo ditos', 'quem matou o caos quer governar de novo']),
 'asmodeu': ('demonologia', ['uma música de festa toca do outro lado da parede, onde não mora ninguém', 'os casamentos da cidade terminam na primeira noite', 'um perfume doce demais segue quem sai do clube'],
             ['um clube onde as festas duram três dias', 'uma casa de noivos onde sete maridos morreram'], ['um convite dourado sem nome', 'um anel com três rostos gravados'],
             ['o que você mais quer?', 'o rei dos desejos cobra tudo']),
 'astarote': ('demonologia', ['um livro que ninguém trouxe está aberto na mesa', 'freiras falam latim ao contrário', 'alguém responde perguntas que ninguém fez'],
             ['um convento fechado por ordem do bispo', 'a seção trancada de uma biblioteca antiga'], ['um grimório que se reescreve sozinho', 'uma pena de anjo enegrecida'],
             ['eu sei o seu segredo', 'Astarote sabe o passado e o futuro']),
}
for god, (area, omens, places, objs, whispers) in GODS.items():
    for t in omens: add(area, 'pressagio', t, god=god)
    for t in places: add(area, 'lugar', t, god=god)
    for t in objs: add(area, 'objeto', t, god=god)
    for t in whispers: add(area, 'sussurro', t, god=god)

# ---- general fragments (any god) --------------------------------------------------------------------------------
for t in ['os cachorros da rua latem para o nada', 'o padre da cidade não sai mais da igreja', 'uma janela que estava fechada amanhece aberta', 'o leite azeda na hora',
          'ninguém lembra quem acendeu as velas', 'um pássaro morto na soleira da porta', 'o rádio sintoniza sozinho uma estação que não existe']:
    add('geral', 'pressagio', t)
for t in ['o salão da prefeitura, depois da meia-noite', 'a estação de trem vazia', 'o sótão da pensão onde vocês dormem', 'a cripta embaixo da capela']:
    add('geral', 'lugar', t)
for t in ['uma vela preta pela metade', 'um mapa com um círculo vermelho', 'uma carta sem remetente', 'uma chave enferrujada']:
    add('geral', 'objeto', t)
for t in ['ainda não é a hora', 'ele está ouvindo', 'falta pouco', 'nenhum de vocês vai sair igual']:
    add('geral', 'sussurro', t)
for t in ['um pedaço da Lança volta para a mesa', 'a relíquia esquenta nas mãos de quem é fiel', 'a relíquia brilha, e o ar fica mais leve']:
    add('biblia', 'reliquia', t)

# ---- quotations from public-domain works (our own translation) -----------------------------------------------------
Q = [
 ('cthulhu', 'cthulhu', 'A coisa mais misericordiosa do mundo é a incapacidade da mente humana de juntar tudo o que ela sabe.', 'H. P. Lovecraft, O Chamado de Cthulhu (1928)'),
 ('cthulhu', 'cthulhu', 'Não está morto o que pode eternamente jazer, e em estranhas eras até a morte pode morrer.', 'H. P. Lovecraft, A Cidade sem Nome (1921)'),
 ('cthulhu', None, 'A emoção mais antiga e mais forte da humanidade é o medo, e o medo mais antigo e mais forte é o do desconhecido.', 'H. P. Lovecraft, O Horror Sobrenatural na Literatura (1927)'),
 ('cthulhu', 'yog', 'Yog-Sothoth conhece o portal. Yog-Sothoth é o portal. Yog-Sothoth é a chave e o guardião do portal.', 'H. P. Lovecraft, O Horror de Dunwich (1929)'),
 ('cthulhu', 'nyarlathotep', 'E foi então que Nyarlathotep saiu do Egito.', 'H. P. Lovecraft, Nyarlathotep (1920)'),
 ('cthulhu', 'dagon', 'Não consigo pensar no mar profundo sem estremecer com as coisas sem nome que podem, neste momento, rastejar no seu leito de lodo.', 'H. P. Lovecraft, Dagon (1919)'),
 ('cthulhu', 'azathoth', 'No centro de tudo, o ilimitado sultão demônio Azathoth, ao som fino e monótono de flautas malditas.', 'H. P. Lovecraft, A Busca Onírica por Kadath Desconhecida (escrito em 1927, adaptado)'),
 ('cthulhu', 'hastur', 'Estranha é a noite onde estrelas negras nascem, e estranhas luas giram pelos céus.', 'Robert W. Chambers, O Rei de Amarelo (1895), Canção de Cassilda'),
 ('cthulhu', 'hastur', 'Pela margem as ondas de nuvem quebram, os sóis gêmeos se põem atrás do lago.', 'Robert W. Chambers, O Rei de Amarelo (1895), Canção de Cassilda'),
 ('cthulhu', 'hastur', 'Você encontrou o Signo Amarelo?', 'Robert W. Chambers, O Rei de Amarelo (1895)'),
 ('cthulhu', 'ithaqua', 'Ah, ah! Os meus pés de fogo! Os meus pés que queimam!', 'Algernon Blackwood, O Wendigo (1910)'),
 ('biblia', None, 'E havia trevas sobre a face do abismo.', 'Bíblia, Gênesis 1:2 (King James, 1611)'),
 ('biblia', 'moloque', 'Não deixarás nenhum dos teus filhos passar pelo fogo para Moloque.', 'Bíblia, Levítico 18:21 (King James, 1611)'),
 ('biblia', 'mamon', 'Não podeis servir a Deus e a Mamom.', 'Bíblia, Mateus 6:24 (King James, 1611)'),
 ('biblia', 'baal', 'Ó Baal, ouve-nos! Mas não houve voz, nem quem respondesse.', 'Bíblia, 1 Reis 18:26 (King James, 1611)'),
 ('biblia', 'asmodeu', 'Asmodeu, o espírito mau, matou os sete maridos antes que se deitassem com ela.', 'Bíblia, Tobias 3:8 (apócrifos da King James, 1611)'),
 ('biblia', None, 'A nossa luta não é contra carne e sangue, mas contra os principados, contra as potestades, contra os príncipes das trevas deste mundo.', 'Bíblia, Efésios 6:12 (King James, 1611)'),
 ('biblia', None, 'Ele abriu o poço do abismo, e subiu fumaça do poço como a fumaça de uma grande fornalha.', 'Bíblia, Apocalipse 9:2 (King James, 1611)'),
 ('biblia', 'tiamat', 'E vi subir do mar uma besta que tinha sete cabeças e dez chifres.', 'Bíblia, Apocalipse 13:1 (King James, 1611)'),
 ('biblia', None, 'O meu nome é Legião, porque somos muitos.', 'Bíblia, Marcos 5:9 (King James, 1611)'),
 ('biblia', None, 'Como caíste do céu, ó Lúcifer, filho da manhã!', 'Bíblia, Isaías 14:12 (King James, 1611)'),
 ('biblia', None, 'Não há nada de novo debaixo do sol.', 'Bíblia, Eclesiastes 1:9 (King James, 1611)'),
 ('biblia', None, 'Um dos soldados furou-lhe o lado com uma lança, e logo saiu sangue e água.', 'Bíblia, João 19:34 (King James, 1611)'),
 ('biblia', None, 'Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum.', 'Bíblia, Salmos 23:4 (King James, 1611)'),
 ('biblia', 'marduque', 'MENE, MENE, TEQUEL, PARSIM.', 'Bíblia, Daniel 5:25 (King James, 1611)'),
 ('biblia', 'marduque', 'Babilônia foi um cálice de ouro na mão do Senhor, que embriagava toda a terra.', 'Bíblia, Jeremias 51:7 (King James, 1611)'),
 ('biblia', 'tiamat', 'Podes tirar o leviatã com um anzol?', 'Bíblia, Jó 41:1 (King James, 1611)'),
 ('babilonia', 'tiamat', 'Quando lá em cima o céu ainda não tinha nome, e embaixo a terra não tinha nome, e Apsu, o primeiro, e Tiamat, o caos, a mãe de todos, misturavam as suas águas.', 'Enuma Elish, tábua I (tradução de L. W. King, 1902)'),
 ('babilonia', 'marduque', 'Pelos seus cinquenta nomes os grandes deuses proclamaram Marduque.', 'Enuma Elish, tábua VII (adaptado da tradução de L. W. King, 1902)'),
 ('babilonia', 'ereshkigal', 'Vou quebrar a porta e partir a tranca; farei os mortos subirem para devorar os vivos.', 'A Descida de Ishtar ao Mundo dos Mortos (adaptado da tradução de R. W. Rogers, 1912)'),
 ('demonologia', 'asmodeu', 'Tem três cabeças: a primeira de touro, a segunda de homem e a terceira de carneiro.', 'A Chave Menor de Salomão, Goécia (tradução de S. L. MacGregor Mathers, 1904)'),
 ('demonologia', 'baal', 'Fala com voz rouca, e torna invisível quem o chama.', 'A Chave Menor de Salomão, Goécia (adaptado da tradução de Mathers, 1904)'),
 ('demonologia', 'astarote', 'Aparece como um anjo nocivo montado num dragão; não o deixe chegar perto, pelo hálito venenoso.', 'A Chave Menor de Salomão, Goécia (adaptado da tradução de Mathers, 1904)'),
 ('babilonia', 'pazuzu', 'Eu sou Pazuzu, filho de Hanbi, rei dos maus espíritos do ar.', 'Inscrição de uma estatueta assíria de Pazuzu (Louvre, cerca de 800–600 a.C., adaptado)'),
]
for area, god, text, src in Q:
    add(area, 'citacao', text, source=src, god=god, date=CHECK)

json.dump(F, open(OUT / 'fragments.json', 'w'), ensure_ascii=False, indent=1)

# ---- templates per moment ------------------------------------------------------------------------------------------
T = {
 'abertura': ['Vocês chegam a {lugar}. Logo na primeira noite, {pressagio}.', 'Ninguém quis vir até {lugar}, mas todos vieram. {pressagio}.', 'Alguém deixou {objeto} na porta de vocês. Num bilhete: “{sussurro}”.'],
 'lei-L': ['{pres} e {chanc} voltam com mais um pedaço da Lança. {reliquia}.', 'Mais uma relíquia, trazida por {pres} e {chanc}. Lá fora, alguém para de cantar.', '{chanc} guarda a relíquia. Por uma noite, {lugar} fica em silêncio.'],
 'lei-F': ['Sob {pres} e {chanc}, mais uma página foi lida. {pressagio}.', '{chanc} vira a página, e a tinta ainda está fresca. Alguém sussurra: “{sussurro}”.', 'Mais uma página do Necronomicon. Em {lugar}, {pressagio}.'],
 'rejeicao': ['A mesa não confia em {pres} e {chanc}. Enquanto discutem, {pressagio}.', 'Governo recusado. Cada minuto perdido é um minuto a mais para o culto.'],
 'caos': ['Ninguém governa, e a cidade se governa sozinha. {pressagio}.', 'Sem governo, {objeto} passa de mão em mão até alguém ler o que não devia.'],
 'veto': ['{pres} e {chanc} rasgam as duas folhas. Nem relíquia, nem página: só medo.'],
 'investigacao': ['{pres} chama {target} para uma conversa a portas fechadas, em {lugar}. Só um dos dois sai sabendo a verdade.', '{pres} revira os papéis de {target} e acha {objeto}. O que isso quer dizer, só {pres} sabe.'],
 'eliminacao': ['{pres} decide, e {target} não volta para a mesa. {pressagio}.', '{target} cai em {lugar}. Ninguém sabe ainda se a mesa ficou mais segura.'],
 'ato2': ['A coisa toda fica pior. {pressagio}, e alguém escreveu na parede: “{sussurro}”.', '“{citacao}”'],
 'ato3': ['Falta pouco. Em {lugar}, o culto já acende as velas. “{sussurro}”.', '“{citacao}” As palavras estão em todas as bocas.'],
 'fim-L': ['A última relíquia volta para o lugar. Em {lugar}, o silêncio dura até o amanhecer.', '“{citacao}” Desta vez, as trevas recuam.'],
 'fim-F': ['O ritual termina em {lugar}. {pressagio}, e não vai parar mais.', 'A última página é lida em voz alta: “{sussurro}”.'],
}
json.dump([{'campaign': C, 'moment': m, 'text': t} for m, ts in T.items() for t in ts], open(OUT / 'templates.json', 'w'), ensure_ascii=False, indent=1)
print(len(F), 'fragmentos,', sum(len(v) for v in T.values()), 'moldes')
