"""lore-enhancer: lore for table games, by tags, without a model."""
from __future__ import annotations
import os
import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field
from .compose import compose
from .parse import fragments as parse_work
from .store import Store, from_env

VERSION = '0.1.0'
app = FastAPI(title='lore-enhancer', version=VERSION)
# The games call /lore straight from the browser: reading is open to any site, writing (/ingest) still needs the login
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['GET'], allow_headers=[])
_store: Store = from_env()


def store() -> Store:
    return _store


def who(authorization: str = Header(default='')) -> str:
    """Only a user of the Supabase project may ingest: asks Supabase who the token belongs to."""
    url, anon = os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_PUBLISHABLE_KEY') or os.environ.get('SUPABASE_ANON_KEY')
    if not authorization.lower().startswith('bearer ') or not url or not anon:
        raise HTTPException(401, 'login do Supabase obrigatório')
    r = httpx.get(url.rstrip('/') + '/auth/v1/user', headers={'apikey': anon, 'authorization': authorization}, timeout=10)
    if r.status_code != 200:
        raise HTTPException(401, 'login inválido')
    return r.json().get('email') or r.json().get('id', '')


class Fragment(BaseModel):
    campaign: str
    area: str
    kind: str
    text: str = Field(min_length=3, max_length=600)
    source: str
    god: str | None = None
    moment: str | None = None
    source_date: str | None = None
    lang: str = 'pt'


class Template(BaseModel):
    campaign: str
    moment: str
    text: str = Field(min_length=3, max_length=600)


class Batch(BaseModel):
    fragments: list[Fragment] = []
    templates: list[Template] = []


@app.exception_handler(404)
async def not_found(request, exc):
    # Says which path reached the app: on Vercel a rewrite or a prefix can change it
    from fastapi.responses import JSONResponse
    return JSONResponse({'detail': getattr(exc, 'detail', 'Not Found'), 'path': request.url.path, 'root_path': request.scope.get('root_path', '')}, status_code=404)


@app.get('/')
def root() -> dict:
    return {'name': 'lore-enhancer', 'version': VERSION, 'see': ['/health', '/lore', '/fragments', '/docs']}


@app.get('/health')
def health(s: Store = Depends(store)) -> dict:
    return {'ok': True, 'version': VERSION, 'store': type(s).__name__}


@app.post('/ingest')
def ingest(b: Batch, s: Store = Depends(store), user: str = Depends(who)) -> dict:
    return {'fragments': s.add_fragments([f.model_dump() for f in b.fragments]), 'templates': s.add_templates([t.model_dump() for t in b.templates]), 'by': user}


class Work(BaseModel):
    url: str = Field(pattern=r'^https://')
    campaign: str
    area: str
    source: str
    lang: str = 'pt'
    source_date: str | None = None
    god: str | None = None
    untagged_max: int = Field(100, ge=0, le=2000)


@app.post('/ingest/url')
def ingest_url(w: Work, s: Store = Depends(store), user: str = Depends(who)) -> dict:
    """A whole work (a Project Gutenberg plain text, say): cut into passages, tagged by keywords, added."""
    r = httpx.get(w.url, timeout=25, follow_redirects=True)
    if r.status_code != 200:
        raise HTTPException(502, f'a fonte respondeu {r.status_code}')
    rows = parse_work(r.text, campaign=w.campaign, area=w.area, source=w.source, lang=w.lang, source_date=w.source_date, god=w.god, untagged_max=w.untagged_max)
    added = sum(s.add_fragments(rows[i:i + 500]) for i in range(0, len(rows), 500))
    return {'passages': len(rows), 'added': added, 'by': user}


@app.get('/lore')
def lore(campaign: str, moment: str, god: str | None = None, seed: int | None = None,
         pres: str | None = Query(None), chanc: str | None = Query(None), target: str | None = Query(None), s: Store = Depends(store)) -> dict:
    names = {k: v for k, v in {'pres': pres, 'chanc': chanc, 'target': target}.items() if v}
    out = compose(s, campaign, moment, god, seed, names)
    if not out:
        raise HTTPException(404, 'sem lore para esse momento')
    return out


@app.get('/fragments')
def fragments(campaign: str, kind: str | None = None, god: str | None = None, moment: str | None = None, q: str | None = None, lang: str = 'pt', s: Store = Depends(store)) -> list[dict]:
    return s.fragments(campaign, kind, god, moment, q, lang)
