# 100-Point Design Compliance Scoring Rubric

The **`web-design-inspector`** skill uses this quantitative 100-point rubric to evaluate whether a builder agent adhered to the local knowledge base or suffered from generic LLM drift.

---

## 🎯 Summary Scoring Scale

| Score Range | Status | Assessment & Required Action |
| :---: | :---: | :--- |
| **95 – 100** | 🌟 **Exemplary** | Perfect token fidelity, exact brand font integration, flawless responsive grid. Ready for immediate production. |
| **85 – 94** | ✅ **Passed** | High fidelity with minor cosmetic discrepancies (e.g. minor transition duration differences). Acceptable. |
| **70 – 84** | ⚠️ **Conditional Fail** | Noticeable drift: arbitrary hex colors or generic Tailwind grays detected. Builder agent must run 1 repair cycle. |
| **< 70** | ❌ **Critical Fail** | Severe hallucination: generic LLM template used with zero grounding in local knowledge base. Full rebuild required. |

---

## 📊 Detailed Dimension Breakdown

### Dimension 1: Color Token Fidelity (30 Points Max)
- **Background & Canvas (10 pts)**:
  - Exact match to `--background` or extracted canvas color (e.g. `#000000` for Resend, `#08090a` for Linear).
  - *Deduction: -10 pts if generic `bg-gray-900` or arbitrary `#1a1a1a` is used.*
- **Surface Elevation Layers (10 pts)**:
  - Proper use of `--surface-card` or local secondary dark tiers rather than flat uniform backgrounds.
  - *Deduction: -5 pts for missing card surface contrast.*
- **Hairline Border Transparency (10 pts)**:
  - Translucent border values matching `tokens.json` (`rgba(255, 255, 255, 0.08)` to `0.12`).
  - *Deduction: -5 pts for solid gray borders (`border-gray-700`).*
  - *Deduction: -5 pts for arbitrary ungrounded hex borders.*

---

### Dimension 2: Typography & Brand Font Identity (20 Points Max)
- **Authentic Font Family Declaration (10 pts)**:
  - Brand font documented in `meta.json` (e.g., `ABC Favorit`, `Commit Mono`, `Geist`) declared in CSS/Tailwind with appropriate fallbacks.
  - *Deduction: -10 pts if generic `font-sans` or Arial is used without the brand font.*
- **Monospace Code & Badge Styling (5 pts)**:
  - Code blocks, pills, and hotkey chips styled with the benchmark's monospace font.
  - *Deduction: -5 pts for unstyled browser default monospace.*
- **Headline Tracking & Weight Contrast (5 pts)**:
  - Negative tracking (`tracking-tight`) applied to large display text.
  - *Deduction: -3 pts for loose or unadjusted display headline tracking.*

---

### Dimension 3: Layout Geometry & Skeleton Structure (20 Points Max)
- **Container Max-Width Constraints (10 pts)**:
  - Container width matches the UX teardown specification (e.g., `max-w-6xl` ~1152px vs `max-w-7xl` ~1280px).
  - *Deduction: -5 pts for unconstrained full-width stretch or arbitrary max-widths.*
- **Grid Architecture & Asymmetric Spans (10 pts)**:
  - Bento grids use the documented column/row spans rather than generic symmetric cards.
  - *Deduction: -5 pts for converting an asymmetric Bento layout into a flat 3x3 grid.*
  - *Deduction: -5 pts for missing mobile breakpoint responsiveness (`grid-cols-1 md:grid-cols-12`).*

---

### Dimension 4: Surface Materials, Borders & Depth (15 Points Max)
- **Top Border Highlight Mask (5 pts)**:
  - Benchmark signature 1px gradient mask on card tops (`bg-gradient-to-r from-transparent via-white/20 to-transparent`).
  - *Deduction: -3 pts for missing subtle card top highlight.*
- **Backdrop Blur & Glassmorphism (5 pts)**:
  - Sticky navbars or floating cards use `backdrop-blur-md` and alpha-blended backgrounds.
  - *Deduction: -3 pts for opaque solid headers where frosted glass was specified.*
- **Tag & Badge Accents (5 pts)**:
  - Subtle status pills with translucent backgrounds (e.g. `bg-emerald-500/10 border-emerald-500/20 text-emerald-400`).
  - *Deduction: -3 pts for heavy solid badges.*

---

### Dimension 5: Motion Physics & Accessibility (15 Points Max)
- **Snappy Easing & Duration (8 pts)**:
  - Micro-interactions use durations <= 250ms with `cubic-bezier(0.16, 1, 0.3, 1)` or snappy ease-out curves.
  - *Deduction: -5 pts for sluggish transitions (>500ms or generic `ease-in-out`).*
- **Accessibility & Focus Rings (7 pts)**:
  - Semantic HTML tags (`<header>`, `<main>`, `<button>`).
  - Keyboard accessible focus indicators (`focus-visible:ring-2`).
  - *Deduction: -4 pts for clickable `<div>` elements without role/tabindex.*
  - *Deduction: -3 pts for missing focus rings.*
