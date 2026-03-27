#!/usr/bin/env python3
"""
fix-hreflang.py — Harmonize hreflang tags across ES/VAL/EN blog articles.
All hreflang point to Spanish slugs (since val/ and en/ files use Spanish filenames).
Also updates sitemap.xml.

Run: cd ~/webautonomos && python3 fix-hreflang.py
"""
import os, re, glob

BASE = "https://webautonomos.es/blog"

# Get all Spanish slugs from blog/es/
es_files = glob.glob("blog/es/*.html")
slugs = sorted([os.path.basename(f).replace(".html", "") for f in es_files])

print(f"Found {len(slugs)} article slugs")

# The correct hreflang block for each slug (all point to Spanish slug names)
def make_hreflang_block(slug, indent="    "):
    return f"""{indent}<link rel="alternate" hreflang="es" href="{BASE}/es/{slug}">
{indent}<link rel="alternate" hreflang="ca-ES" href="{BASE}/val/{slug}">
{indent}<link rel="alternate" hreflang="en" href="{BASE}/en/{slug}">
{indent}<link rel="alternate" hreflang="x-default" href="{BASE}/es/{slug}">"""

def fix_file(filepath):
    """Replace all hreflang links in a file with the correct ones."""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    slug = os.path.basename(filepath).replace(".html", "")
    
    # Remove ALL existing hreflang lines
    content = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*"[^>]*/?\s*>', "", content)
    
    # Find where to insert new hreflang (after canonical)
    canonical_match = re.search(r'(<link rel="canonical"[^>]*>)', content)
    if canonical_match:
        insert_pos = canonical_match.end()
        new_block = "\n\n    <!-- Hreflang -->\n" + make_hreflang_block(slug)
        content = content[:insert_pos] + new_block + content[insert_pos:]
    
    # Also fix canonical to point to the correct lang version
    lang_dir = filepath.split("/blog/")[1].split("/")[0]  # es, val, or en
    content = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{BASE}/{lang_dir}/{slug}">',
        content
    )
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

# Fix all files in es/, val/, en/
fixed = 0
for lang in ["es", "val", "en"]:
    for slug in slugs:
        filepath = f"blog/{lang}/{slug}.html"
        if fix_file(filepath):
            fixed += 1
            print(f"  ✓ {filepath}")
        elif os.path.exists(filepath):
            print(f"  · {filepath} (no change)")
        # skip silently if file doesn't exist

print(f"\n✅ Fixed {fixed} files")

# Update sitemap.xml with correct hreflang URLs
print("\nUpdating sitemap.xml...")
sitemap = open("sitemap.xml", "r", encoding="utf-8").read()

# For each slug that has val/en files, ensure sitemap uses Spanish slugs in hreflang
for slug in slugs:
    # Check if this slug is in the sitemap
    es_url = f"{BASE}/es/{slug}"
    if es_url in sitemap:
        # Replace any translated slug hreflang with Spanish slug versions
        # Find the <url> block for this article and ensure hreflang are correct
        val_correct = f'{BASE}/val/{slug}'
        en_correct = f'{BASE}/en/{slug}'
        
        # Fix val hreflang - replace any val URL for this article with correct one
        sitemap = re.sub(
            rf'hreflang="ca-ES" href="{BASE}/val/[^"]*"',
            f'hreflang="ca-ES" href="{val_correct}"',
            sitemap
        )
        sitemap = re.sub(
            rf'hreflang="en" href="{BASE}/en/[^"]*"',
            f'hreflang="en" href="{en_correct}"',
            sitemap
        )

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

print("✅ sitemap.xml updated")
print("\nDone! Now run:")
print("  git add blog/es/ blog/val/ blog/en/ sitemap.xml")
print('  git commit -m "fix: harmonize hreflang to Spanish slugs across ES/VAL/EN articles"')
print("  git push origin main")
print("  npx wrangler deploy")
