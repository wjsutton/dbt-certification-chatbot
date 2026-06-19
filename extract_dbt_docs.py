#!/usr/bin/env python3
"""
extract_dbt_docs.py
===================
Download the dbt documentation / guide / blog pages referenced by the dbt
Analytics Engineering certification mapping and save each one as a clean
markdown file (one file per page) into a `raw/` directory.

This `raw/` directory is the *immutable source layer* for the Karpathy
"LLM Wiki" pattern (see build_llm_wiki.py).

How it works
------------
docs.getdbt.com is a Docusaurus site. Appending `.md` to any
docs / reference / best-practices / guides URL returns the page already
stripped of header, nav, sidebar and footer. We use that endpoint and then
do light cleanup of leftover MDX/JSX (`<Term/>`, `<File>`, admonitions, etc.).

The `.md` trick returns empty for /blog/ pages and does not exist on the
www.getdbt.com marketing site, so those are extracted from HTML instead
(grab the article body, drop bios / comments / related-post / footer chrome).

Usage
-----
    pip install requests beautifulsoup4 markdownify
    python extract_dbt_docs.py                 # -> ./raw
    python extract_dbt_docs.py --out ./raw     # custom output dir
    python extract_dbt_docs.py --limit 3       # quick test on first 3 URLs
    python extract_dbt_docs.py --only sample-flag defer   # urls matching substrings
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.exit("Missing dependency. Run: pip install requests beautifulsoup4 markdownify")

DOCS_HOST = "https://docs.getdbt.com"
USER_AGENT = "dbt-cert-wiki-extractor/1.0 (+local knowledge base build)"

# ---------------------------------------------------------------------------
# Source URLs (deduped, from the certification content-mapping spreadsheet)
# ---------------------------------------------------------------------------
URLS: list[str] = [
    # --- 01 Developing & optimizing dbt models ---
    "https://docs.getdbt.com/docs/build/sources",
    "https://docs.getdbt.com/reference/source-configs",
    "https://docs.getdbt.com/docs/deploy/source-freshness",
    "https://docs.getdbt.com/docs/build/materializations",
    "https://docs.getdbt.com/best-practices/materializations/1-guide-overview",
    "https://docs.getdbt.com/best-practices/materializations/5-best-practices",
    "https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview",
    "https://docs.getdbt.com/guides/refactoring-legacy-sql",
    "https://docs.getdbt.com/community/resources/viewpoint",
    "https://docs.getdbt.com/reference/commands/build",
    "https://docs.getdbt.com/reference/commands/run",
    "https://docs.getdbt.com/reference/commands/test",
    "https://docs.getdbt.com/reference/commands/cmd-docs",
    "https://docs.getdbt.com/reference/dbt-commands",
    "https://docs.getdbt.com/reference/commands/snapshot",
    "https://docs.getdbt.com/reference/commands/seed",
    "https://docs.getdbt.com/reference/node-selection/syntax",
    "https://docs.getdbt.com/reference/dbt_project.yml",
    "https://docs.getdbt.com/docs/build/packages",
    "https://docs.getdbt.com/docs/build/python-models",
    "https://docs.getdbt.com/reference/resource-configs/grants",
    "https://docs.getdbt.com/docs/build/snapshots",
    "https://docs.getdbt.com/docs/build/incremental-strategy",
    "https://docs.getdbt.com/docs/build/incremental-models-overview",
    "https://docs.getdbt.com/docs/build/empty-flag",
    "https://docs.getdbt.com/docs/build/sample-flag",
    "https://docs.getdbt.com/docs/build/incremental-microbatch",
    # --- 02 Governance ---
    "https://docs.getdbt.com/docs/mesh/govern/model-contracts",
    "https://docs.getdbt.com/reference/resource-configs/contract",
    "https://docs.getdbt.com/docs/mesh/govern/model-versions",
    "https://docs.getdbt.com/reference/resource-properties/versions",
    "https://docs.getdbt.com/reference/resource-properties/constraints",
    "https://docs.getdbt.com/docs/mesh/govern/about-model-governance",
    # --- 03 Debugging ---
    "https://docs.getdbt.com/guides/debug-errors",
    "https://docs.getdbt.com/reference/commands/compile",
    "https://docs.getdbt.com/best-practices/best-practice-workflows",
    "https://docs.getdbt.com/reference/global-configs/about-global-configs",
    "https://docs.getdbt.com/reference/global-configs/behavior-changes",
    # --- 04 Troubleshooting & optimizing pipelines ---
    "https://docs.getdbt.com/reference/commands/retry",
    "https://docs.getdbt.com/reference/commands/clone",
    "https://docs.getdbt.com/best-practices/clone-incremental-models",
    # --- 05 Implementing dbt tests ---
    "https://docs.getdbt.com/docs/build/data-tests",
    "https://docs.getdbt.com/docs/build/unit-tests",
    "https://docs.getdbt.com/best-practices/writing-custom-generic-tests",
    "https://docs.getdbt.com/reference/data-test-configs",
    # --- 06 External dependencies ---
    "https://docs.getdbt.com/docs/build/exposures",
    "https://docs.getdbt.com/reference/exposure-properties",
    "https://docs.getdbt.com/reference/commands/source",
    "https://docs.getdbt.com/reference/resource-properties/freshness",
    # --- 07 Leveraging the dbt state ---
    "https://docs.getdbt.com/reference/node-selection/state-selection",
    "https://docs.getdbt.com/reference/node-selection/methods",
    "https://docs.getdbt.com/reference/node-selection/defer",
    # --- Blog readings (docs.getdbt.com/blog -> HTML extraction) ---
    "https://docs.getdbt.com/blog/to-defer-or-to-clone",
    "https://docs.getdbt.com/blog/test-smarter-not-harder",
    "https://docs.getdbt.com/blog/test-smarter-where-tests-should-go",
    "https://docs.getdbt.com/blog/essential-dbt-project-checklist",
    # --- Marketing-site reading (www.getdbt.com -> HTML extraction) ---
    "https://www.getdbt.com/blog/data-product-management",
]


# ---------------------------------------------------------------------------
# Classification & filenames
# ---------------------------------------------------------------------------
def is_docs_md_page(url: str) -> bool:
    """True if the page is served cleanly via the `.md` endpoint."""
    p = urlparse(url)
    return p.netloc == "docs.getdbt.com" and not p.path.startswith("/blog")


def slug_for(url: str) -> str:
    """Stable, collision-free filename derived from the URL path."""
    p = urlparse(url)
    host = "getdbt" if p.netloc == "www.getdbt.com" else "docs"
    path = p.path.strip("/").replace("/", "__")
    path = re.sub(r"[^A-Za-z0-9_.-]", "-", path) or "index"
    return f"{host}__{path}.md"


# ---------------------------------------------------------------------------
# Markdown cleanup for the `.md` endpoint
# ---------------------------------------------------------------------------
def _humanize(term_id: str) -> str:
    return term_id.replace("-", " ").replace("_", " ")


def clean_docusaurus_md(text: str, base: str = DOCS_HOST) -> tuple[str, str]:
    """Clean the raw markdown returned by the `.md` endpoint.

    Returns (title, cleaned_body).
    """
    # Strip YAML frontmatter if present (raw GitHub source has it; .md endpoint
    # usually doesn't, but handle both).
    if text.startswith("---"):
        m = re.match(r"^---\n.*?\n---\n", text, flags=re.DOTALL)
        if m:
            text = text[m.end():]

    lines = text.splitlines()

    # Drop MDX import/export statements.
    lines = [ln for ln in lines if not re.match(r"^\s*(import|export)\s", ln)]
    text = "\n".join(lines)

    # Convert admonition fences (:::note / :::info Title ... :::) to blockquotes.
    text = _convert_admonitions(text)

    # <Term id="x">Label</Term>  ->  Label   ;   <Term id="x" />  ->  x
    text = re.sub(r'<Term\s+id="[^"]*"\s*>(.*?)</Term>', r"\1", text, flags=re.DOTALL)
    text = re.sub(r'<Term\s+id="([^"]*)"\s*/>', lambda m: _humanize(m.group(1)), text)
    # <Constant name="x" />  ->  x
    text = re.sub(r'<Constant\s+name="([^"]*)"\s*/>', lambda m: m.group(1), text)

    # Drop media / non-text self-closing components entirely.
    text = re.sub(
        r"<(Lightbox|WistiaVideo|YoutubeVideo|LoomVideo|Lightbox|Image|"
        r"detailsToggle|VersionBlock)\b[^>]*/>",
        "",
        text,
    )
    # Any remaining self-closing JSX component -> drop.
    text = re.sub(r"<[A-Z][A-Za-z0-9]*\b[^>]*/>", "", text)

    # Strip wrapper tags but keep their inner content (<File>, <div>, <Tabs>...).
    text = re.sub(r"</?(File|div|Tabs|TabItem|Snippet|Expandable|"
                  r"FAQ|CommunitySpotlightList)\b[^>]*>", "", text)

    # Absolutize root-relative markdown links: ](/docs/..) -> ](https://docs..)
    text = re.sub(r"\]\((/[^)]*)\)", lambda m: f"]({base}{m.group(1)})", text)

    # Remove the duplicated leading title (frontmatter title rendered as H1,
    # then the real H1).  Capture the page title while we're here.
    title, text = _dedupe_leading_title(text)

    # Collapse 3+ blank lines down to 2.
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return title, text


def _convert_admonitions(text: str) -> str:
    out, in_block, label = [], False, ""
    for ln in text.splitlines():
        open_m = re.match(r"^:::(\w+)\s*(.*)$", ln)
        if open_m and not in_block:
            in_block = True
            kind, rest = open_m.group(1), open_m.group(2).strip()
            label = rest if rest else kind.capitalize()
            out.append(f"> **{label}**")
            out.append(">")
            continue
        if re.match(r"^:::\s*$", ln) and in_block:
            in_block = False
            out.append("")
            continue
        out.append(("> " + ln) if in_block else ln)
    return "\n".join(out)


def _dedupe_leading_title(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    # find first H1
    first_idx = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if first_idx is None:
        return "", text
    title = lines[first_idx][2:].strip()
    # look ahead for a second H1 before any substantive content
    j = first_idx + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j < len(lines) and lines[j].startswith("# "):
        title = lines[j][2:].strip()           # the real title is the 2nd one
        del lines[first_idx:j]                  # drop the duplicate + blanks
    return title, "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML extraction for blog / marketing pages
# ---------------------------------------------------------------------------
def clean_html_to_md(html: str, url: str) -> tuple[str, str]:
    from bs4 import BeautifulSoup
    from markdownify import markdownify as to_md

    soup = BeautifulSoup(html, "html.parser")

    # Remove obvious chrome.
    for tag in soup(["nav", "header", "footer", "aside", "script", "style", "form"]):
        tag.decompose()
    junk = re.compile(
        r"(footer|navbar|sidebar|breadcrumb|pagination|comment|tableofcontents|"
        r"toc|author|tags|cookie|banner|newsletter|subscribe|related|share|"
        r"announcement)",
        re.I,
    )
    for tag in soup.find_all(attrs={"class": junk}):
        tag.decompose()
    for tag in soup.find_all(attrs={"id": junk}):
        tag.decompose()

    # Pick the main content container, most specific first.
    node = (
        soup.select_one("div.markdown")
        or soup.select_one("article")
        or soup.select_one("main")
        or soup.body
        or soup
    )

    title = ""
    h1 = node.find(["h1"]) if node else None
    if h1:
        title = h1.get_text(strip=True)

    body = to_md(str(node), heading_style="ATX", strip=["nav", "footer"])
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return title, body


# ---------------------------------------------------------------------------
# Fetch + write
# ---------------------------------------------------------------------------
def fetch(session: requests.Session, url: str, retries: int = 3) -> str:
    last = None
    for attempt in range(1, retries + 1):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            return r.text
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"failed after {retries} attempts: {last}")


def frontmatter(title: str, url: str, method: str) -> str:
    today = dt.date.today().isoformat()
    safe_title = title.replace('"', "'")
    return (
        "---\n"
        f'title: "{safe_title}"\n'
        f"source_url: {url}\n"
        f"retrieved_via: {method}\n"
        f"fetched: {today}\n"
        "---\n\n"
    )


def process(session: requests.Session, url: str, out_dir: Path) -> dict:
    if is_docs_md_page(url):
        raw = fetch(session, url + ".md")
        if not raw.strip():
            raise RuntimeError(".md endpoint returned empty")
        title, body = clean_docusaurus_md(raw)
        method = "md-endpoint"
    else:
        html = fetch(session, url)
        title, body = clean_html_to_md(html, url)
        method = "html-extract"

    fname = slug_for(url)
    (out_dir / fname).write_text(frontmatter(title or fname, url, method) + body,
                                 encoding="utf-8")
    return {"url": url, "file": fname, "title": title, "method": method,
            "chars": len(body)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="raw", help="output directory (default: ./raw)")
    ap.add_argument("--limit", type=int, default=0, help="only first N URLs")
    ap.add_argument("--only", nargs="*", default=[],
                    help="only URLs containing any of these substrings")
    ap.add_argument("--sleep", type=float, default=0.8,
                    help="seconds to wait between requests")
    args = ap.parse_args()

    urls = URLS
    if args.only:
        urls = [u for u in urls if any(s in u for s in args.only)]
    if args.limit:
        urls = urls[: args.limit]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    results, failures = [], []
    for i, url in enumerate(urls, 1):
        try:
            info = process(session, url, out_dir)
            results.append(info)
            print(f"[{i:>2}/{len(urls)}] ok   {info['file']:<48} "
                  f"({info['method']}, {info['chars']:,} chars)")
        except Exception as e:  # noqa: BLE001
            failures.append((url, str(e)))
            print(f"[{i:>2}/{len(urls)}] FAIL {url}\n           {e}")
        time.sleep(args.sleep)

    # Write a manifest the wiki builder can read.
    manifest = out_dir / "_manifest.tsv"
    with manifest.open("w", encoding="utf-8") as fh:
        fh.write("file\ttitle\tmethod\tchars\tsource_url\n")
        for r in results:
            fh.write(f"{r['file']}\t{r['title']}\t{r['method']}\t"
                     f"{r['chars']}\t{r['url']}\n")

    print(f"\nDone. {len(results)} saved, {len(failures)} failed -> {out_dir}/")
    print(f"Manifest: {manifest}")
    if failures:
        print("\nFailures:")
        for u, e in failures:
            print(f"  - {u}: {e}")


if __name__ == "__main__":
    main()
