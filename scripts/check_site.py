from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.hrefs=[]; self.blank=[]; self.meta_names=set(); self.meta_props=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        if tag == "a" and "href" in a: self.hrefs.append(a["href"])
        if tag == "a" and a.get("target") == "_blank": self.blank.append(a)
        if tag == "meta":
            if a.get("name"): self.meta_names.add(a["name"])
            if a.get("property"): self.meta_props.add(a["property"])

p=SiteParser(); p.feed(HTML.read_text())
errors=[]
for value in sorted(set(p.ids)):
    if p.ids.count(value) > 1: errors.append(f"duplicate id: {value}")
for href in p.hrefs:
    if href.startswith("#") and len(href)>1 and href[1:] not in p.ids: errors.append(f"missing anchor: {href}")
for a in p.blank:
    rel=set(a.get("rel", "").split())
    if not {"noopener","noreferrer"}.issubset(rel): errors.append(f"unsafe target=_blank: {a.get('href')}")
for name in ["description","twitter:card"]:
    if name not in p.meta_names: errors.append(f"missing meta name: {name}")
for prop in ["og:title","og:description","og:image","og:url"]:
    if prop not in p.meta_props: errors.append(f"missing Open Graph field: {prop}")
for asset in ["assets/favicon.svg","assets/og-image.png","robots.txt","sitemap.xml"]:
    if not (ROOT/asset).exists(): errors.append(f"missing asset: {asset}")
required_ids=["main-content","skills","experience","engineering","services","certifications","education","contact"]
for value in required_ids:
    if value not in p.ids: errors.append(f"missing section/id: {value}")
if errors:
    print("Site quality checks FAILED")
    for e in errors: print("-",e)
    raise SystemExit(1)
print("Site quality checks PASSED")
