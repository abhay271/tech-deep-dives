# Daily Tech Deep-Dive: standing instructions

This repo is one self-contained `index.html` (served by GitHub Pages from `main`). Each scheduled run adds ONE new deep-dive entry at the top. Everything you need is in this file.

## Content spec

- Each run, pick ONE popular app or system used by millions (Netflix, Discord, Google Maps, Uber, Spotify, WhatsApp, Instagram, Cloudflare, Postgres, etc.) and explain how it actually works under the hood.
- **Audience and purpose:** an entry-level software engineer (a student who hasn't graduated yet) who reads this to stay curious and gain breadth of knowledge and exposure across many systems, not deep expertise in any one. Assume the reader has NOT heard of the specific tech in the entry. Stay technical enough that they learn how the thing genuinely works (the real architecture, the real trade-off), but explain it the way you would to a smart friend: the "what" and "why" matter more than exact numbers, protocol details or code-level specifics. Never write a textbook chapter.
- **Tone and legend (important):** Write like a smart friend explaining over coffee, not a paper. New terms and tech words are welcome, but every entry MUST include a **Legend** (see components) that briefly explains each new or non-obvious term in one or two plain sentences, and the first use of each term in the prose is wrapped in `<dfn class="term" title="short definition">`. **Simple language first:** short sentences, everyday words, one idea per paragraph. Lead with an analogy or a concrete everyday situation, then name the real technical thing. If a term can be replaced by a plain word without losing meaning, use the plain word; if it's a real term worth learning, keep it and put it in the legend. Prefer one vivid analogy over three technical details. Use at most 2-3 numbers in the whole entry, only ones that make a point, and explain what each means. Don't explain internals (library names, data structures, protocol fields) unless the reader needs them to follow the story; name-drop at most one or two specifics per section. If a paragraph needs re-reading, simplify it. Aim for 3-5 minutes of reading. Diagrams should stay as clear as the existing ones: few boxes, plain labels. Legend has 4-10 entries, ordered by first appearance.
- **Rotate domains** between runs: consumer apps, infra, databases, OS/runtime internals, dev tools, odd protocol choices. Never two similar topics back to back. Before choosing, read all existing `<article>` elements and their `data-topic` / `data-domain` attributes (`grep -o 'data-topic="[^"]*" data-domain="[^"]*"' index.html`). Never repeat a topic, and pick a domain different from the last two entries.
- **Shape:** start with the core functionality and the design challenge it creates, then roughly: (1) **The design**, the one or two architectural choices that make it work; (2) **Why**, the real constraint or trade-off that forced it, with as much room as it deserves; (3) **Things this explains**, 2-3 behaviors people experience constantly but never questioned, now obvious given the design. A guide, not a checklist; length follows what's genuinely interesting. No headers for the sake of headers.
- **Accuracy:** verify technical claims against reliable current sources (web search/fetch) when unsure. Prefer primary sources (the company's engineering blog, the RFC, the paper, the source code). If not confident about a detail, say so in the text using the confidence-note component instead of asserting it. Never invent numbers.
- **Diagrams:** 1-3 per entry, only where they genuinely clarify (data flow, architecture, sequence, state machine). No decorative diagrams.

## Append rules

- Insert each new entry as one self-contained
  `<article class="entry" id="YYYY-MM-DD-slug" data-topic="..." data-domain="..." data-date="YYYY-MM-DD">`
  directly below the `<!-- ENTRIES -->` marker (newest first). Never modify or reorder older entries.
- Also add the entry to the archive list in the sidebar, directly below the `<!-- TOC -->` marker, as
  `<li><a href="#ID"><time datetime="YYYY-MM-DD">YYYY-MM-DD</time><span>Short title</span></a></li>`.
- All CSS and JS live once in `index.html`; entries add markup only, reusing existing classes/components. If a needed component doesn't exist, add it to the shared CSS carefully without changing existing styles.
- Diagrams are hand-written inline SVG using the shared diagram classes. No Mermaid, no image files, no external JS or CDN dependencies. Fonts may use Google Fonts with system fallbacks (already set up).
- Use the newest entry as your template: copy its markup structure (header, `.prose`, sections, callouts, figure/diagram markup).
- **Validate before committing:** run `python scripts/validate.py`. It checks well-formed HTML, that every SVG parses and has a title/desc, no duplicate ids, and (via `git diff`) that no existing line was modified or removed. Fix everything it reports. Also make sure every SVG id you use is prefixed with the entry slug.
- **Commit message:** `Add deep-dive: <topic> (<domain>)`, then a blank line and these two trailer lines at the very end, exactly (the repo owner is credited as co-author; keep any other trailers your environment adds):
  `Co-Authored-By: abhay271 <153154236+abhay271@users.noreply.github.com>`
  `Co-Authored-By: Claude <noreply@anthropic.com>`
  Push to `main` (`git push origin HEAD:main`). Do not open a PR. The trailers are only metadata; never let them block or delay the commit and push.

## Component reference (entry markup)

```html
<article class="entry" id="2026-09-30-example" data-topic="Example" data-domain="Consumer apps" data-date="2026-09-30">
  <header class="entry-head">
    <div class="entry-meta">
      <span class="chip">Consumer apps</span>
      <time datetime="2026-09-30">30 Sep 2026</time>
      <span class="read"><span class="read-time">6</span> min read</span>
    </div>
    <h2 class="entry-title">Title</h2>
    <p class="lede">Core functionality and the design challenge it creates.</p>
  </header>
  <div class="prose">
    <details class="legend" open>
      <summary>Legend: terms used below</summary>
      <dl>
        <div><dt>Term</dt><dd>One or two plain sentences, no further jargon.</dd></div>
        <div><dt>Another term</dt><dd>…</dd></div>
      </dl>
    </details>
    <section class="reveal"><h3>The design</h3><p>… <code>inline code</code> …</p></section>
    <figure class="diagram-fig"> … see below … </figure>
    <aside class="callout why reveal"><span class="callout-label">Why</span><p>…</p></aside>
    <blockquote class="pullquote reveal">…</blockquote>
    <aside class="confidence reveal"><span class="callout-label">Confidence note</span><p>…</p></aside>
    <section class="reveal"><h3>Things this explains</h3>
      <ol class="explains stagger"><li><strong>Behavior.</strong> Why.</li>…</ol></section>
  </div>
</article>
```

Diagram figure: `<figure class="diagram-fig"><div class="diagram-scroll" tabindex="0" role="group" aria-label="Diagram, scrollable"><svg class="diagram" viewBox="0 0 760 300" role="img" aria-labelledby="SLUG-d1-t SLUG-d1-d"><title id="SLUG-d1-t">…</title><desc id="SLUG-d1-d">…</desc> … </svg></div><figcaption>…</figcaption><button class="replay" type="button">↻ Replay</button></figure>`

SVG parts (all styled by shared CSS; set `style="--i:N"` for sequence order, N = 0,1,2…):
- Node: `<g class="d-node [accent|alt]" style="--i:0"><rect x y width height rx="10"/><text class="d-text" x y text-anchor="middle">Name</text><text class="d-sub" …>sub</text></g>`
- Edge: `<path class="d-edge [accent]" style="--i:1" d="…"/>` plus arrowhead `<path class="d-arrow" style="--i:1" d="M x1 y1 L x2 y2 L x3 y3 Z"/>`. Never use dashed edges (the draw-in animation uses dasharray).
- Label: `<text class="d-label" style="--i:2" …>`
- Packet (travels along a path; time is driven by the SVG timeline, so use static `begin` offsets):
  `<circle class="d-packet" r="5" opacity="0"><animateMotion dur="5s" begin="1s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.7;1" calcMode="linear" path="M…"/><animate attributeName="opacity" dur="5s" begin="1s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.03;.68;.7;1"/></circle>`
  (add class `alt` for a second packet colour). Keep all packets on the same `dur`.
- Keep text ≥ 12px in user units; the diagram scrolls horizontally on very narrow screens (min-width set in CSS).

## Run checklist

1. Read existing entries' topics/domains → choose topic + domain.
2. Research with web search/fetch; note sources you rely on; decide what to hedge.
3. Write the entry (with Legend) + TOC line. 4. `python scripts/validate.py`. 5. Commit, push to `main`.
