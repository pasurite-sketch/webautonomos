# -*- coding: utf-8 -*-
"""Publie le prochain article dû depuis _tools/queue/.

Lancé par le GitHub Action (lundi/jeudi). Logique :
  - lit tous les _tools/queue/*.json ;
  - garde ceux dont publish_date <= aujourd'hui, non encore publiés ;
  - publie le PLUS ANCIEN (un seul par exécution → cadence 2/semaine tenue même si un run saute) ;
  - réutilise add_article.py (déjà testé) pour l'insertion + le sitemap ;
  - déplace le JSON publié dans _tools/queue/published/.
Test local : PUBLISH_DATE_OVERRIDE=2026-07-23 python3 _tools/publish_next.py
"""
import os, sys, glob, json, subprocess, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, 'queue')
PUBLISHED = os.path.join(QUEUE, 'published')
ADD = os.path.join(HERE, 'add_article.py')

today = datetime.date.fromisoformat(os.environ.get('PUBLISH_DATE_OVERRIDE') or datetime.date.today().isoformat())

def gh_output(key, value):
    p = os.environ.get('GITHUB_OUTPUT')
    if p:
        with open(p, 'a', encoding='utf-8') as f:
            f.write(f'{key}={value}\n')

# 1) collecter les articles dus
due = []
for f in sorted(glob.glob(os.path.join(QUEUE, '*.json'))):
    try:
        pd = json.load(open(f, encoding='utf-8')).get('publish_date')
        if pd and datetime.date.fromisoformat(pd) <= today:
            due.append((pd, f))
    except Exception as e:
        print(f'  (ignoré {os.path.basename(f)}: {e})')

if not due:
    print(f'Aucun article à publier aujourd\'hui ({today}). File vide ou dates futures.')
    gh_output('published', 'false')
    sys.exit(0)

due.sort()  # plus ancienne date d'abord
pub_date, path = due[0]
name = os.path.basename(path)
print(f'Article dû : {name} (publish_date {pub_date}). Insertion via add_article.py…')

# 2) insertion (add_article.py tourne depuis la racine du repo)
repo_root = os.path.dirname(HERE)
r = subprocess.run([sys.executable, ADD, path], cwd=repo_root, capture_output=True, text=True)
sys.stdout.write(r.stdout)
if r.stderr:
    sys.stderr.write(r.stderr)
if r.returncode != 0:
    print('ÉCHEC de add_article.py — aucune modification, rien déplacé.')
    gh_output('published', 'false')
    sys.exit(1)

# 3) déplacer le JSON publié
os.makedirs(PUBLISHED, exist_ok=True)
slug = json.load(open(path, encoding='utf-8')).get('slug', name)
shutil.move(path, os.path.join(PUBLISHED, name))

gh_output('published', 'true')
gh_output('slug', slug)
print(f'\n✅ Publié : {slug}  (déplacé vers _tools/queue/published/{name})')
