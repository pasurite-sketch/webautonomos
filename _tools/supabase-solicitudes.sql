-- ============================================================
-- Table  : solicitudes
-- Usage  : leads de la landing /visibilidad-ia (campagne Google Ads)
-- Écrire : rôle anon (INSERT uniquement, depuis le navigateur)
-- Lire   : personne via l'API publique — service_role / SQL editor seulement
-- ============================================================

create table if not exists public.solicitudes (
  id             bigint generated always as identity primary key,
  oficio         text        not null,
  ciudad         text        not null,
  pregunta_tipo  text        not null,
  motores        text[]      not null default '{}',
  nombre         text        not null,
  email          text        not null,
  origen         text        not null default 'LP-ads',
  created_at     timestamptz not null default now(),

  -- Garde-fous : empêchent un bot de remplir la table de vide ou de romans
  constraint solicitudes_oficio_len  check (char_length(oficio)  between 1 and 120),
  constraint solicitudes_ciudad_len  check (char_length(ciudad)  between 1 and 120),
  constraint solicitudes_nombre_len  check (char_length(nombre)  between 1 and 120),
  constraint solicitudes_email_fmt   check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' and char_length(email) <= 200),
  constraint solicitudes_origen_len  check (char_length(origen)  between 1 and 60),
  constraint solicitudes_motores_len check (array_length(motores, 1) is null or array_length(motores, 1) <= 10),
  constraint solicitudes_pregunta_ok check (pregunta_tipo in (
    'recomiendas','mejor','urgente','precio','confianza','top5','a_quien_llamo'
  ))
);

comment on table  public.solicitudes            is 'Leads LP visibilidad IA — insertion publique (anon), lecture réservée au service_role.';
comment on column public.solicitudes.motores    is 'IA à vérifier : chatgpt, gemini, perplexity, claude.';
comment on column public.solicitudes.origen     is 'Source du lead. LP-ads = landing /visibilidad-ia.';

create index if not exists solicitudes_created_at_idx on public.solicitudes (created_at desc);
create index if not exists solicitudes_origen_idx     on public.solicitudes (origen);


-- ============================================================
-- Row Level Security
-- ============================================================

alter table public.solicitudes enable row level security;

-- Nettoyage si tu rejoues le script
drop policy if exists "anon puede insertar solicitudes" on public.solicitudes;

-- INSERT autorisé au rôle anon (la clé publique du navigateur).
-- with check (true) : toute ligne est acceptable, les contraintes CHECK
-- ci-dessus font le filtrage.
create policy "anon puede insertar solicitudes"
  on public.solicitudes
  for insert
  to anon
  with check (true);

-- Aucune policy SELECT / UPDATE / DELETE n'est créée.
-- Avec RLS actif, l'absence de policy = accès refusé. Les rôles anon et
-- authenticated ne peuvent donc rien lire ni modifier. Le service_role
-- contourne RLS (côté serveur uniquement) et l'éditeur SQL du dashboard
-- Supabase reste utilisable pour consulter les leads.

-- Ceinture et bretelles : on retire aussi les droits table au niveau SQL,
-- pour que même une policy ajoutée par erreur plus tard n'ouvre pas la lecture.
revoke all      on public.solicitudes from anon, authenticated;
grant  insert   on public.solicitudes to   anon;


-- ============================================================
-- Vérification (à lancer dans le SQL editor après exécution)
-- ============================================================
-- select policyname, cmd, roles from pg_policies
--   where schemaname = 'public' and tablename = 'solicitudes';
--   -> doit renvoyer exactement 1 ligne : INSERT / {anon}
--
-- select relrowsecurity from pg_class where oid = 'public.solicitudes'::regclass;
--   -> doit renvoyer true
