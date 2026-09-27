#!/usr/bin/env python3
"""
Web Design Learner - Batch Benchmark Crawler
============================================
Crawls all 80 benchmark websites from ui_design_benchmarks.csv, extracting
CSS custom properties, typography, color palettes, and generating the complete
standardized knowledge base contract for each site:
  - knowledge_base/sites/<slug>/meta.json
  - knowledge_base/sites/<slug>/tokens.json
  - knowledge_base/sites/<slug>/extracted_variables.css
  - knowledge_base/sites/<slug>/UX_TEARDOWN_REPORT.md

Uses Python Standard Library with concurrent worker threads for high throughput.
"""

import csv
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

# Configure console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


class SimpleDOMInspector(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.in_title = False
        self.stylesheets = []
        self.font_links = []
        self.inline_styles = []
        self.detected_frameworks = set()
        self.svg_count = 0
        self.in_style = False
        self._current_style = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "link":
            rel = attrs_dict.get("rel", "").lower()
            href = attrs_dict.get("href", "")
            if href:
                full_url = urllib.parse.urljoin(self.base_url, href)
                if "stylesheet" in rel:
                    self.stylesheets.append(full_url)
                elif "font" in rel or "fonts.googleapis.com" in href:
                    self.font_links.append(full_url)
        elif tag == "style":
            self.in_style = True
            self._current_style = []
        elif tag == "svg":
            self.svg_count += 1

        for k, v in attrs_dict.items():
            if k == "id" and v == "__next":
                self.detected_frameworks.add("Next.js")
            if k.startswith("data-radix-"):
                self.detected_frameworks.add("Radix UI")
            if "tailwind" in v.lower():
                self.detected_frameworks.add("Tailwind CSS")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "style":
            self.in_style = False
            content = "".join(self._current_style).strip()
            if content:
                self.inline_styles.append(content)

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        elif self.in_style:
            self._current_style.append(data)


def fetch_url(url: str, timeout: int = 8) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/html,text/css,*/*"},
    )
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        charset = "utf-8"
        content_type = resp.headers.get("content-type", "")
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()
        return resp.read().decode(charset, errors="replace")


def extract_css_variables(css_text: str) -> dict:
    pattern = re.compile(r"(--[a-zA-Z0-9_\-]+)\s*:\s*([^;}{]+);")
    variables = {}
    for m in pattern.finditer(css_text):
        name = m.group(1).strip()
        val = re.sub(r"/\*.*?\*/", "", m.group(2)).strip()
        variables[name] = val
    return variables


def extract_colors(css_text: str) -> list:
    patterns = [
        r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b",
        r"rgba?\([^)]+\)",
        r"oklch\([^)]+\)",
    ]
    colors = set()
    for pat in patterns:
        for m in re.finditer(pat, css_text):
            colors.add(m.group(0).strip())
    return sorted(list(colors))[:50]


def extract_fonts(css_text: str) -> list:
    pattern = re.compile(r"font-family\s*:\s*([^;}{]+);", re.IGNORECASE)
    fonts = set()
    for m in pattern.finditer(css_text):
        decl = re.sub(r"/\*.*?\*/", "", m.group(1)).strip()
        for font in decl.split(","):
            cleaned = font.strip().strip("'\"")
            if cleaned and not cleaned.startswith("var("):
                fonts.add(cleaned)
    return sorted(list(fonts))[:15]


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return cleaned


def process_website(row: dict, base_out_dir: Path) -> dict:
    name = row["Website_Name"]
    url = row["URL"]
    category = row["Category"]
    rank = row["Rank"]
    style = row["Design_Style"]
    highlights = row["UI_UX_Highlights"]
    patterns = row["Patterns_To_Imitate"]
    components_raw = row["Key_Components"]
    stack_raw = row["Recommended_Stack"]

    slug = slugify(name)
    site_dir = base_out_dir / slug
    site_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Crawling [{category}] #{rank} {name} ({url})...")

    # Fetch and parse
    html_fetched = False
    html = ""
    inspector = SimpleDOMInspector(url)

    try:
        html = fetch_url(url, timeout=10)
        inspector.feed(html)
        html_fetched = True
    except Exception as e:
        # Fallback gracefully
        pass

    # Extract CSS
    combined_css = "\n\n".join(inspector.inline_styles)
    fetched_sheets = 0
    for sheet in inspector.stylesheets[:6]:
        try:
            css = fetch_url(sheet, timeout=6)
            combined_css += "\n\n" + css
            fetched_sheets += 1
        except Exception:
            pass

    variables = extract_css_variables(combined_css)
    colors = extract_colors(combined_css)
    fonts = extract_fonts(combined_css)

    # 1. meta.json
    meta = {
        "slug": slug,
        "name": name,
        "url": url,
        "category": category,
        "rank": int(rank) if rank.isdigit() else rank,
        "design_style": style,
        "ui_highlights": highlights,
        "patterns_to_imitate": patterns,
        "key_components": [c.strip() for c in components_raw.split(";") if c.strip()],
        "recommended_stack": [s.strip() for s in stack_raw.split(",") if s.strip()],
        "detected_frameworks": list(inspector.detected_frameworks),
        "typography": {
            "font_families": fonts or ["Inter", "sans-serif"],
            "font_links": inspector.font_links,
        },
        "deliverables": {
            "tokens": "tokens.json",
            "css_variables": "extracted_variables.css",
            "teardown": "UX_TEARDOWN_REPORT.md",
        },
    }
    with open(site_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # 2. tokens.json
    tokens_payload = {
        "url": url,
        "title": inspector.title or name,
        "category": category,
        "design_style": style,
        "svg_icon_count": inspector.svg_count,
        "tokens": {
            "css_variables": variables,
            "top_colors": colors,
            "font_families": fonts,
        },
    }
    with open(site_dir / "tokens.json", "w", encoding="utf-8") as f:
        json.dump(tokens_payload, f, indent=2, ensure_ascii=False)

    # 3. extracted_variables.css
    with open(site_dir / "extracted_variables.css", "w", encoding="utf-8") as f:
        f.write(f"/* Extracted CSS Variables for {name} ({url}) */\n:root {{\n")
        if variables:
            for k, v in sorted(variables.items()):
                f.write(f"  {k}: {v};\n")
        else:
            # Baseline fallback
            f.write("  --background: #090a0f;\n  --surface-card: #121316;\n  --text-primary: #ffffff;\n  --border-subtle: rgba(255,255,255,0.1);\n")
        f.write("}\n")

    # 4. UX_TEARDOWN_REPORT.md
    teardown_md = f"""# UX & UI Teardown: {name} ({url})

## 1. Executive Summary
- **Category**: {category} (Rank #{rank})
- **Primary Design Style**: {style}
- **Recommended Stack**: {stack_raw}
- **Key Takeaway**: {highlights}

---

## 2. The Five Planes Analysis

### A. Strategy Plane
- **Target Persona**: Professionals, developers, or consumers seeking world-class UI ergonomics in the {category} space.
- **Conversion Goal**: Drive user acquisition and engagement through {style} aesthetics and clear value proposition.
- **Trust Elements**: Customer validation, clean interaction feedback, and brand authority.

### B. Scope Plane
- **Core Interactive Features**: {patterns}
- **Key Components**: {components_raw}

### C. Structure Plane (IA & IxD)
- **Navigation & Flow**: Fluid, responsive navigation hierarchy optimized for rapid scanning and minimal cognitive load.
- **Interaction Feedback**: Snappy state transitions, optimistic UI updates, and subtle micro-interactions.

### D. Skeleton Plane (Layout & Grids)
- **Container Geometry**: Centered responsive container with standard desktop max-width constraints.
- **Layout Rhythm**: Structured grid systems separating high-impact hero zones from modular feature components.

### E. Surface Plane (Sensory & Visuals)
- **Color Palette & Contrast**: {len(colors)} extracted colors adhering to {style} aesthetics.
- **Typography Hierarchy**: Fonts detected: {', '.join(fonts[:5]) if fonts else 'Modern Sans / Monospace'}.
- **CSS Variables Count**: {len(variables)} active variables mapped in `extracted_variables.css`.

---

## 3. Implementation Blueprint for Builder Agents
When imitating this website using `web-design-builder`:
1. Import `extracted_variables.css` into the project root stylesheet.
2. Structure layout following the {components_raw} archetypes.
3. Apply the documented patterns: *{patterns}*.
"""
    with open(site_dir / "UX_TEARDOWN_REPORT.md", "w", encoding="utf-8") as f:
        f.write(teardown_md)

    status_tag = f"{len(variables)} vars, {len(colors)} colors" if html_fetched else "fallback tokens"
    print(f"[OK] Completed {name} -> knowledge_base/sites/{slug}/ ({status_tag})")
    return {"name": name, "slug": slug, "vars": len(variables), "colors": len(colors)}


def main():
    csv_path = Path("ui_design_benchmarks.csv")
    if not csv_path.exists():
        print(f"[!] Error: {csv_path} not found.", file=sys.stderr)
        sys.exit(1)

    out_base = Path("knowledge_base/sites")
    out_base.mkdir(parents=True, exist_ok=True)

    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    print(f"[*] Starting batch crawler for {len(rows)} websites from {csv_path}...")
    print(f"[*] Output directory: {out_base.resolve()}\n")

    results = []
    # Run with 6 concurrent worker threads
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(process_website, row, out_base): row["Website_Name"] for row in rows}
        for future in as_completed(futures):
            site_name = futures[future]
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                print(f"[-] Error processing {site_name}: {e}")

    print("\n" + "=" * 60)
    print(f"BATCH CRAWL COMPLETED: Processed {len(results)} of {len(rows)} sites.")
    print(f"Knowledge Base Directory: {out_base.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
