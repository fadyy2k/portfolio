from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "index.html": {"main-content","engineering","case-studies","experience","skills","services","certifications","education","contact"},
    "projects.html": {"main-content","project-map"},
}
REQUIRED_ASSETS = [
    "assets/favicon.svg","assets/og-image.png","assets/profile.jpg",
    "assets/style.css","assets/app.js","robots.txt","sitemap.xml",
]

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.hrefs=[]; self.blank=[]; self.meta_names=set(); self.meta_props=set()
        self.styles=[]; self.scripts=[]; self.images=[]; self.details=0
        self.filter_buttons=0; self.project_cards=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        if tag == "a" and "href" in a: self.hrefs.append(a["href"])
        if tag == "a" and a.get("target") == "_blank": self.blank.append(a)
        if tag == "link" and a.get("rel") == "stylesheet": self.styles.append(a.get("href"))
        if tag == "script" and a.get("src"): self.scripts.append(a.get("src"))
        if tag == "img" and a.get("src"): self.images.append(a.get("src"))
        if tag == "details": self.details += 1
        if tag == "button" and "data-project-filter" in a: self.filter_buttons += 1
        if "data-project-tags" in a: self.project_cards += 1
        if tag == "meta":
            if a.get("name"): self.meta_names.add(a["name"])
            if a.get("property"): self.meta_props.add(a["property"])

parsers={}
errors=[]
for filename, required_ids in PAGES.items():
    path=ROOT/filename
    if not path.exists():
        errors.append(f"missing page: {filename}")
        continue
    p=SiteParser(); p.feed(path.read_text(encoding="utf-8")); parsers[filename]=p

    for value in sorted(set(p.ids)):
        if p.ids.count(value)>1: errors.append(f"{filename}: duplicate id: {value}")
    for value in required_ids:
        if value not in p.ids: errors.append(f"{filename}: missing section/id: {value}")
    for a in p.blank:
        rel=set(a.get("rel","").split())
        if not {"noopener","noreferrer"}.issubset(rel):
            errors.append(f"{filename}: unsafe target=_blank: {a.get('href')}")
    for name in ["description","twitter:card"]:
        if name not in p.meta_names: errors.append(f"{filename}: missing meta name: {name}")
    for prop in ["og:title","og:description","og:image","og:url"]:
        if prop not in p.meta_props: errors.append(f"{filename}: missing Open Graph field: {prop}")
    if "assets/style.css" not in p.styles: errors.append(f"{filename}: main stylesheet not linked")
    if "assets/app.js" not in p.scripts: errors.append(f"{filename}: main script not linked")
    if p.details: errors.append(f"{filename}: hidden <details> content found ({p.details})")

for asset in REQUIRED_ASSETS:
    if not (ROOT/asset).exists(): errors.append(f"missing asset: {asset}")

index=parsers.get("index.html")
if index and "assets/profile.jpg" not in index.images:
    errors.append("index.html: profile image not used")

projects=parsers.get("projects.html")
if projects:
    if projects.filter_buttons < 5: errors.append("projects.html: expected project filter controls")
    if projects.project_cards < 8: errors.append("projects.html: expected curated project/evidence cards")

# Validate local page links and anchors across both HTML files.
for filename,p in parsers.items():
    for href in p.hrefs:
        if href.startswith(("http://","https://","mailto:","tel:")): continue
        parts=urlsplit(href)
        target_name=parts.path or filename
        if target_name.startswith("./"): target_name=target_name[2:]
        if target_name.endswith(".html"):
            if target_name not in parsers and not (ROOT/target_name).exists():
                errors.append(f"{filename}: missing local page: {target_name}")
            if parts.fragment:
                target=parsers.get(target_name)
                if target and parts.fragment not in target.ids:
                    errors.append(f"{filename}: missing anchor {parts.fragment} in {target_name}")
        elif not parts.path and parts.fragment and parts.fragment not in p.ids:
            errors.append(f"{filename}: missing anchor: #{parts.fragment}")

if errors:
    print("Site quality checks FAILED")
    for e in errors: print("-",e)
    raise SystemExit(1)
print("Site quality checks PASSED")
print(f"Validated {len(parsers)} HTML pages, {sum(p.project_cards for p in parsers.values())} project/evidence cards and visible-by-default content.")
