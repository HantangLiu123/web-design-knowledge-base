# UI Fidelity & Alignment Checklist

Use this checklist to audit any generated frontend code against the local knowledge base before delivering it to the user.

---

## 1. Token Alignment Audit
- [ ] **Canvas Color**: Does the body/page background match the extracted `--background` variable?
- [ ] **Surface Card Colors**: Do container/card backgrounds match `--surface-*` or the top dark hex codes from `tokens.json`?
- [ ] **Borders**: Are all card and divider borders using the exact translucent alpha values (`rgba(255, 255, 255, 0.08)` to `0.12`)?
- [ ] **Text Hierarchy**: Is `text-primary` pure white or off-white, and is `text-muted` matched to the extracted muted color?
- [ ] **Zero Hallucinated Colors**: Are there any arbitrary hex codes not found in `tokens.json`?

---

## 2. Typography & Hierarchy Audit
- [ ] **Font Family**: Is the primary brand font declared with appropriate system fallbacks?
- [ ] **Monospace Font**: Are code blocks, pills, badges, and metrics using the extracted monospace font (e.g. `Commit Mono`, `Geist Mono`)?
- [ ] **Scale & Tracking**: Do headline elements have tighter letter spacing (`tracking-tight` or `-0.02em`)?

---

## 3. Layout & Geometry Audit
- [ ] **Container Max-Width**: Is the overall page container constrained according to `UX_TEARDOWN_REPORT.md` (e.g. `max-w-6xl`)?
- [ ] **Grid Spans**: Do Bento cards match the asymmetric column and row spans defined in the benchmark teardown?
- [ ] **Responsive Breakpoints**: Does the grid cleanly collapse to a single column on mobile screens (`col-span-12`)?

---

## 4. Interaction & Motion Audit
- [ ] **Hover Feedback**: Do interactive cards and buttons have subtle hover elevation or border illumination?
- [ ] **Transition Physics**: Are transitions snappy (150ms–250ms) using cubic-bezier easing curves rather than linear transitions?
- [ ] **Focus Rings**: Are form elements and clickable buttons accessible via keyboard with dual-ring focus styles?
