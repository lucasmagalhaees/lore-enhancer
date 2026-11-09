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


# ---- D6: more for each god (omens, a place, an object, a whisper) ---------------------------------------------------
MORE = {
 'cthulhu': (['as gaivotas voam em círculos sobre um ponto do mar onde não há nada', 'os sonhos de toda a cidade, esta noite, têm a mesma arquitetura errada'], 'um farol apagado que ainda gira', 'uma pedra verde que sua água do mar', 'quando as estrelas estiverem certas'),
 'nyarlathotep': (['os cachorros fogem quando um certo homem passa', 'um professor do Cairo dá aulas que ninguém lembra de ter assistido'], 'uma sala de cinema que só passa um filme', 'uma máscara de faraó sem rosto atrás', 'eu tenho mil formas e todas sorriem'),
 'hastur': (['um ator esqueceu o próprio nome no meio da fala', 'as estrelas do céu estão negras e brilham mesmo assim'], 'uma pensão de artistas com um quarto que não se aluga', 'uma máscara pálida que não sai do rosto', 'eu não uso máscara'),
 'shub': (['as vacas da fazenda deram cria todas na mesma noite', 'um cheiro de terra revirada e leite azedo'], 'um bosque onde as árvores parecem ajoelhadas', 'um chifre de bode entalhado com rostos', 'mil filhotes, e nenhum se parece com a mãe'),
 'yog': (['a porta do armário dá para um lugar que não é o armário', 'os gêmeos da fazenda vizinha não são gêmeos de verdade'], 'uma casa de fazenda com as janelas pregadas por dentro', 'um anel com uma esfera iridescente', 'todos os tempos são um só'),
 'dagon': (['o padre da vila parou de rezar e começou a pescar', 'um sino toca debaixo da água'], 'um salão da Ordem Esotérica de Dagon', 'uma estatueta de peixe com braços humanos', 'Iä! Iä! O Pai Dagon sobe!'),
 'azathoth': (['as notas do piano soam fora do tempo, como se alguém tocasse com mãos demais', 'um relógio anda para trás e ninguém se espanta'], 'uma sala de concertos vazia onde alguém ensaia', 'um tambor de pele que ninguém reconhece', 'os deuses dançam em volta dele sem saber por quê'),
 'tsathoggua': (['um bocejo enorme ecoa da caverna', 'os morcegos da mina saíram todos de uma vez'], 'um poço antigo com degraus que descem em espiral', 'uma tigela de pedra com restos de oferenda', 'ele tem fome só às vezes'),
 'ithaqua': (['as árvores estão cobertas de gelo por dentro', 'alguém grita lá do alto, e a voz vai ficando mais fraca'], 'um lago congelado com rachaduras em forma de pegada', 'um gorro de pele achado longe de qualquer casa', 'quem anda com o vento não volta a pisar no chão'),
 'cthugha': (['as brasas da lareira formam letras', 'as lâmpadas estouram uma por uma'], 'uma fundição abandonada que ainda está quente', 'um isqueiro que acende com chama azul', 'tudo vira cinza, e a cinza também queima'),
 'hydra': (['os peixes do mercado olham para quem passa', 'a água do poço sobe até a boca e para'], 'um cais de madeira apodrecida que ninguém usa', 'um véu de rede de pesca', 'todos os filhos voltam para a Mãe'),
 'glaaki': (['os rostos no lago sorriem antes de você', 'a vizinhança inteira parou de envelhecer'], 'uma casa de veraneio onde ninguém tem pressa de sair', 'um volume de capa verde que dá sono', 'aqui ninguém chora'),
 'baal': (['um touro escapou do curral e foi deitar no altar', 'chove só em cima de uma casa'], 'um campo de trigo queimado por raios em linha reta', 'um chifre de touro coberto de bronze', 'dê a ele o primeiro e ele te dá a chuva'),
 'mamon': (['os mendigos da praça sumiram, e com eles as dívidas', 'o cofre da igreja amanheceu cheio'], 'um escritório de penhores aberto à meia-noite', 'uma balança que pesa almas', 'quanto você vale?'),
 'moloque': (['o sino da escola não toca mais', 'cinzas caem do céu num dia sem incêndio'], 'um vale onde os pais deixam presentes que ninguém pega', 'um carrinho de criança vazio na frente da fábrica', 'o fogo é um pai que não dorme'),
 'tiamat': (['a cisterna da cidade virou salgada', 'serpentes aparecem nas pias'], 'um pântano onde a água doce e a salgada não se misturam', 'um selo cilíndrico com um dragão de muitas cabeças', 'eu sou o mar antes do mundo'),
 'pazuzu': (['as crianças da casa falam com a voz de um velho', 'o vento sopra sempre do sudoeste'], 'um telhado onde ficam pendurados amuletos contra o vento', 'uma placa de bronze com a cabeça do demônio', 'eu trago a peste e levo o que quero'),
 'ereshkigal': (['as velas do velório se apagam todas juntas', 'alguém bate na tampa de um caixão já enterrado'], 'um porão de sete portas', 'uma balança de pesar mortos', 'tire as suas joias, uma por portão'),
 'marduque': (['um dragão de tijolos azuis parece se mexer no muro', 'alguém trocou os nomes das ruas por nomes de deuses'], 'um zigurate de sete andares de tijolo cru', 'uma lança de bronze com cabeça de dragão', 'eu matei o caos e fiz o mundo, e posso desfazer'),
 'asmodeu': (['as alianças de casamento ficam pretas', 'alguém ri do outro lado de todas as paredes'], 'um quarto de núpcias com sete camas', 'um espelho que mostra o que você quer', 'você pode ter tudo, e só vai custar você'),
 'astarote': (['os sinos da igreja tocam ao contrário', 'cartas antigas aparecem respondidas'], 'uma cela de convento com as paredes riscadas de nomes', 'uma lista com o nome de todos da mesa', 'pergunte, e eu respondo a verdade'),
}
for god, (omens, place, obj, whisper) in MORE.items():
    area = GODS[god][0]
    for t in omens: add(area, 'pressagio', t, god=god)
    add(area, 'lugar', place, god=god); add(area, 'objeto', obj, god=god); add(area, 'sussurro', whisper, god=god)

for t in ['a lâmpada da rua pisca no ritmo de uma respiração', 'o espelho do corredor está virado para a parede', 'ninguém ouviu o galo cantar hoje', 'há terra de cemitério nos sapatos de alguém da mesa',
          'uma criança desenhou vocês todos, e um está de túnica', 'a farmácia esgotou o láudano', 'o telegrafista da estação pediu demissão sem explicar']:
    add('geral', 'pressagio', t)
for t in ['a biblioteca municipal, depois de fechada', 'o hospício no alto da colina', 'o necrotério da delegacia', 'uma igreja anglicana sem fiéis', 'o porão da universidade']:
    add('geral', 'lugar', t)
for t in ['um revólver com uma bala só', 'uma fotografia com um rosto riscado', 'um frasco de água benta pela metade', 'um diário com as últimas páginas arrancadas']:
    add('geral', 'objeto', t)
for t in ['um de vocês já é nosso', 'conte de novo quantos são', 'as velas já estão acesas']:
    add('geral', 'sussurro', t)
for t in ['a Lança ainda tem sangue na ponta', 'a relíquia pesa mais nas mãos de quem mente', 'um sino toca longe quando a relíquia é tocada']:
    add('biblia', 'reliquia', t)

# ---- D6: more public-domain quotations (our own translation), tagged by god or by the moment they fit -------------
Q2 = [
 # Lovecraft (died 1937; public domain in Brazil since 2008)
 ('cthulhu', None, None, 'Vivemos numa ilha plácida de ignorância, no meio de mares negros de infinito.', 'H. P. Lovecraft, O Chamado de Cthulhu (1928)'),
 ('cthulhu', None, 'abertura', 'A oeste de Arkham as colinas se erguem selvagens, e há vales com matas fundas que nenhum machado jamais cortou.', 'H. P. Lovecraft, A Cor que Caiu do Espaço (1927)'),
 ('cthulhu', None, None, 'Infeliz é aquele a quem as lembranças da infância só trazem medo e tristeza.', 'H. P. Lovecraft, O Estranho (1926)'),
 ('cthulhu', 'dagon', 'abertura', 'Escrevo isto sob uma pressão mental considerável, pois esta noite já não existirei.', 'H. P. Lovecraft, Dagon (1919)'),
 ('cthulhu', None, 'abertura', 'Quem procura o horror frequenta lugares estranhos e distantes.', 'H. P. Lovecraft, A Imagem na Casa (1921)'),
 ('cthulhu', None, 'eliminacao', 'Seu tolo, o Warren está MORTO!', 'H. P. Lovecraft, O Depoimento de Randolph Carter (1920)'),
 ('cthulhu', None, None, 'Há na terra de Mnar um grande lago parado, que nenhum rio alimenta e de onde nenhum rio sai.', 'H. P. Lovecraft, A Maldição que Caiu sobre Sarnath (1920)'),
 ('cthulhu', None, None, 'Em Ulthar, que fica além do rio Skai, nenhum homem pode matar um gato.', 'H. P. Lovecraft, Os Gatos de Ulthar (1920)'),
 ('cthulhu', None, 'ato3', 'Ao longe, um latido fraco, como o de um cão gigantesco.', 'H. P. Lovecraft, O Cão (1924, adaptado)'),
 ('cthulhu', None, 'ato3', 'Tekeli-li! Tekeli-li!', 'H. P. Lovecraft, Nas Montanhas da Loucura (1936)'),
 ('cthulhu', 'cthulhu', 'ato3', 'Iä! Iä! Cthulhu fhtagn!', 'H. P. Lovecraft, O Chamado de Cthulhu (1928)'),
 # Robert W. Chambers (1895), Ambrose Bierce (1886)
 ('cthulhu', 'hastur', None, 'Não sobre nós, ó Rei, não sobre nós!', 'Robert W. Chambers, O Rei de Amarelo (1895)'),
 ('cthulhu', 'hastur', 'ato2', 'A canção que as Híades cantam, onde os farrapos do Rei esvoaçam, há de morrer sem ser ouvida na Carcosa sombria.', 'Robert W. Chambers, O Rei de Amarelo (1895), Canção de Cassilda'),
 ('cthulhu', 'hastur', None, 'Há muitos tipos de morte: em alguns o corpo fica; em outros ele some junto com o espírito.', 'Ambrose Bierce, Um Habitante de Carcosa (1886)'),
 # Poe (died 1849)
 ('literatura', None, 'eliminacao', 'E as Trevas e a Ruína e a Morte Rubra tiveram domínio sem limite sobre todos.', 'Edgar Allan Poe, A Máscara da Morte Rubra (1842)'),
 ('literatura', None, None, 'Disse o corvo: “Nunca mais.”', 'Edgar Allan Poe, O Corvo (1845)'),
 ('literatura', None, None, 'Tudo o que vemos ou parecemos não passa de um sonho dentro de um sonho.', 'Edgar Allan Poe, Um Sonho dentro de um Sonho (1849)'),
 ('literatura', None, 'investigacao', 'Era a batida do seu coração horrendo!', 'Edgar Allan Poe, O Coração Delator (1843)'),
 ('literatura', None, 'abertura', 'Durante todo um dia escuro, sombrio e sem som, no outono do ano.', 'Edgar Allan Poe, A Queda da Casa de Usher (1839)'),
 ('literatura', None, 'eliminacao', 'Pelo amor de Deus, Montresor!', 'Edgar Allan Poe, O Barril de Amontillado (1846)'),
 # Stoker (1897), Mary Shelley (1818), M. R. James (1904)
 ('literatura', None, 'abertura', 'Bem-vindo à minha casa! Entre livremente, e por vontade própria!', 'Bram Stoker, Drácula (1897)'),
 ('literatura', None, 'ato2', 'Escutem, os filhos da noite. Que música eles fazem!', 'Bram Stoker, Drácula (1897)'),
 ('literatura', None, None, 'Cuidado, pois não tenho medo, e por isso sou poderoso.', 'Mary Shelley, Frankenstein (1818)'),
 ('literatura', None, 'abertura', 'Quem é este que vem?', 'M. R. James, Oh, Assobie e Eu Irei até Você (1904), a inscrição do apito'),
 # Shakespeare, Dante (Longfellow, 1867), Milton (1667)
 ('literatura', None, 'ato2', 'Pelo comichão dos meus polegares, algo malvado vem para cá.', 'William Shakespeare, Macbeth (1623)'),
 ('literatura', None, 'ato3', 'Dobra, dobra, labuta e mágoa; queime o fogo e ferva a água.', 'William Shakespeare, Macbeth (1623)'),
 ('literatura', None, None, 'Há mais coisas entre o céu e a terra, Horácio, do que sonha a sua filosofia.', 'William Shakespeare, Hamlet (1603)'),
 ('literatura', None, 'ato3', 'Agora é a hora mais enfeitiçada da noite, quando os cemitérios bocejam.', 'William Shakespeare, Hamlet (1603)'),
 ('literatura', None, 'investigacao', 'Há algo de podre no reino da Dinamarca.', 'William Shakespeare, Hamlet (1603)'),
 ('literatura', None, 'abertura', 'No meio do caminho da nossa vida, eu me achei numa floresta escura.', 'Dante Alighieri, Inferno, canto I (tradução de Longfellow, 1867)'),
 ('literatura', None, 'fim-F', 'Abandonai toda a esperança, vós que entrais.', 'Dante Alighieri, Inferno, canto III (tradução de Longfellow, 1867)'),
 ('literatura', None, 'fim-F', 'Melhor reinar no Inferno do que servir no Céu.', 'John Milton, O Paraíso Perdido (1667)'),
 ('literatura', None, None, 'A mente é o seu próprio lugar, e nela pode fazer do Inferno um Céu e do Céu um Inferno.', 'John Milton, O Paraíso Perdido (1667)'),
 # Augusto dos Anjos (died 1914), in the original Portuguese
 ('literatura', None, 'eliminacao', 'Vês?! Ninguém assistiu ao formidável enterro de tua última quimera.', 'Augusto dos Anjos, Versos Íntimos, em Eu (1912)'),
 ('literatura', None, 'investigacao', 'O beijo, amigo, é a véspera do escarro, a mão que afaga é a mesma que apedreja.', 'Augusto dos Anjos, Versos Íntimos, em Eu (1912)'),
 # The Bible, King James (1611)
 ('biblia', None, 'investigacao', 'Guardai-vos dos falsos profetas, que vêm a vós vestidos de ovelhas, mas por dentro são lobos devoradores.', 'Bíblia, Mateus 7:15 (King James, 1611)'),
 ('biblia', None, 'rejeicao', 'A mão daquele que me trai está comigo à mesa.', 'Bíblia, Lucas 22:21 (King James, 1611)'),
 ('biblia', None, 'rejeicao', 'Em verdade vos digo que um de vós me trairá.', 'Bíblia, Mateus 26:21 (King James, 1611)'),
 ('biblia', None, 'investigacao', 'Quando ele falar com doçura, não acredites, porque há sete abominações no seu coração.', 'Bíblia, Provérbios 26:25 (King James, 1611)'),
 ('biblia', None, 'investigacao', 'O próprio Satanás se transfigura em anjo de luz.', 'Bíblia, 2 Coríntios 11:14 (King James, 1611)'),
 ('biblia', None, 'eliminacao', 'Até o meu amigo íntimo, em quem eu confiava, levantou contra mim o calcanhar.', 'Bíblia, Salmos 41:9 (King James, 1611)'),
 ('biblia', None, 'ato3', 'Olhei, e eis um cavalo amarelo, e o que estava montado nele chamava-se Morte, e o Inferno o seguia.', 'Bíblia, Apocalipse 6:8 (King James, 1611)'),
 ('biblia', None, 'ato2', 'O vosso adversário, o diabo, anda em derredor, como leão que ruge, buscando a quem possa tragar.', 'Bíblia, 1 Pedro 5:8 (King James, 1611)'),
 ('biblia', None, None, 'Também os demônios creem, e estremecem.', 'Bíblia, Tiago 2:19 (King James, 1611)'),
 ('biblia', None, None, 'De rodear a terra, e de passear por ela.', 'Bíblia, Jó 1:7 (King James, 1611)'),
 ('biblia', 'astarote', None, 'Quem aumenta o conhecimento aumenta a dor.', 'Bíblia, Eclesiastes 1:18 (King James, 1611)'),
 ('biblia', 'mamon', None, 'O amor ao dinheiro é a raiz de todos os males.', 'Bíblia, 1 Timóteo 6:10 (King James, 1611)'),
 ('biblia', 'dagon', None, 'Os príncipes dos filisteus se reuniram para oferecer um grande sacrifício a Dagom, o seu deus.', 'Bíblia, Juízes 16:23 (King James, 1611)'),
 ('biblia', 'dagon', 'fim-L', 'Dagom estava caído com o rosto em terra diante da arca do Senhor.', 'Bíblia, 1 Samuel 5:4 (King James, 1611)'),
 ('biblia', 'baal', None, 'Ide e consultai Baal-Zebube, deus de Ecrom.', 'Bíblia, 2 Reis 1:2 (King James, 1611)'),
 ('biblia', 'moloque', None, 'Edificaram os altos de Baal, para fazerem passar pelo fogo os seus filhos e as suas filhas a Moloque.', 'Bíblia, Jeremias 32:35 (King James, 1611)'),
 ('biblia', 'hydra', None, 'Naquele dia o Senhor castigará o leviatã, a serpente veloz, o dragão que está no mar.', 'Bíblia, Isaías 27:1 (King James, 1611)'),
 ('biblia', 'marduque', None, 'As feras do deserto repousarão ali, e as suas casas se encherão de corujas, e os sátiros pularão ali.', 'Bíblia, Isaías 13:21 (King James, 1611)'),
 ('biblia', 'marduque', 'fim-L', 'Caiu, caiu a grande Babilônia, e se tornou morada de demônios.', 'Bíblia, Apocalipse 18:2 (King James, 1611)'),
 ('biblia', 'marduque', 'ato3', 'MISTÉRIO, A GRANDE BABILÔNIA, A MÃE DAS PROSTITUIÇÕES E ABOMINAÇÕES DA TERRA.', 'Bíblia, Apocalipse 17:5 (King James, 1611)'),
 ('biblia', 'marduque', 'ato2', 'Apareceram uns dedos de mão de homem, e escreviam na parede do palácio do rei.', 'Bíblia, Daniel 5:5 (King James, 1611)'),
 ('biblia', None, 'abertura', 'E a terra era sem forma e vazia.', 'Bíblia, Gênesis 1:2 (King James, 1611)'),
 ('biblia', None, 'fim-L', 'Revesti-vos de toda a armadura de Deus, para que possais estar firmes contra as ciladas do diabo.', 'Bíblia, Efésios 6:11 (King James, 1611)'),
 ('biblia', None, None, 'Não terás outros deuses diante de mim.', 'Bíblia, Êxodo 20:3 (King James, 1611)'),
 ('biblia', None, None, 'Azazel ensinou os homens a fazer espadas e facas, escudos e couraças.', 'Livro de Enoque 8:1 (tradução de R. H. Charles, 1912)'),
 # The Goetia (Mathers, 1904)
 ('demonologia', 'baal', None, 'O primeiro espírito principal é um rei que governa no Oriente, chamado Bael.', 'A Chave Menor de Salomão, Goécia (tradução de Mathers, 1904)'),
 ('demonologia', None, None, 'Belial foi criado logo depois de Lúcifer.', 'A Chave Menor de Salomão, Goécia (adaptado da tradução de Mathers, 1904)'),
]
for area, god, moment, text, src in Q2:
    add(area, 'citacao', text, source=src, god=god, moment=moment, date=CHECK)

json.dump(F, open(OUT / 'fragments.json', 'w'), ensure_ascii=False, indent=1)

# ---- templates per moment ------------------------------------------------------------------------------------------
T = {
 'abertura': ['“{citacao}” Foi assim que começou, em {lugar}.', 'O telegrama dizia só o endereço: {lugar}. Na mesa da entrada, {objeto}.', 'Vocês chegam a {lugar}. Logo na primeira noite, {pressagio}.', 'Ninguém quis vir até {lugar}, mas todos vieram. {pressagio}.', 'Alguém deixou {objeto} na porta de vocês. Num bilhete: “{sussurro}”.'],
 'lei-L': ['{pres} e {chanc} acham a relíquia escondida junto com {objeto}. {reliquia}.', '{pres} e {chanc} voltam com mais um pedaço da Lança. {reliquia}.', 'Mais uma relíquia, trazida por {pres} e {chanc}. Lá fora, alguém para de cantar.', '{chanc} guarda a relíquia. Por uma noite, {lugar} fica em silêncio.'],
 'lei-F': ['A página que {pres} e {chanc} deixaram passar fala de {lugar}. Desde então, {pressagio}.', 'Sob {pres} e {chanc}, mais uma página foi lida. {pressagio}.', '{chanc} vira a página, e a tinta ainda está fresca. Alguém sussurra: “{sussurro}”.', 'Mais uma página do Necronomicon. Em {lugar}, {pressagio}.'],
 'rejeicao': ['“{citacao}” Ninguém diz em voz alta, mas todos pensam.', 'A mesa não confia em {pres} e {chanc}. Enquanto discutem, {pressagio}.', 'Governo recusado. Cada minuto perdido é um minuto a mais para o culto.'],
 'caos': ['Sem ninguém no comando, alguém pendura {objeto} na porta da prefeitura. “{sussurro}”.', 'Ninguém governa, e a cidade se governa sozinha. {pressagio}.', 'Sem governo, {objeto} passa de mão em mão até alguém ler o que não devia.'],
 'veto': ['O veto cai como uma pedra. Lá fora, alguém sussurra: “{sussurro}”.', '{pres} e {chanc} rasgam as duas folhas. Nem relíquia, nem página: só medo.'],
 'investigacao': ['{pres} olha {target} nos olhos e lembra: “{citacao}”', '{pres} chama {target} para uma conversa a portas fechadas, em {lugar}. Só um dos dois sai sabendo a verdade.', '{pres} revira os papéis de {target} e acha {objeto}. O que isso quer dizer, só {pres} sabe.'],
 'eliminacao': ['{target} cai. Alguém murmura: “{citacao}”', 'A cadeira de {target} fica vazia. {pressagio}.', '{pres} decide, e {target} não volta para a mesa. {pressagio}.', '{target} cai em {lugar}. Ninguém sabe ainda se a mesa ficou mais segura.'],
 'ato2': ['A coisa ganha nome em {lugar}. Alguém achou {objeto}, e desde então {pressagio}.', 'A coisa toda fica pior. {pressagio}, e alguém escreveu na parede: “{sussurro}”.', '“{citacao}”'],
 'ato3': ['Falta pouco. Em {lugar}, o culto já acende as velas. “{sussurro}”.', '“{citacao}” As palavras estão em todas as bocas.'],
 'fim-L': ['O culto se dispersa, e {objeto} fica para trás em {lugar}. Ninguém toca nele.', 'A última relíquia volta para o lugar. Em {lugar}, o silêncio dura até o amanhecer.', '“{citacao}” Desta vez, as trevas recuam.'],
 'fim-F': ['“{citacao}”', 'O ritual termina em {lugar}. {pressagio}, e não vai parar mais.', 'A última página é lida em voz alta: “{sussurro}”.'],
}
json.dump([{'campaign': C, 'moment': m, 'text': t} for m, ts in T.items() for t in ts], open(OUT / 'templates.json', 'w'), ensure_ascii=False, indent=1)
print(len(F), 'fragmentos,', sum(len(v) for v in T.values()), 'moldes')
