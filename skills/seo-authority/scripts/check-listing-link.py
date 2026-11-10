#!/usr/bin/env python3
"""Prove a platform listing links to us: fetch the live page, find every <a> whose href hits our domain, report rel.
Usage: check-listing-link.py <listing_url> <our_domain>   Exit 0 = at least one followed link, 1 = only nofollow/ugc/sponsored, 2 = no link, 3 = fetch failed (blocked or down: check in a browser)."""
import sys, urllib.error, urllib.request
from html.parser import HTMLParser

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.found = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            a = dict(attrs); self.found.append((a.get("href") or "", (a.get("rel") or "").lower()))

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    url, domain = sys.argv[1], sys.argv[2].lower().removeprefix("www.")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link-check)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", "replace"); status = r.status
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"{url} -> FETCH FAILED: {e} (blocked or down; check in a browser)", file=sys.stderr); sys.exit(3)
    p = Links(); p.feed(html)
    hits = [(h, rel) for h, rel in p.found if domain in h.lower()]
    print(f"{url} -> HTTP {status}, {len(p.found)} links, {len(hits)} to {domain}")
    for h, rel in hits:
        blocked = [t for t in ("nofollow", "ugc", "sponsored") if t in rel.split()]
        print(f"  {'NOFOLLOW' if blocked else 'FOLLOW  '} rel='{rel}' {h}")
    if not hits:
        print("  NO LINK in server HTML (may be client-rendered: recheck in a browser)"); sys.exit(2)
    sys.exit(0 if any(not any(t in rel.split() for t in ("nofollow", "ugc", "sponsored")) for _, rel in hits) else 1)

if __name__ == "__main__":
    main()
