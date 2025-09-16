#!/usr/bin/env python3
import os, sys, time, hashlib, html
from datetime import datetime
import feedparser

RSS_URL = os.environ.get("RSS_URL")
POSTS_DIR = os.environ.get("POSTS_DIR", "_posts")

if not RSS_URL:
    print("ERROR: RSS_URL environment variable is required.")
    sys.exit(1)

def slugify(value):
    value = value.lower()
    value = "".join(ch if ch.isalnum() or ch in (" ", "-") else "-" for ch in value)
    value = "-".join(value.strip().split())
    while "--" in value:
        value = value.replace("--", "-")
    return value.strip("-")

def safe_filename(date_obj, title):
    s = slugify(title) or hashlib.md5(title.encode("utf-8")).hexdigest()[:8]
    return f"{date_obj.strftime('%Y-%m-%d')}-{s}.md"

def entry_date(entry):
    t = None
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        t = entry.published_parsed
    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
        t = entry.updated_parsed
    if t:
        return datetime.fromtimestamp(time.mktime(t))
    return datetime.utcnow()

def entry_content(entry):
    if hasattr(entry, "content") and entry.content:
        return "\n\n".join(c.value for c in entry.content)
    if hasattr(entry, "summary") and entry.summary:
        return entry.summary
    if hasattr(entry, "description") and entry.description:
        return entry.description
    return ""

def front_matter(title, date, original_url):
    fm = [
        "---",
        f"title: \"{title.replace('\\','').replace('"','\\"')}\"",
        f"date: {date.strftime('%Y-%m-%d %H:%M:%S %z')}",
        "layout: post",
        f"original: \"{original_url}\"",
        "---",
        ""
    ]
    return "\n".join(fm)

def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("No entries found.")
        return
    os.makedirs(POSTS_DIR, exist_ok=True)
    for entry in feed.entries[::-1]:
        title = entry.get("title", "untitled")
        content = entry_content(entry)
        link = entry.get("link", "")
        date = entry_date(entry)
        filename = safe_filename(date, title)
        filepath = os.path.join(POSTS_DIR, filename)
        if os.path.exists(filepath):
            continue
        md = front_matter(title, date, link) + html.unescape(content) + "\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Created: {filepath}")

if __name__ == "__main__":
    main()
