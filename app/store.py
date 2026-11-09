"""Where the fragments and templates live: in memory (tests, local runs) or in Supabase (production, through its REST API)."""
from __future__ import annotations
import os
from typing import Protocol
import httpx

Row = dict


class Store(Protocol):
    def add_fragments(self, rows: list[Row]) -> int: ...
    def add_templates(self, rows: list[Row]) -> int: ...
    def fragments(self, campaign: str, kind: str | None = None, god: str | None = None, moment: str | None = None, q: str | None = None, lang: str | None = 'pt') -> list[Row]: ...
    def templates(self, campaign: str, moment: str) -> list[Row]: ...


def _match(row: Row, **tags: str | None) -> bool:
    # A tag left out matches anything; a fragment with no god or no moment fits every god or moment.
    return all(v is None or row.get(k) in (v, None) for k, v in tags.items())


class MemoryStore:
    def __init__(self) -> None:
        self.frag: list[Row] = []
        self.tmpl: list[Row] = []

    def add_fragments(self, rows: list[Row]) -> int:
        seen = {(r['campaign'], r['kind'], r['text']) for r in self.frag}
        new = [r for r in rows if (r['campaign'], r['kind'], r['text']) not in seen]
        self.frag += new
        return len(new)

    def add_templates(self, rows: list[Row]) -> int:
        seen = {(r['campaign'], r['moment'], r['text']) for r in self.tmpl}
        new = [r for r in rows if (r['campaign'], r['moment'], r['text']) not in seen]
        self.tmpl += new
        return len(new)

    def fragments(self, campaign, kind=None, god=None, moment=None, q=None, lang='pt'):
        out = [r for r in self.frag if r['campaign'] == campaign and _match(r, kind=kind, god=god, moment=moment) and (not lang or r.get('lang', 'pt') == lang)]
        return [r for r in out if not q or q.lower() in r['text'].lower()]

    def templates(self, campaign, moment):
        return [r for r in self.tmpl if r['campaign'] == campaign and r['moment'] == moment]


class SupabaseStore:
    """PostgREST behind Supabase, with the service key (server only)."""

    def __init__(self, url: str, key: str) -> None:
        self.base = url.rstrip('/') + '/rest/v1'
        # New keys (sb_secret_...) go only in apikey; a legacy service_role JWT also goes as the bearer
        self.h = {'apikey': key, **({'authorization': f'Bearer {key}'} if key.startswith('eyJ') else {})}

    def _post(self, table: str, rows: list[Row], conflict: str) -> int:
        if not rows:
            return 0
        r = httpx.post(f'{self.base}/{table}?on_conflict={conflict}', json=rows, timeout=20,
                       headers={**self.h, 'prefer': 'resolution=ignore-duplicates,return=representation'})
        r.raise_for_status()
        return len(r.json())

    def add_fragments(self, rows):
        return self._post('fragment', rows, 'campaign,kind,text')

    def add_templates(self, rows):
        return self._post('template', rows, 'campaign,moment,text')

    def fragments(self, campaign, kind=None, god=None, moment=None, q=None, lang='pt'):
        p: dict[str, str] = {'campaign': f'eq.{campaign}', 'select': 'id,campaign,area,god,moment,kind,text,source,lang', 'limit': '200'}
        if lang:
            p['lang'] = f'eq.{lang}'
        if kind:
            p['kind'] = f'eq.{kind}'
        ors = [f'or=(god.eq.{god},god.is.null)' if god else '', f'or=(moment.eq.{moment},moment.is.null)' if moment else '']
        if q:
            p['search'] = f'wfts(portuguese).{q}'
        url = f'{self.base}/fragment?' + '&'.join([f'{k}={v}' for k, v in p.items()] + [o for o in ors if o])
        r = httpx.get(url, headers=self.h, timeout=10)
        if r.status_code == 400 and lang:   # a database from before the lang column (D7): ask without it
            r = httpx.get(url.replace(f'&lang=eq.{lang}', '').replace(',lang', ''), headers=self.h, timeout=10)
        r.raise_for_status()
        return r.json()

    def templates(self, campaign, moment):
        r = httpx.get(f'{self.base}/template', params={'campaign': f'eq.{campaign}', 'moment': f'eq.{moment}', 'select': 'id,campaign,moment,text'}, headers=self.h, timeout=10)
        r.raise_for_status()
        return r.json()


def from_env() -> Store:
    url, key = os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SECRET_KEY') or os.environ.get('SUPABASE_SERVICE_KEY')
    return SupabaseStore(url, key) if url and key else MemoryStore()
