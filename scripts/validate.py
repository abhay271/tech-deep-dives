#!/usr/bin/env python3
"""Validate index.html before committing a new deep-dive entry.

Checks: balanced/well-formed HTML, every <svg> parses as XML and has title+desc,
unique ids, required article attributes, TOC <-> article consistency, and that no
existing line of index.html was modified or removed (git diff vs HEAD).
Exit code 0 = OK, 1 = problems found.
"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "index.html"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
errors = []


def err(msg):
    errors.append(msg)


html = PATH.read_text(encoding="utf-8")


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids = [], []
        self.in_svg = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            err(f"unexpected </{tag}> at line {self.getpos()[0]}")
            return
        top, pos = self.stack[-1]
        if top != tag:
            err(f"</{tag}> at line {self.getpos()[0]} does not match <{top}> opened at line {pos[0]}")
            # try to recover
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break
        else:
            self.stack.pop()


p = P()
p.feed(html)
for tag, pos in p.stack:
    err(f"<{tag}> opened at line {pos[0]} never closed")

# duplicate ids
seen = set()
for i in p.ids:
    if i in seen:
        err(f"duplicate id: {i}")
    seen.add(i)

# svgs
svgs = [s for s in re.findall(r"<svg\b.*?</svg>", html, flags=re.S) if 'class="diagram"' in s[:200]]
if not svgs:
    err("no SVG found")
for n, s in enumerate(svgs, 1):
    try:
        root = ET.fromstring(s.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1) if "xmlns" not in s[:200] else s)
    except ET.ParseError as e:
        err(f"svg #{n} is not well-formed XML: {e}")
        continue
    ns = "{http://www.w3.org/2000/svg}"
    if root.find(f"{ns}title") is None or root.find(f"{ns}desc") is None:
        err(f"svg #{n} missing <title> or <desc>")
    if root.get("role") != "img" or not root.get("aria-labelledby"):
        err(f"svg #{n} needs role=\"img\" and aria-labelledby")
    if not root.get("viewBox"):
        err(f"svg #{n} missing viewBox")
    for el in root.iter():
        if el.tag.endswith("path") and "d-edge" in (el.get("class") or "") and not el.get("d"):
            err(f"svg #{n} edge without d")

# articles
arts = re.findall(r"<article class=\"entry\"([^>]*)>", html)
toc = re.findall(r'<li><a href="#([^"]+)">', html)
art_ids = []
for a in arts:
    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', a))
    for k in ("id", "data-topic", "data-domain", "data-date"):
        if not attrs.get(k):
            err(f"article missing {k}: {a[:80]}")
    art_ids.append(attrs.get("id"))
    if attrs.get("id") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+", attrs["id"]):
        err(f"bad article id format: {attrs['id']}")
# entries from 2026-10-01 on must include a Legend
for m in re.finditer(r'<article class="entry" id="(\d{4}-\d{2}-\d{2})-[^"]*".*?</article>', html, flags=re.S):
    if m.group(1) >= "2026-10-01" and 'class="legend"' not in m.group(0):
        err(f"entry {m.group(1)} is missing a Legend (<details class=\"legend\">)")
if art_ids != sorted(art_ids, key=lambda x: x[:10], reverse=True):
    err("articles are not newest-first")
if set(toc) != set(art_ids):
    err(f"TOC/article mismatch: toc-only={set(toc) - set(art_ids)} article-only={set(art_ids) - set(toc)}")
if html.count("<!-- ENTRIES -->") != 1 or html.count("<!-- TOC -->") != 1:
    err("markers <!-- ENTRIES --> and <!-- TOC --> must each appear exactly once")
if re.search(r"<script[^>]+src=", html) or re.search(r"cdn\.|mermaid", html, re.I):
    err("external scripts / CDN / mermaid are not allowed")
if re.search(r"<img\b", html):
    err("image files are not allowed; use inline SVG")

# older content unchanged
try:
    out = subprocess.run(["git", "diff", "HEAD", "--unified=0", "--", "index.html"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    removed = [l for l in out.splitlines() if l.startswith("-") and not l.startswith("---")]
    if removed:
        err(f"{len(removed)} existing line(s) modified/removed (only additions allowed). First: {removed[0][:100]}")
except Exception as e:  # not a repo yet, etc.
    print(f"note: git diff check skipped ({e})")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK: {len(arts)} article(s), {len(svgs)} svg(s), {len(p.ids)} ids, all checks passed")
