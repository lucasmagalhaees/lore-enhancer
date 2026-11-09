-- lore-enhancer: run once in the Supabase SQL Editor (project lore-enhancer).
-- Fragments of lore tagged by campaign, area, god, moment and kind; templates with gaps; full-text search in Portuguese.
-- The embedding column exists from the start, empty: the vector search comes later, if tag search is not enough (D2).
create extension if not exists vector;

create table if not exists fragment (
  id bigint generated always as identity primary key,
  campaign text not null,
  area text not null,
  god text,
  moment text,
  kind text not null,
  text text not null,
  source text not null,
  source_date date,
  search tsvector generated always as (to_tsvector('portuguese', text)) stored,
  embedding vector(384),
  created_at timestamptz not null default now(),
  unique (campaign, kind, text)
);
create index if not exists fragment_tags on fragment (campaign, kind, god, moment);
create index if not exists fragment_search on fragment using gin (search);

create table if not exists template (
  id bigint generated always as identity primary key,
  campaign text not null,
  moment text not null,
  text text not null,
  unique (campaign, moment, text)
);

-- Only the API (service role) reads and writes; nothing is open to the anon key.
alter table fragment enable row level security;
alter table template enable row level security;
