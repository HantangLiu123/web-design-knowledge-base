#!/usr/bin/env python3
"""
Web Design Learner - Design Token & Asset Extractor
===================================================
A zero-dependency Python script (Standard Library only) designed for AI agents
and developers to automatically fetch, crawl stylesheets, and extract design
tokens (CSS variables, colors, typography, borders, shadows, breakpoints)
from any target website.

Usage:
    python extract_design_tokens.py <url> [--output-dir <path>]

Example:
    python extract_design_tokens.py https://linear.app --output-dir ./extracted/linear
"""

import argparse
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


class DOMInspector(HTMLParser):
    """Parses HTML to extract stylesheets, fonts, inline styles, and framework indicators."""

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.in_title = False
        self.stylesheets = []
        self.font_links = []
        self.inline_styles = []
        self.meta_tags = {}
        self.detected_frameworks = set()
        self.svg_count = 0
        self.in_style = False
        self._current_style_content = []

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
                elif "font" in rel or "fonts.googleapis.com" in href or "use.typekit.net" in href:
                    self.font_links.append(full_url)

        elif tag == "style":
            self.in_style = True
            self._current_style_content = []

        elif tag == "meta":
            name = attrs_dict.get("name") or attrs_dict.get("property")
            content = attrs_dict.get("content")
            if name and content:
                self.meta_tags[name] = content

        elif tag == "svg":
            self.svg_count += 1

        # Framework heuristics based on attributes and IDs
        for key, val in attrs_dict.items():
            if key == "id":
                if val == "__next":
                    self.detected_frameworks.add("Next.js")
                elif val == "root" or val == "app":
                    self.detected_frameworks.add("SPA (React/Vue/Vite)")
            if key.startswith("data-radix-"):
                self.detected_frameworks.add("Radix UI / Shadcn")
            if key.startswith("data-framer-"):
                self.detected_frameworks.add("Framer Motion")
            if "tailwind" in val.lower():
                self.detected_frameworks.add("Tailwind CSS")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "style":
            self.in_style = False
            content = "".join(self._current_style_content).strip()
            if content:
                self.inline_styles.append(content)

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        elif self.in_style:
            self._current_style_content.append(data)


def fetch_url(url: str, timeout: int = 15) -> str:
    """Fetch text content from a URL with custom user-agent and SSL handling."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url,
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/html,text/css,*/*"},
    )
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
        content_type = response.headers.get("content-type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()
        return response.read().decode(charset, errors="replace")


def extract_css_variables(css_text: str) -> dict:
    """Extract custom properties (variables) defined like --my-var: value;"""
    var_pattern = re.compile(r"(--[a-zA-Z0-9_\-]+)\s*:\s*([^;}{]+);")
    variables = {}
    for match in var_pattern.finditer(css_text):
        name = match.group(1).strip()
        val = match.group(2).strip()
        # Clean up comments
        val = re.sub(r"/\*.*?\*/", "", val).strip()
        variables[name] = val
    return variables


def extract_colors(css_text: str) -> list:
    """Extract hex, rgb/rgba, hsl/hsla, and oklch colors with occurrence counts."""
    patterns = [
        r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b",
        r"rgba?\([^)]+\)",
        r"hsla?\([^)]+\)",
        r"oklch\([^)]+\)",
    ]
    colors = []
    for pat in patterns:
        for match in re.finditer(pat, css_text):
            colors.append(match.group(0).strip())

    counter = Counter(colors)
    return [{"color": color, "count": count} for color, count in counter.most_common(50)]


def extract_font_families(css_text: str) -> list:
    """Extract unique font families mentioned in font-family declarations."""
    pattern = re.compile(r"font-family\s*:\s*([^;}{]+);", re.IGNORECASE)
    fonts = set()
    for match in pattern.finditer(css_text):
        font_decl = match.group(1).strip()
        # Clean quotes and splits
        font_decl = re.sub(r"/\*.*?\*/", "", font_decl).strip()
        for font in font_decl.split(","):
            cleaned = font.strip().strip("'\"")
            if cleaned and not cleaned.startswith("var("):
                fonts.add(cleaned)
    return sorted(list(fonts))


def extract_radii(css_text: str) -> list:
    """Extract common border-radius values."""
    pattern = re.compile(r"border-radius\s*:\s*([^;}{]+);", re.IGNORECASE)
    radii = Counter()
    for match in pattern.finditer(css_text):
        val = match.group(1).strip()
        val = re.sub(r"/\*.*?\*/", "", val).strip()
        if not val.startswith("var("):
            radii[val] += 1
    return [{"radius": r, "count": c} for r, c in radii.most_common(15)]


def extract_shadows(css_text: str) -> list:
    """Extract common box-shadow values."""
    pattern = re.compile(r"box-shadow\s*:\s*([^;}{]+);", re.IGNORECASE)
    shadows = Counter()
    for match in pattern.finditer(css_text):
        val = match.group(1).strip()
        val = re.sub(r"/\*.*?\*/", "", val).strip()
        if val != "none" and not val.startswith("var("):
            shadows[val] += 1
    return [{"shadow": s, "count": c} for s, c in shadows.most_common(10)]


def extract_breakpoints(css_text: str) -> list:
    """Extract responsive media queries."""
    pattern = re.compile(r"@media\s*([^{]+)\{", re.IGNORECASE)
    queries = set()
    for match in pattern.finditer(css_text):
        q = match.group(1).strip()
        queries.add(q)
    return sorted(list(queries))


def main():
    parser = argparse.ArgumentParser(description="Fetch and extract website design tokens.")
    parser.add_argument("url", help="Target website URL (e.g. https://linear.app)")
    parser.add_argument("--output-dir", "-o", default=None, help="Directory to save extracted data (defaults to knowledge_base/sites/<slug>)")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Compute site slug from URL if not specified
    parsed_netloc = urllib.parse.urlparse(url).netloc.split(":")[0]
    domain_clean = re.sub(r"^www\.", "", parsed_netloc)
    slug = domain_clean.split(".")[0] if domain_clean else "site"

    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        out_dir = Path("knowledge_base") / "sites" / slug

    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Fetching HTML from {url}...")
    try:
        html = fetch_url(url)
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse DOM
    inspector = DOMInspector(url)
    inspector.feed(html)

    print(f"[+] Found {len(inspector.stylesheets)} stylesheet(s) and {len(inspector.inline_styles)} inline style block(s).")
    print(f"[+] Detected Frameworks: {', '.join(inspector.detected_frameworks) or 'Standard Web'}")

    # Aggregate CSS
    all_css_chunks = list(inspector.inline_styles)
    for sheet_url in inspector.stylesheets[:10]:  # Limit to first 10 stylesheets
        try:
            print(f"[*] Fetching stylesheet: {sheet_url}")
            css = fetch_url(sheet_url, timeout=10)
            all_css_chunks.append(css)
        except Exception as e:
            print(f"[-] Could not fetch stylesheet {sheet_url}: {e}")

    combined_css = "\n\n".join(all_css_chunks)

    # Extract design elements
    variables = extract_css_variables(combined_css)
    colors = extract_colors(combined_css)
    fonts = extract_font_families(combined_css)
    radii = extract_radii(combined_css)
    shadows = extract_shadows(combined_css)
    breakpoints = extract_breakpoints(combined_css)

    # Build result
    result = {
        "url": url,
        "title": inspector.title,
        "meta": inspector.meta_tags,
        "frameworks": list(inspector.detected_frameworks),
        "svg_icon_count": inspector.svg_count,
        "font_links": inspector.font_links,
        "typography": {
            "font_families": fonts,
        },
        "tokens": {
            "css_variables": variables,
            "top_colors": colors,
            "radii": radii,
            "shadows": shadows,
            "media_breakpoints": breakpoints,
        },
    }

    # Save tokens.json
    json_path = out_dir / "tokens.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved structured design tokens to: {json_path}")

    # Generate starter CSS file
    css_path = out_dir / "extracted_variables.css"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(f"/* Extracted CSS Variables from {url} */\n:root {{\n")
        for var_name, var_val in sorted(variables.items()):
            f.write(f"  {var_name}: {var_val};\n")
        f.write("}\n")
    print(f"[OK] Saved extracted CSS variables to: {css_path}")

    # Print summary to stdout for agents
    print("\n" + "=" * 50)
    print("EXTRACTION SUMMARY")
    print("=" * 50)
    print(f"Title: {inspector.title}")
    print(f"Frameworks: {', '.join(inspector.detected_frameworks) or 'None'}")
    print(f"Font Families: {', '.join(fonts[:6])}")
    print(f"CSS Variables Extracted: {len(variables)}")
    print(f"Distinct Colors Found: {len(colors)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
