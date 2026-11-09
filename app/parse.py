"""Whole works into tagged passages: strip the Project Gutenberg wrapper, cut into sentences of a readable size, and tag
each one by keywords (which god, which moment). No model: a passage with no keyword keeps no god and no moment."""
from __future__ import annotations
import random
import re
import unicodedata

MIN, MAX = 60, 280


def fold(s: str) -> str:
    """Lower case without accents, for keyword matching."""
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


GOD_WORDS = {
    'cthulhu': ['cthulhu', "r'lyeh", 'rlyeh'], 'dagon': ['dagon', 'dagom', 'innsmouth', "y'ha-nthlei", 'deep ones'],
    'yog': ['yog-sothoth', 'dunwich', 'whateley'], 'nyarlathotep': ['nyarlathotep'], 'hastur': ['hastur', 'carcosa', 'yellow sign', 'king in yellow'],
    'shub': ['shub-niggurath', 'black goat'], 'azathoth': ['azathoth'], 'tsathoggua': ['tsathoggua'], 'ithaqua': ['ithaqua', 'wendigo'],
    'cthugha': ['cthugha', 'fomalhaut'], 'hydra': ['mother hydra'], 'glaaki': ['glaaki'],
    'baal': ['baal'], 'mamon': ['mamom', 'mammon', 'riquezas', 'riches', 'avareza'], 'moloque': ['moloque', 'moloch', 'molech', 'molec'],
    'tiamat': ['leviathan', 'leviatha', 'leviata', 'dragao', 'dragon', 'serpente', 'abysmo', 'abismo'], 'pazuzu': ['gafanhoto', 'locust', 'pestilencia', 'pestilence', 'peste'],
    'ereshkigal': ['sepulchro', 'sepulcro', 'sepulchre', 'sepultura', 'sheol'], 'marduque': ['babylon', 'babel', 'nabucodonosor', 'nebuchadnezzar', 'chaldeu', 'caldeu'],
    'asmodeu': ['asmodeu', 'asmodeus', 'luxuria', 'lust'], 'astarote': ['astaroth', 'astarote', 'astoreth', 'asherah', 'adivinho', 'feiticeir', 'sorcer', 'witch'],
}
MOMENT_WORDS = {
    'investigacao': ['trair', 'traidor', 'traicao', 'betray', 'traitor', 'judas', 'falso', 'mentir', 'mentira', 'false', 'deceit', 'engan'],
    'eliminacao': ['matou', 'mataram', 'morreu', 'morte', 'slain', 'killed', 'death', 'espada', 'sword', 'sangue', 'blood'],
    'ato3': ['inferno', 'hell', 'trevas', 'darkness', 'abominac', 'abomination', 'maldito', 'cursed', 'demonio', 'devil', 'diabo'],
}


def strip_gutenberg(text: str) -> str:
    """The text between the *** START and *** END lines of a Project Gutenberg file (or all of it)."""
    m = re.search(r'\*\*\*\s*START OF[^\n]*\*\*\*(.*?)\*\*\*\s*END OF', text, re.S)
    return m.group(1) if m else text


def passages(text: str) -> list[str]:
    """Sentences of MIN to MAX characters; the lines of a paragraph are joined first."""
    out: list[str] = []
    for para in re.split(r'\n\s*\n', strip_gutenberg(text)):
        para = re.sub(r'\s+', ' ', para).strip()
        para = re.sub(r'\b\d+[:.]\d+\s*', '', para)   # verse numbers
        if not para or 'gutenberg' in para.lower():
            continue
        for s in re.split(r'(?<=[.!?;])\s+(?=[A-ZÀ-Ú“"])', para):
            s = re.sub(r'\[\d+\]', '', s).strip(' "“”')
            letters = sum(c.isalpha() for c in s)
            if MIN <= len(s) <= MAX and letters > len(s) * 0.6 and not s.isupper():
                out.append(s)
    return out


def tag(passage: str) -> tuple[str | None, str | None]:
    f = fold(passage)
    god = next((g for g, ws in GOD_WORDS.items() if any(w in f for w in ws)), None)
    moment = next((m for m, ws in MOMENT_WORDS.items() if any(w in f for w in ws)), None)
    return god, moment


def fragments(text: str, *, campaign: str, area: str, source: str, lang: str, source_date: str | None = None, god: str | None = None,
              untagged_max: int = 100, seed: int = 0) -> list[dict]:
    """Every tagged passage, and at most untagged_max of the rest (picked at random, the same each time)."""
    tagged, plain = [], []
    for p in dict.fromkeys(passages(text)):
        g, m = tag(p)
        row = {'campaign': campaign, 'area': area, 'kind': 'trecho', 'text': p, 'source': source, 'source_date': source_date,
               'lang': lang, 'god': g or god, 'moment': m}
        (tagged if (g or m) else plain).append(row)
    random.Random(seed).shuffle(plain)
    return tagged + plain[:untagged_max]
