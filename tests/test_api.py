import json, pathlib, re
import pytest
from fastapi.testclient import TestClient
from app import main
from app.compose import compose, GAP
from app.store import MemoryStore

ROOT = pathlib.Path(__file__).resolve().parent.parent
F = json.load(open(ROOT / 'corpus/fragments.json'))
T = json.load(open(ROOT / 'corpus/templates.json'))
MOMENTS = ['abertura', 'lei-L', 'lei-F', 'rejeicao', 'caos', 'veto', 'investigacao', 'eliminacao', 'ato2', 'ato3', 'fim-L', 'fim-F']
GODS = sorted({f['god'] for f in F if f['god']})
NAMES = {'pres': 'Ana', 'chanc': 'Beto', 'target': 'Caio'}


@pytest.fixture
def store():
    s = MemoryStore(); s.add_fragments(F); s.add_templates(T); return s


@pytest.fixture
def client(store, monkeypatch):
    main.app.dependency_overrides[main.store] = lambda: store
    yield TestClient(main.app)
    main.app.dependency_overrides.clear()


def test_corpus_is_sound():
    assert len(F) >= 200 and len({(f['campaign'], f['kind'], f['text']) for f in F}) == len(F), 'no repeated fragment'
    assert all(f['source'] and f['area'] and f['kind'] for f in F)
    quoted = [f for f in F if f['kind'] == 'citacao']
    assert quoted and all(f['source_date'] and re.search(r'\(.*\d{3,4}', f['source']) for f in quoted), 'every quotation names its work and year'
    assert {t['moment'] for t in T} == set(MOMENTS)


def test_every_god_has_omen_place_object_and_whisper():
    assert len(GODS) == 21
    for g in GODS:
        kinds = {f['kind'] for f in F if f['god'] == g}
        assert {'pressagio', 'lugar', 'objeto', 'sussurro'} <= kinds, g


def test_every_moment_composes_for_every_god_without_a_gap(store):
    for g in GODS:
        for m in MOMENTS:
            out = compose(store, 'secret-cultist', m, g, seed=7, names=NAMES)
            assert out and not GAP.search(out['text']), (g, m)


def test_same_seed_same_line_and_the_god_comes_first(store):
    a = compose(store, 'secret-cultist', 'lei-F', 'hastur', seed=3, names=NAMES)
    assert a == compose(store, 'secret-cultist', 'lei-F', 'hastur', seed=3, names=NAMES)
    lines = {compose(store, 'secret-cultist', 'abertura', 'hastur', seed=s)['text'] for s in range(40)}
    assert len(lines) > 5, 'variety'
    hastur = {f['text'] for f in F if f['god'] == 'hastur'}
    assert all(any(h in l for h in hastur) for l in lines), 'a god that has its own fragments uses them'


def test_a_gap_nothing_can_fill_gives_no_line():
    s = MemoryStore(); s.add_templates([{'campaign': 'x', 'moment': 'm', 'text': 'Em {lugar}.'}])
    assert compose(s, 'x', 'm') is None and compose(s, 'x', 'other') is None


def test_health(client):
    assert client.get('/health').json() == {'ok': True, 'version': main.VERSION, 'store': 'MemoryStore'}


def test_lore_and_fragments(client):
    r = client.get('/lore', params={'campaign': 'secret-cultist', 'moment': 'eliminacao', 'god': 'moloque', 'seed': 1, 'pres': 'Ana', 'target': 'Caio'})
    assert r.status_code == 200 and 'Caio' in r.json()['text'] and r.json()['sources']
    assert client.get('/lore', params={'campaign': 'secret-cultist', 'moment': 'nada'}).status_code == 404
    got = client.get('/fragments', params={'campaign': 'secret-cultist', 'kind': 'citacao', 'god': 'marduque'}).json()
    assert got and all(f['god'] in ('marduque', None) for f in got)
    assert all('babil' in f['text'].lower() for f in client.get('/fragments', params={'campaign': 'secret-cultist', 'q': 'babil'}).json())


def test_ingest_needs_a_supabase_login(client, monkeypatch):
    body = {'fragments': [{'campaign': 'secret-cultist', 'area': 'geral', 'kind': 'pressagio', 'text': 'um corvo na janela', 'source': 'teste'}]}
    assert client.post('/ingest', json=body).status_code == 401
    monkeypatch.setenv('SUPABASE_URL', 'https://exemplo.supabase.co'); monkeypatch.setenv('SUPABASE_ANON_KEY', 'anon')

    class R:
        def __init__(self, code): self.status_code = code
        def json(self): return {'email': 'lucas@exemplo.com'}
    monkeypatch.setattr(main.httpx, 'get', lambda *a, **k: R(401))
    assert client.post('/ingest', json=body, headers={'authorization': 'Bearer x'}).status_code == 401
    monkeypatch.setattr(main.httpx, 'get', lambda *a, **k: R(200))
    ok = client.post('/ingest', json=body, headers={'authorization': 'Bearer x'}).json()
    assert ok == {'fragments': 1, 'templates': 0, 'by': 'lucas@exemplo.com'}
    assert client.post('/ingest', json=body, headers={'authorization': 'Bearer x'}).json()['fragments'] == 0, 'the same text twice is kept once'


def test_seed_sql_matches_the_corpus():
    sql = (ROOT / 'sql/seed.sql').read_text()
    assert sql.count('\n(') + 2 >= len(F) + len(T) - 2 and "Robert W. Chambers" in sql, 'run scripts/seed_sql.py after changing corpus/'


def test_tidy_joins_prepositions_and_capitalizes():
    from app.compose import tidy
    assert tidy('vocês chegam a o porão. a relíquia brilha em uma noite de os mortos, a a beira') == 'Vocês chegam ao porão. A relíquia brilha numa noite dos mortos, à beira'


def test_new_secret_keys_go_only_in_apikey():
    from app.store import SupabaseStore
    assert SupabaseStore('https://x.supabase.co', 'sb_secret_abc').h == {'apikey': 'sb_secret_abc'}
    assert SupabaseStore('https://x.supabase.co', 'eyJlegacy').h['authorization'] == 'Bearer eyJlegacy'


def test_a_quote_made_for_the_moment_beats_a_general_one(store):
    out = compose(store, 'secret-cultist', 'rejeicao', 'cthulhu', seed=0, names=NAMES)
    lines = {compose(store, 'secret-cultist', 'rejeicao', 'cthulhu', seed=s, names=NAMES)['text'] for s in range(30)}
    quoted = [l for l in lines if l.startswith('“')]
    assert out and quoted and all(('trai' in l) for l in quoted), 'a quote in a betrayal moment is about betrayal'
