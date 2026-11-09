"""Sends corpus/*.json straight to Supabase with the service key (used by the Ingestão workflow after a merge).
    SUPABASE_URL=... SUPABASE_SERVICE_KEY=... python3 scripts/ingest.py"""
import json, os, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from app.store import SupabaseStore
ROOT = pathlib.Path(__file__).resolve().parent.parent
url, key = os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SERVICE_KEY')
if not url or not key:
    sys.exit('faltam SUPABASE_URL e SUPABASE_SERVICE_KEY')
s = SupabaseStore(url, key)
F = json.load(open(ROOT / 'corpus/fragments.json')); T = json.load(open(ROOT / 'corpus/templates.json'))
nf = sum(s.add_fragments(F[i:i + 100]) for i in range(0, len(F), 100))
nt = s.add_templates(T)
print(f'novos: {nf} fragmentos, {nt} moldes (de {len(F)} e {len(T)})')
