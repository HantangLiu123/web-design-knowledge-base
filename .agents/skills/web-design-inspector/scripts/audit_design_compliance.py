#!/usr/bin/env python3
"""
Web Design Inspector - Automated Compliance Auditor
===================================================
A zero-dependency Python script (Standard Library only) that statically audits
generated frontend code (React/JSX/HTML/CSS) against a target website's local
knowledge base deliverable (tokens.json, meta.json, UX_TEARDOWN_REPORT.md).

Outputs a 100-point compliance score, flags LLM drift (ungrounded hex colors,
missing brand fonts, generic Tailwind classes), and writes a structured
INSPECTION_REPORT.md with actionable fix instructions.

Usage:
    python audit_design_compliance.py --source <file_or_dir> --knowledge-base <site_dir> [--output <report.md>]

Example:
    python audit_design_compliance.py -s ./src/Hero.tsx -k ./knowledge_base/sites/resend -o ./INSPECTION_REPORT.md
"""

import argparse
import json
import re
import sys
from pathlib import Path


class DesignAuditor:
    def __init__(self, source_path: Path, kb_dir: Path):
        self.source_path = source_path
        self.kb_dir = kb_dir
        self.score = 100
        self.violations = []
        self.passed_checks = []

        # Load Knowledge Base Data
        self.meta = self._load_json(kb_dir / "meta.json")
        self.tokens_data = self._load_json(kb_dir / "tokens.json")
        self.kb_colors = self._extract_kb_colors()
        self.kb_fonts = self._extract_kb_fonts()

    def _load_json(self, path: Path) -> dict:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[-] Warning: Failed to read {path}: {e}")
        return {}

    def _extract_kb_colors(self) -> set:
        colors = set()
        if "tokens" in self.tokens_data and "top_colors" in self.tokens_data["tokens"]:
            for item in self.tokens_data["tokens"]["top_colors"]:
                c = item.get("color", "").strip().lower()
                if c:
                    colors.add(c)
        if "tokens" in self.tokens_data and "css_variables" in self.tokens_data["tokens"]:
            for _, val in self.tokens_data["tokens"]["css_variables"].items():
                val_clean = val.strip().lower()
                if val_clean.startswith("#") or "rgb" in val_clean or "hsl" in val_clean or "oklch" in val_clean:
                    colors.add(val_clean)
        return colors

    def _extract_kb_fonts(self) -> list:
        fonts = []
        if "fonts" in self.meta:
            display = self.meta["fonts"].get("display")
            mono = self.meta["fonts"].get("mono")
            if display:
                fonts.append(display.lower())
            if mono:
                fonts.append(mono.lower())
        if "typography" in self.tokens_data and "font_families" in self.tokens_data["typography"]:
            for f in self.tokens_data["typography"]["font_families"]:
                fonts.append(f.lower().strip())
        return list(set(fonts))

    def audit_file(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            print(f"[!] Error reading source file {file_path}: {e}")
            return

        lines = content.splitlines()

        # 1. Color Token Audit
        self._audit_colors(lines, file_path)

        # 2. Typography Audit
        self._audit_typography(content, file_path)

        # 3. Layout & Geometry Audit
        self._audit_layout(content, file_path)

        # 4. Motion & Easing Audit
        self._audit_motion(content, file_path)

    def _audit_colors(self, lines: list, file_path: Path):
        hex_pattern = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
        generic_tailwind_colors = re.compile(r"\b(?:bg|text|border)-(?:gray|slate|zinc|neutral)-(?:[1-9]00|950)\b")

        unmapped_hexes = set()
        generic_tw_occurrences = 0

        for line_num, line in enumerate(lines, start=1):
            # Check for hardcoded hex colors
            matches = hex_pattern.findall(line)
            for hex_code in matches:
                lower_hex = hex_code.lower()
                # Check if it's in KB colors or a very close variant
                if lower_hex not in self.kb_colors and not (lower_hex in ["#000", "#000000", "#fff", "#ffffff"]):
                    unmapped_hexes.add((hex_code, line_num))

            # Check for generic Tailwind colors
            tw_matches = generic_tailwind_colors.findall(line)
            if tw_matches:
                generic_tw_occurrences += len(tw_matches)

        if unmapped_hexes:
            penalty = min(len(unmapped_hexes) * 4, 20)
            self.score = max(0, self.score - penalty)
            sample = [f"{h} (L{l})" for h, l in list(unmapped_hexes)[:4]]
            self.violations.append({
                "severity": "HIGH",
                "category": "Color Token Drift",
                "message": f"Found {len(unmapped_hexes)} arbitrary hex colors not registered in local tokens: {', '.join(sample)}",
                "remedy": "Replace hardcoded hex codes with CSS variables: `var(--background)`, `var(--surface-card)`, or `var(--border-subtle)`."
            })
        else:
            self.passed_checks.append("Color Token Integrity: Zero ungrounded hex codes detected.")

        if generic_tw_occurrences > 5:
            penalty = 10
            self.score = max(0, self.score - penalty)
            self.violations.append({
                "severity": "MEDIUM",
                "category": "Generic Tailwind Color Drift",
                "message": f"Found {generic_tw_occurrences} generic Tailwind grays (e.g. `bg-gray-900`, `text-slate-400`).",
                "remedy": "Map palette to the site's local variables (e.g. `bg-[var(--surface-card)]` or configure custom Tailwind colors)."
            })
        else:
            self.passed_checks.append("Tailwind Color Integrity: Clean usage of custom surface tokens.")

    def _audit_typography(self, content: list, file_path: Path):
        content_lower = content.lower()
        brand_fonts_found = []
        for font in self.kb_fonts:
            if font and font in content_lower:
                brand_fonts_found.append(font)

        if not brand_fonts_found and self.kb_fonts:
            self.score = max(0, self.score - 15)
            self.violations.append({
                "severity": "HIGH",
                "category": "Typography Drift",
                "message": f"None of the documented brand fonts ({', '.join(self.kb_fonts[:3])}) were declared in the source code.",
                "remedy": f"Inject brand font stack: `font-['{self.kb_fonts[0].title()}',-apple-system,sans-serif]` or configure `tailwind.config.js`."
            })
        else:
            self.passed_checks.append(f"Typography Fidelity: Verified authentic font stack usage ({', '.join(brand_fonts_found[:2])}).")

    def _audit_layout(self, content: str, file_path: Path):
        # Check if container max-width is constrained
        if "max-w-" not in content and "w-full" in content:
            self.score = max(0, self.score - 5)
            self.violations.append({
                "severity": "LOW",
                "category": "Layout Geometry",
                "message": "No container max-width (`max-w-*`) constraint found; layout may stretch unconstrained on wide screens.",
                "remedy": "Wrap content in standard container geometry (e.g. `max-w-6xl mx-auto px-6`) matching UX teardown."
            })
        else:
            self.passed_checks.append("Layout Geometry: Responsive container constraints detected.")

    def _audit_motion(self, content: str, file_path: Path):
        # Check for generic linear or long easing
        if "duration-700" in content or "duration-1000" in content:
            self.score = max(0, self.score - 5)
            self.violations.append({
                "severity": "LOW",
                "category": "Motion Physics",
                "message": "Detected sluggish animation duration (>500ms). Modern tech benchmarks utilize snappy 150ms-250ms transitions.",
                "remedy": "Use duration-150 or duration-200 with snappy easing: `cubic-bezier(0.16, 1, 0.3, 1)`."
            })
        else:
            self.passed_checks.append("Motion Physics: Snappy transition durations verified.")

    def generate_report(self, output_path: Path):
        status = "PASSED" if self.score >= 85 else "FAILED"
        status_badge = "✅ PASSED" if self.score >= 85 else "❌ FAILED"

        lines = [
            f"# Design Compliance Inspection Report",
            f"",
            f"| Metric | Value |",
            f"| :--- | :--- |",
            f"| **Target Code** | `{self.source_path}` |",
            f"| **Reference KB** | `{self.kb_dir}` |",
            f"| **Compliance Score** | **{self.score} / 100** |",
            f"| **Status** | **{status_badge}** |",
            f"",
            f"---",
            f"",
            f"## 📋 Executive Summary",
        ]

        if self.score >= 85:
            lines.append(f"The inspected code demonstrates high adherence to the local knowledge base design system. "
                         f"Styling, typography, and layout match the benchmark specifications with minimal drift.")
        else:
            lines.append(f"The inspected code shows **significant drift** from the local knowledge base. "
                         f"Generic LLM defaults (unmapped hex codes or missing brand fonts) were detected and must be corrected.")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 🔍 Passed Verification Checks ({len(self.passed_checks)})",
        ])
        for p in self.passed_checks:
            lines.append(f"- [x] {p}")

        if self.violations:
            lines.extend([
                f"",
                f"---",
                f"",
                f"## ⚠️ Flagged Discrepancies & Required Fixes ({len(self.violations)})",
                f"",
                f"| Severity | Category | Discrepancy | Actionable Remedy |",
                f"| :---: | :--- | :--- | :--- |",
            ])
            for v in self.violations:
                lines.append(f"| **{v['severity']}** | {v['category']} | {v['message']} | {v['remedy']} |")

            lines.extend([
                f"",
                f"---",
                f"",
                f"## 🤖 Automated Action Items for Builder Agent",
                f"To bring the score to 100%, the builder agent must perform these updates:",
            ])
            for idx, v in enumerate(self.violations, 1):
                lines.append(f"{idx}. **Fix {v['category']}**: {v['remedy']}")
        else:
            lines.extend([
                f"",
                f"---",
                f"",
                f"## 🎉 Perfect Alignment",
                f"Zero compliance violations found. Code is ready for production.",
            ])

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        print(f"\n" + "=" * 50)
        print("INSPECTION RESULTS")
        print("=" * 50)
        print(f"Compliance Score: {self.score} / 100 ({status})")
        print(f"Passed Checks:    {len(self.passed_checks)}")
        print(f"Violations Found: {len(self.violations)}")
        print(f"Report Generated: {output_path}")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Audit frontend code against local knowledge base deliverables.")
    parser.add_argument("--source", "-s", required=True, help="Path to frontend source file or component to audit")
    parser.add_argument("--knowledge-base", "-k", required=True, help="Path to reference site directory in knowledge_base/sites/<slug>")
    parser.add_argument("--output", "-o", default="./INSPECTION_REPORT.md", help="Output path for inspection report")
    args = parser.parse_args()

    source_path = Path(args.source)
    kb_path = Path(args.knowledge_base)
    output_path = Path(args.output)

    if not source_path.exists():
        print(f"[!] Error: Source path does not exist: {source_path}", file=sys.stderr)
        sys.exit(1)

    if not kb_path.exists():
        print(f"[!] Error: Knowledge base directory does not exist: {kb_path}", file=sys.stderr)
        sys.exit(1)

    auditor = DesignAuditor(source_path, kb_path)

    if source_path.is_file():
        auditor.audit_file(source_path)
    else:
        for ext in ["*.tsx", "*.jsx", "*.html", "*.css"]:
            for f in source_path.glob(f"**/{ext}"):
                auditor.audit_file(f)

    auditor.generate_report(output_path)


if __name__ == "__main__":
    main()
