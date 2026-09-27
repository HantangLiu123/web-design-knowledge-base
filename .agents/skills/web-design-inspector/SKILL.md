---
name: web-design-inspector
description: >-
  Audits and inspects frontend code built by the builder agent against local knowledge base deliverables.
  Evaluates token compliance, brand typography fidelity, layout geometry, and motion physics,
  flagging LLM drift and generating actionable inspection reports.
---

# Web Design Inspector: Design Quality & Compliance Auditor Skill

This skill guides an agent in acting as the **Quality Gatekeeper & Critic** in the web design triad (`learner -> builder -> inspector`). It independently verifies that frontend code produced by the builder agent faithfully adheres to the benchmark deliverables stored in the local knowledge base, catching LLM drift, hallucinated colors, and missing brand fonts before code reaches production.

---

## 🛡️ The Inspection Mission

The inspector answers one fundamental question:
> **"Did the builder faithfully replicate the authentic design tokens, typography, layout, and motion from the local knowledge base, or did it drift into generic LLM defaults?"**

```
┌─────────────────────────────────┐
│     TARGET SOURCE CODE          │ (e.g. src/components/Hero.tsx)
└────────────────┬────────────────┘
                 │
                 ▼               vs.
┌─────────────────────────────────┐
│  LOCAL KNOWLEDGE BASE DELIVERABLE│ (knowledge_base/sites/<slug>/)
└────────────────┬────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     THE 5-POINT COMPLIANCE AUDIT                       │
│  1. Colors (30pts)  2. Typography (20pts)  3. Layout/Grids (20pts)     │
│  4. Surface Depth (15pts)                  5. Motion & A11y (15pts)    │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   INSPECTION_REPORT.md DELIVERABLE                     │
│   • Quantitative Score (0-100)      • Pass / Fail Decision             │
│   • Flagged Discrepancy Table       • Actionable Patches for Builder   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Automated Audit Script (Recommended Shortcut)

An automated zero-dependency Python auditor is bundled with this skill:

```powershell
python .agents/skills/web-design-inspector/scripts/audit_design_compliance.py \
  --source <PATH_TO_CODE> \
  --knowledge-base knowledge_base/sites/<SITE_SLUG> \
  --output ./INSPECTION_REPORT.md
```

### What it checks automatically:
- Scans every hex color, rgb, hsl, and oklch value in the source code and compares it to `tokens.json`.
- Detects generic Tailwind grays (`bg-gray-900`, `text-slate-400`) that override the local palette.
- Verifies that authentic brand fonts declared in `meta.json` are present in font-family definitions.
- Verifies container constraints (`max-w-*`) and flags sluggish transition durations (>500ms).
- Writes a ready-to-read `INSPECTION_REPORT.md`.

---

## 📋 The 4-Step Manual Inspection Workflow

When performing an in-depth audit or reviewing the automated report:

### Step 1: Load Ground Truth Deliverables
Navigate to `knowledge_base/sites/<site_slug>/` and load:
1. `tokens.json`: The source of truth for colors, border-radii, and shadows.
2. `meta.json`: The source of truth for brand typography and technology stack.
3. `UX_TEARDOWN_REPORT.md`: The source of truth for layout geometry, section hierarchy, and micro-interactions.

### Step 2: Static Code Review Across 5 Dimensions
Evaluate the target code using the [100-Point Audit Rubric](./references/audit_rubric.md):
1. **Color Token Fidelity (30 pts)**: Canvas background (`--background`), card surface (`--surface-card`), hairline border alpha transparency (`rgba(255, 255, 255, 0.08)`).
2. **Typography & Font Identity (20 pts)**: Authentic brand font declared in font stack, monospace code styling, negative headline tracking.
3. **Layout & Skeleton Geometry (20 pts)**: Container width constraint matching teardown, asymmetric Bento grid column spans, mobile collapsing.
4. **Surface Depth & Materials (15 pts)**: Top border gradient illumination mask, backdrop blur, subtle badge styling.
5. **Motion Physics & Accessibility (15 pts)**: Snappy easing curves (`cubic-bezier(0.16, 1, 0.3, 1)`), durations <= 250ms, semantic HTML, and visible focus rings.

### Step 3: Identify & Classify Discrepancies
Compare findings against [Common Drift Anti-Patterns](./references/common_drift_anti_patterns.md):
- **HIGH Severity**: Arbitrary unmapped hex codes, wrong canvas background, missing brand font.
- **MEDIUM Severity**: Generic Tailwind gray classes replacing custom tokens, missing top border highlight.
- **LOW Severity**: Slightly sluggish transition duration, loose headline tracking.

### Step 4: Generate the Inspection Report
Write the final audit to `INSPECTION_REPORT.md` using the [Report Template](./references/report_template.md).
- If score >= 85: Mark as **✅ PASSED**.
- If score < 85: Mark as **❌ FAILED** and provide concrete code patch snippets so the builder agent can immediately heal itself.

---

## 🔄 Closing the Loop: Builder Self-Healing Protocol

When the builder agent receives an inspection report with a score < 85:
1. Read the **"Flagged Discrepancies"** and **"Automated Action Items"** in `INSPECTION_REPORT.md`.
2. Apply the specified token and font corrections to the source file.
3. Re-run `audit_design_compliance.py` to confirm the score rises to >= 85 (Passed).
