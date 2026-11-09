"""Lore from fragments: a template of the moment, its gaps filled with fragments of the right kind and god.
No model: it is recombination. The same seed gives the same line."""
from __future__ import annotations
import random
import re
from .store import Store

GAP = re.compile(r'\{(\w+)\}')
# Portuguese contractions a fragment brings when it lands after a preposition ("chegam a o porão" -> "chegam ao porão")
JOIN = [(r'\ba (os?)\b', r'a\1'), (r'\ba a(s?)\b', r'à\1'), (r'\bem (os?|as?|um|uma|uns|umas)\b', r'n\1'), (r'\bde (os?|as?)\b', r'd\1')]


def tidy(text: str) -> str:
    """Contractions, and a capital letter wherever a sentence starts."""
    for pat, rep in JOIN:
        text = re.sub(pat, rep, text)
    return re.sub(r'(^|[.!?]\s+|“)([a-zà-ú])', lambda m: m.group(1) + m.group(2).upper(), text)


def compose(store: Store, campaign: str, moment: str, god: str | None = None, seed: int | None = None, names: dict[str, str] | None = None) -> dict | None:
    rnd = random.Random(seed)
    tmpls = sorted(store.templates(campaign, moment), key=lambda t: t['text'])
    if not tmpls:
        return None
    t = rnd.choice(tmpls)
    used: list[dict] = []

    def fill(m: re.Match) -> str:
        kind = m.group(1)
        if names and kind in names:
            return names[kind]
        pool = sorted(store.fragments(campaign, kind=kind, god=god, moment=moment), key=lambda r: r['text'])
        # prefer what belongs to this god and this moment, then the general ones
        best = [r for r in pool if r.get('god') == god and god] or [r for r in pool if r.get('moment') == moment] or pool
        if not best:
            return m.group(0)
        r = rnd.choice(best)
        used.append(r)
        return r['text']

    text = GAP.sub(fill, t['text'])
    if GAP.search(text):
        return None   # a gap with nothing to fill it: better no line than a broken one
    text = tidy(text)
    return {'text': text, 'moment': moment, 'god': god, 'sources': sorted({r['source'] for r in used})}
