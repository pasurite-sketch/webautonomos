#!/usr/bin/env node

/**
 * publish-articles.js
 *
 * Automatically adds blog articles to index.html SPA listing
 * based on publish_date in calendrier.json and pre-generated SPA data.
 *
 * Run by GitHub Action every Mon/Thu at 8:00 (Europe/Madrid).
 * Can also be run manually: node scripts/publish-articles.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_PATH = path.join(ROOT, 'index.html');
const CALENDRIER_PATH = path.join(ROOT, 'calendrier.json');
const SPA_DATA_PATH = path.join(ROOT, 'blog-spa-data.json');
const SITEMAP_PATH = path.join(ROOT, 'sitemap.xml');

// Read files
console.log('Reading files...');
let html = fs.readFileSync(INDEX_PATH, 'utf8');
let sitemap = fs.readFileSync(SITEMAP_PATH, 'utf8');
const calendrier = JSON.parse(fs.readFileSync(CALENDRIER_PATH, 'utf8'));
const spaData = JSON.parse(fs.readFileSync(SPA_DATA_PATH, 'utf8'));

// Today's date in YYYY-MM-DD format
const today = new Date().toISOString().split('T')[0];
console.log(`Today: ${today}`);
console.log(`Total articles in calendrier: ${calendrier.articles.length}`);

// Find articles that:
// 1. Have status "published" (HTML exists but not yet in SPA)
// 2. Have publish_date <= today
// 3. Have SPA data available
// 4. Are not already in index.html
const toPublish = calendrier.articles.filter(a => {
    return a.status === 'published'
        && a.publish_date <= today
        && spaData[a.id.toString()]
        && !html.includes(`slug: "es/${a.slug_es}"`);
});

console.log(`Articles to publish today: ${toPublish.length}`);

if (toPublish.length === 0) {
    console.log('No articles to publish. Exiting.');
    process.exit(0);
}

// Display which articles will be published
toPublish.forEach(a => {
    console.log(`  - [${a.id}] ${a.title_es} (${a.publish_date})`);
});

// Find the 3 CTA insertion points (ES, VAL, EN)
// The articles arrays end right before "cta: {" in each language block
const ctaRegex = /\n(\s+)cta:\s*\{/g;
const ctaPositions = [];
let ctaMatch;
while ((ctaMatch = ctaRegex.exec(html)) !== null) {
    ctaPositions.push(ctaMatch.index);
}

if (ctaPositions.length < 3) {
    console.error(`Expected at least 3 CTA markers, found ${ctaPositions.length}. Aborting.`);
    process.exit(1);
}

// Use the last 3 CTA positions (there might be other cta references before)
// But from our analysis, there are exactly 3 at lines 757, 1690, 2623
const langs = ['es', 'val', 'en'];

// Process in REVERSE order to avoid position shifts when inserting
for (let i = 2; i >= 0; i--) {
    const lang = langs[i];
    const ctaPos = ctaPositions[i];

    // Find the closing ] of the articles array (last ] before this cta:)
    const searchArea = html.substring(0, ctaPos);
    const closingBracketPos = searchArea.lastIndexOf(']');

    if (closingBracketPos === -1) {
        console.error(`Could not find articles array closing ] for ${lang}. Aborting.`);
        process.exit(1);
    }

    // Verify we found the right bracket by checking context
    const contextBefore = html.substring(Math.max(0, closingBracketPos - 60), closingBracketPos);
    if (!contextBefore.includes('}')) {
        console.warn(`Warning: Unusual context before ] for ${lang}. Proceeding anyway.`);
    }

    // Generate entries for this language
    const entries = toPublish.map(a => {
        const articleData = spaData[a.id.toString()];
        if (!articleData || !articleData[lang]) {
            console.warn(`No SPA data for article ${a.id} in ${lang}. Skipping.`);
            return null;
        }
        return formatEntry(articleData[lang]);
    }).filter(Boolean);

    if (entries.length > 0) {
        // Find the newline before the closing ] to preserve its indentation
        const lineBreakBefore = html.lastIndexOf('\n', closingBracketPos - 1);
        const indentBefore = html.substring(lineBreakBefore + 1, closingBracketPos);

        const insertion = entries.map(e => ',\n' + e).join('');
        // Insert after the last article's }, keeping ] on its own properly-indented line
        html = html.substring(0, lineBreakBefore) + insertion + '\n' + indentBefore + html.substring(closingBracketPos);
        console.log(`Inserted ${entries.length} entries in ${lang.toUpperCase()} block.`);
    }
}

// Update calendrier.json statuses to "published_spa"
toPublish.forEach(a => {
    const article = calendrier.articles.find(art => art.id === a.id);
    if (article) {
        article.status = 'published_spa';
    }
});

// Update sitemap.xml — add entries for articles not yet listed
const sitemapInsertions = [];
toPublish.forEach(a => {
    const sitemapUrl = `https://webautonomos.es/blog/es/${a.slug_es}`;
    if (!sitemap.includes(sitemapUrl)) {
        sitemapInsertions.push(
            `    <url>\n` +
            `        <loc>${sitemapUrl}</loc>\n` +
            `        <lastmod>${a.publish_date}</lastmod>\n` +
            `        <changefreq>monthly</changefreq>\n` +
            `        <priority>0.7</priority>\n` +
            `    </url>`
        );
    }
});

if (sitemapInsertions.length > 0) {
    // Insert before <!-- Demos --> or before </urlset>
    const demoMarker = '<!-- Demos -->';
    const insertPos = sitemap.indexOf(demoMarker);
    if (insertPos !== -1) {
        sitemap = sitemap.substring(0, insertPos) +
            sitemapInsertions.join('\n\n') + '\n\n    ' +
            sitemap.substring(insertPos);
    } else {
        // Fallback: insert before </urlset>
        sitemap = sitemap.replace('</urlset>', sitemapInsertions.join('\n\n') + '\n\n</urlset>');
    }
    console.log(`Added ${sitemapInsertions.length} new entries to sitemap.xml.`);
} else {
    console.log('All articles already in sitemap.xml.');
}

// Write updated files
fs.writeFileSync(INDEX_PATH, html);
fs.writeFileSync(SITEMAP_PATH, sitemap);
fs.writeFileSync(CALENDRIER_PATH, JSON.stringify(calendrier, null, 2) + '\n');

console.log('');
console.log(`Done! Published ${toPublish.length} articles to index.html SPA.`);
console.log('Updated calendrier.json statuses to published_spa.');

// === Helper Functions ===

function formatEntry(data) {
    const indent = '                        '; // 24 spaces (article object level)
    const propIndent = '                            '; // 28 spaces (property level)
    const contentIndent = '                                '; // 32 spaces (content item level)

    const lines = [];
    lines.push(`${indent}{`);
    lines.push(`${propIndent}id: ${data.id},`);
    lines.push(`${propIndent}slug: ${esc(data.slug)},`);
    lines.push(`${propIndent}title: ${esc(data.title)},`);
    lines.push(`${propIndent}seoTitle: ${esc(data.seoTitle)},`);
    lines.push(`${propIndent}metaDescription: ${esc(data.metaDescription)},`);
    lines.push(`${propIndent}keywords: [${data.keywords.map(k => esc(k)).join(', ')}],`);
    lines.push(`${propIndent}excerpt: ${esc(data.excerpt)},`);
    lines.push(`${propIndent}category: ${esc(data.category)},`);
    lines.push(`${propIndent}date: ${esc(data.date)},`);
    lines.push(`${propIndent}readTime: ${data.readTime},`);
    lines.push(`${propIndent}image: ${esc(data.image)},`);

    // Content array
    lines.push(`${propIndent}content: [`);
    data.content.forEach((c, idx) => {
        const comma = idx < data.content.length - 1 ? ',' : '';
        lines.push(`${contentIndent}{ type: ${esc(c.type)}, text: ${esc(c.text)} }${comma}`);
    });
    lines.push(`${propIndent}],`);

    // FAQ array
    lines.push(`${propIndent}faq: [`);
    data.faq.forEach((f, idx) => {
        const comma = idx < data.faq.length - 1 ? ',' : '';
        lines.push(`${contentIndent}{ q: ${esc(f.q)}, a: ${esc(f.a)} }${comma}`);
    });
    lines.push(`${propIndent}]`);

    lines.push(`${indent}}`);

    return lines.join('\n');
}

/**
 * Escape a string for JavaScript source code embedding.
 * Uses JSON.stringify which handles quotes, newlines, unicode properly.
 */
function esc(str) {
    return JSON.stringify(str);
}
