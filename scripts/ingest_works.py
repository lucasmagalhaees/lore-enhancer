"""Downloads each work of corpus/sources.json, cuts it into tagged passages (app/parse.py) and adds them to Supabase.
Runs in the workflow 'ingestão de obras'; adding is idempotent.
    SUPABASE_URL=... SUPABASE_SECRET_KEY=... python3 scripts/ingest_works.py [--dry]"""
import json, os, pathlib, sys
import httpx
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from app.parse import fragments
from app.store import SupabaseStore, MemoryStore
ROOT = pathlib.Path(__file__).resolve().parent.parent
dry = '--dry' in sys.argv
url, key = os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SECRET_KEY') or os.environ.get('SUPABASE_SERVICE_KEY')
if not dry and (not url or not key):
    sys.exit('faltam SUPABASE_URL e SUPABASE_SECRET_KEY (ou rode com --dry)')
store = MemoryStore() if dry else SupabaseStore(url, key)
total = 0
for w in json.load(open(ROOT / 'corpus/sources.json')):
    r = httpx.get(w['url'], timeout=60, follow_redirects=True)
    if r.status_code != 200:
        print(f"FALHOU {w['source']}: {r.status_code}"); continue
    rows = fragments(r.text, campaign=w['campaign'], area=w['area'], source=w['source'], lang=w['lang'], source_date=w.get('source_date'),
                     god=w.get('god'), untagged_max=w.get('untagged_max', 100))
    added = sum(store.add_fragments(rows[i:i + 500]) for i in range(0, len(rows), 500))
    gods = {x['god'] for x in rows if x['god']}
    print(f"{w['source']}: {len(rows)} trechos ({added} novos), deuses: {', '.join(sorted(gods)) or 'nenhum'}")
    total += added
print(f'total de novos: {total}')
