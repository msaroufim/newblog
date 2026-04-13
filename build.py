#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

import markdown
import yaml
from jinja2 import Environment
from markdown.extensions.codehilite import CodeHiliteExtension
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "_site"
ASSETS_DIR = ROOT / "assets"
POSTS_DIR = ROOT / "_posts"
DATA_DIR = ROOT / "_data"
PAGES = ["index.md", "blog.md", "talks.md", "bookshelf.md", "404.html"]


SITE = {
    "title": "Mark Saroufim",
    "author": "Mark Saroufim",
    "description": "My personal blog",
    "base_url": "https://www.marksaroufim.com",
    "color_scheme": "avocado",
    "analytics_id": "UA-127963930-2",
}


DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <!-- meta information -->
<meta charset="utf-8">
<meta name="description" content="{{ meta_description }}">
<meta name="author" content="{{ site.author }}">

<!-- Enable responsiveness on mobile devices-->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">

<!-- title -->
<title>{% if page.title %}{{ page.title }} &middot; {% endif %}{{ site.title }}</title>

<!-- icons -->
<link rel="shortcut icon" href="/assets/images/favicon.ico">

<!-- stylesheets -->
<link rel="stylesheet" href="/assets/css/responsive.gs.12col.css">
<link rel="stylesheet" href="/assets/css/syntax.css">
<link rel="stylesheet" href="/assets/css/main.css">

<!-- Google fonts -->
<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700,400italic&subset=latin-ext">

<script type="text/javascript" async
src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>

<!-- feed links -->
<link rel="alternate" href="/feed.xml" type="application/rss+xml" title="{{ site.title }}">
  </head>
  <body>
    <main class="container {{ site.color_scheme }}">
      <header>
        <div>
          <a href="/" id="logo" title="{{ site.title }}" style="background-image: url(/assets/images/logo.png);"></a>
        </div>

        <nav id="main-navigation">
  {% for link in nav_links %}
  <a href="{{ link.url }}" title="{{ link.title }}"{% if page.title == link.title %} class="current"{% endif %}>{{ link.title }}</a>
  {% endfor %}
</nav>
      </header>

      {{ content | safe }}

    <!-- scripts -->
    <script src="/assets/js/fluidvids.min.js"></script>
    <script>
      fluidvids.init({
        selector: ['iframe', 'object'],
        players: ['www.youtube.com', 'player.vimeo.com']
      });
    </script>
  </body>
  <div style="text-align: center; margin-top: 2em; margin-bottom: 2em;">
    <a href="https://medium.com/@marksaroufim" title="Medium" style="text-decoration: none; margin: 0 0.5em;">📝</a>
    <a href="https://github.com/msaroufim" title="Github" style="text-decoration: none; margin: 0 0.5em;">👨‍💻</a>
    <a href="https://twitter.com/marksaroufim" title="Twitter" style="text-decoration: none; margin: 0 0.5em;">🐦</a>
    <a href="http://marksaroufim.substack.com/" title="Substack" style="text-decoration: none; margin: 0 0.5em;">📧</a>
    <a href="https://www.twitch.tv/marksaroufim" title="Twitch" style="text-decoration: none; margin: 0 0.5em;">🎮</a>
    <a href="https://www.youtube.com/@marksaroufim" title="Youtube" style="text-decoration: none; margin: 0 0.5em;">🎥</a>
  </div>
</html>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ site.analytics_id }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '{{ site.analytics_id }}');
</script>
"""


NOT_FOUND_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <!-- meta information -->
<meta charset="utf-8">
<meta name="description" content="{{ site.description }}">
<meta name="author" content="{{ site.author }}">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">
<title>{{ site.title }}</title>
<link rel="shortcut icon" href="/assets/images/favicon.ico">
<link rel="stylesheet" href="/assets/css/responsive.gs.12col.css">
<link rel="stylesheet" href="/assets/css/syntax.css">
<link rel="stylesheet" href="/assets/css/main.css">
  </head>
  <body>
    <div class="container not-found">
      <h1 class="bounceInDown animated">404</h1>
      <p>
        Did You steal the content from me? No?! Well, somebody did, and you're the only one here.
      </p>
    </div>
  </body>
</html>
"""


@dataclass
class Document:
    source_path: Path
    meta: dict[str, Any]
    body: str
    title: str
    url: str
    output_path: Path
    html_content: str
    published_at: dt.datetime | None = None


def parse_front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    _, rest = text.split("---\n", 1)
    front_matter, body = rest.split("\n---\n", 1)
    meta = yaml.safe_load(front_matter) or {}
    return meta, body.lstrip("\n")


def preprocess_markdown(text: str) -> str:
    def replace_highlight(match: re.Match[str]) -> str:
        language = match.group("lang").strip()
        code = match.group("code").strip("\n")
        return f"\n```{language}\n{code}\n```\n"

    processed = re.sub(
        r"{%\s*highlight\s+(?P<lang>[^\s%]+)\s*%}(?P<code>.*?){%\s*endhighlight\s*%}",
        replace_highlight,
        text,
        flags=re.DOTALL,
    )

    lines = processed.splitlines()
    normalized: list[str] = []
    list_item_re = re.compile(r"^(\* |- |\d+\. )")
    for line in lines:
        if (
            normalized
            and line.strip()
            and list_item_re.match(line)
            and normalized[-1].strip()
            and not list_item_re.match(normalized[-1])
        ):
            normalized.append("")
        normalized.append(line)

    return "\n".join(normalized)


def render_markdown(text: str) -> str:
    processed = preprocess_markdown(text)
    md = markdown.Markdown(
        extensions=[
            "extra",
            "smarty",
            "toc",
            CodeHiliteExtension(css_class="highlight", guess_lang=False),
        ],
        output_format="html5",
    )
    return md.convert(processed)


def strip_html(text: str) -> str:
    collapsed = re.sub(r"<[^>]+>", " ", text)
    collapsed = re.sub(r"\s+", " ", collapsed)
    collapsed = collapsed.strip()
    while True:
        unescaped = html.unescape(collapsed)
        if unescaped == collapsed:
            return unescaped
        collapsed = unescaped


def truncate(text: str, length: int = 120) -> str:
    if len(text) <= length:
        return text
    return text[: max(0, length - 3)].rstrip() + "..."


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def page_output_paths(page_path: Path, permalink: str | None) -> tuple[str, list[Path]]:
    if permalink:
        cleaned = permalink.strip("/")
        if not cleaned:
            return "/", [OUTPUT_DIR / "index.html"]
        return f"/{cleaned}/", [OUTPUT_DIR / cleaned / "index.html"]

    if page_path.name == "index.md":
        return "/", [OUTPUT_DIR / "index.html"]

    stem = page_path.stem
    return f"/{stem}", [OUTPUT_DIR / f"{stem}.html", OUTPUT_DIR / stem / "index.html"]


def parse_post_date(path: Path) -> tuple[dt.datetime, str]:
    match = re.match(r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})-(?P<slug>.+)\.md", path.name)
    if not match:
        raise ValueError(f"Unsupported post filename: {path}")
    year = int(match.group("year"))
    month = int(match.group("month"))
    day = int(match.group("day"))
    slug = match.group("slug")
    return dt.datetime(year, month, day), slug


def post_output_path(path: Path, meta: dict[str, Any]) -> tuple[str, Path, dt.datetime]:
    published_at, slug = parse_post_date(path)
    url = f"/{published_at.year:04d}/{published_at.month:02d}/{published_at.day:02d}/{quote(slug)}.html"
    output_path = OUTPUT_DIR / f"{published_at.year:04d}" / f"{published_at.month:02d}" / f"{published_at.day:02d}" / f"{slug}.html"
    return url, output_path, published_at


def load_navigation() -> list[dict[str, str]]:
    return yaml.safe_load((DATA_DIR / "links.yml").read_text(encoding="utf-8")) or []


def build_posts(env: Environment, nav_links: list[dict[str, str]]) -> list[Document]:
    posts: list[Document] = []
    template = env.from_string(DEFAULT_TEMPLATE)

    for path in sorted(POSTS_DIR.glob("*.md")):
        meta, body = parse_front_matter(path)
        html_content = render_markdown(body)
        url, output_path, published_at = post_output_path(path, meta)
        title = str(meta.get("title", path.stem))
        rendered = template.render(
            site=SITE,
            nav_links=nav_links,
            page={"title": title},
            meta_description=truncate(strip_html(html_content)),
            content=html_content,
        )
        ensure_parent(output_path)
        output_path.write_text(rendered, encoding="utf-8")
        posts.append(
            Document(
                source_path=path,
                meta=meta,
                body=body,
                title=title,
                url=url,
                output_path=output_path,
                html_content=html_content,
                published_at=published_at,
            )
        )

    posts.sort(key=lambda post: post.published_at or dt.datetime.min, reverse=True)
    return posts


def build_pages(env: Environment, nav_links: list[dict[str, str]]) -> None:
    template = env.from_string(DEFAULT_TEMPLATE)
    not_found_template = env.from_string(NOT_FOUND_TEMPLATE)

    for name in PAGES:
        path = ROOT / name
        meta, body = parse_front_matter(path)
        title = str(meta.get("title", ""))
        url, output_paths = page_output_paths(path, meta.get("permalink"))

        if name == "404.html":
            rendered = not_found_template.render(site=SITE)
        else:
            content = render_markdown(body) if path.suffix == ".md" else body
            description_source = SITE["description"] if title == "Home" else strip_html(content)
            rendered = template.render(
                site=SITE,
                nav_links=nav_links,
                page={"title": title, "url": url},
                meta_description=truncate(description_source),
                content=content,
            )

        for output_path in output_paths:
            ensure_parent(output_path)
            output_path.write_text(rendered, encoding="utf-8")


def render_feed(posts: list[Document]) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    items = []
    for post in posts[:10]:
        description = xml_escape(post.html_content)
        pub_date = post.published_at.replace(tzinfo=dt.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
        items.append(
            f"""      <item>
        <title>{xml_escape(post.title)}</title>
        <link>{SITE['base_url']}{post.url}</link>
        <pubDate>{pub_date}</pubDate>
        <author>{xml_escape(SITE['author'])}</author>
        <description>{description}</description>
      </item>"""
        )

    channel_date = now.strftime("%a, %d %b %Y %H:%M:%S %z")
    return f"""<?xml version="1.0"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{xml_escape(SITE['title'])}</title>
    <link>{SITE['base_url']}</link>
    <atom:link href="{SITE['base_url']}/feed.xml" rel="self" type="application/rss+xml" />
    <description>{xml_escape(SITE['description'])}</description>
    <language>en-us</language>
    <pubDate>{channel_date}</pubDate>
    <lastBuildDate>{channel_date}</lastBuildDate>
{os.linesep.join(items)}
  </channel>
</rss>
"""


def copy_assets() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    shutil.copytree(ASSETS_DIR, OUTPUT_DIR / "assets")


def write_support_files(posts: list[Document]) -> None:
    (OUTPUT_DIR / "feed.xml").write_text(render_feed(posts), encoding="utf-8")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    env = Environment(autoescape=True)
    nav_links = load_navigation()
    copy_assets()
    posts = build_posts(env, nav_links)
    build_pages(env, nav_links)
    write_support_files(posts)


if __name__ == "__main__":
    main()
