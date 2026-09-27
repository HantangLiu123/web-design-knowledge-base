---
name: web-design-builder
description: >-
  Builds high-fidelity frontend applications, pages, and UI components by strictly reading
  and imitating reverse-engineered deliverables in the local knowledge base.
  Prioritizes local design tokens, UX teardowns, and benchmark data over generic LLM training defaults.
---

# Web Design Builder: Knowledge-Base Driven UI Engineering Skill

This skill guides an agent in building production-ready frontend interfaces that accurately replicate the visual quality, layout systems, design tokens, and interaction physics of benchmark websites. 

Instead of guessing or relying on generic LLM training data, this skill enforces **Local Knowledge Base Primacy**: the agent must ground every styling and architectural decision in the deliverables produced by the `web-design-learner` skill.

---

## 🔗 The Shared Deliverables Interface

Both `web-design-learner` (the creator) and `web-design-builder` (the consumer) communicate through a standardized directory contract:

```
d:/chris/projects/web-design-knowledge-base/
├── knowledge_base/
│   └── sites/
│       └── <site_slug>/                     <-- PRIMARY INTERFACE CONTRACT
│           ├── meta.json                    <-- Site summary, fonts, stack
│           ├── tokens.json                  <-- Full structured token dump
│           ├── extracted_variables.css      <-- Ready-to-import :root variables
│           ├── UX_TEARDOWN_REPORT.md        <-- Five Planes architectural breakdown
│           └── components/                  <-- Extracted reusable component blueprints
Accessible at either:
- **Master Workspace**: `d:/chris/projects/web-design-knowledge-base/knowledge_base/sites/<site_slug>/`
- **Global Link (All Projects)**: `~/.gemini/config/knowledge_base/sites/<site_slug>/` (or `C:/Users/chris/.gemini/config/knowledge_base/sites/<site_slug>/`)

See [Shared Contract Specification](./references/shared_contract_specification.md) for detailed file schemas.

---

## ⚖️ Core Rule: Local Knowledge Base Primacy

> **CRITICAL DIRECTIVE**: When building frontend interfaces, the local knowledge base is the **Single Source of Truth (SSOT)**. It strictly supersedes generic LLM intuition, default Tailwind color classes, and generic UI templates.

1. **Colors**: NEVER use generic Tailwind grays (`bg-gray-900`, `text-slate-400`) if the local knowledge base defines custom palette variables (e.g. `bg-canvas: #000`, `surface-subtle: #121316`).
2. **Typography**: Always use the exact font family, scale, and tracking documented in `meta.json` or `tokens.json`.
3. **Borders & Radii**: Use the exact alpha transparency (e.g. `rgba(255, 255, 255, 0.08)`) and border-radius steps (`6px`, `10px`, `16px`) from `tokens.json`.
4. **Motion**: Use the exact cubic-bezier easing curves and duration tiers documented in the local teardown report.

Read the complete enforcement protocol: [Local Primacy Rules](./references/local_primacy_rules.md).

---

## 🛠️ The 5-Step Builder Protocol

```
┌────────────────────────┐     ┌────────────────────────┐     ┌────────────────────────┐
│ 1. RESOLVE KNOWLEDGE   │ ──> │ 2. INJECT SYSTEM       │ ──> │ 3. ASSEMBLE SKELETON   │
│    BASE DELIVERABLE    │     │    DESIGN TOKENS       │     │    & GRID LAYOUT       │
└────────────────────────┘     └────────────────────────┘     └────────────────────────┘
                                                                           │
                                                                           ▼
┌────────────────────────┐     ┌────────────────────────┐     ┌────────────────────────┐
│ 5. FIDELITY & TOKEN    │ <── │ 4. IMPLEMENT SURFACE   │ <── │ WIRE INTERACTION       │
│    ALIGNMENT AUDIT     │     │    STYLING & MOTION    │     │ & ACCESSIBILITY        │
└────────────────────────┘     └────────────────────────┘     └────────────────────────┘
```

---

### Step 1: Resolve the Knowledge Base Deliverable

1. **Identify the Target Reference**:
   - Determine which benchmark site or design style the user requested (e.g., "Build a landing page hero like Resend", or "Create a dark cyber-minimalist bento grid like Linear").
2. **Inspect the Local Knowledge Base**:
   - Check `knowledge_base/sites/<site_slug>/` for existing deliverables.
   - If the site is listed in `ui_design_benchmarks.csv` but hasn't been crawled yet, **activate the `web-design-learner` skill first** to generate the required deliverables:
     ```powershell
     python .agent/skills/web-design-learner/scripts/extract_design_tokens.py <URL>
     ```
3. **Read the Specification Files**:
   - Read `knowledge_base/sites/<site_slug>/meta.json` for stack, font, and category context.
   - Read `knowledge_base/sites/<site_slug>/UX_TEARDOWN_REPORT.md` for layout zoning, copy tone, and Five Planes analysis.
   - Read `knowledge_base/sites/<site_slug>/extracted_variables.css` for active CSS variables.

---

### Step 2: Inject Design System Tokens

1. **Global CSS Integration**:
   - Copy or import `extracted_variables.css` into the target project's root stylesheet (`globals.css`, `index.css`).
2. **Tailwind Theme Configuration**:
   - Configure `tailwind.config.js` to extend colors, fonts, and animation utilities using the extracted variables:
     ```javascript
     // Example Tailwind extension mapped directly from local tokens
     module.exports = {
       darkMode: 'class',
       theme: {
         extend: {
           colors: {
             canvas: 'var(--background, #000000)',
             surface: 'var(--surface-card, #111318)',
             border: {
               subtle: 'var(--border-subtle, rgba(255, 255, 255, 0.08))',
             }
           },
           fontFamily: {
             sans: ['var(--font-sans)', 'sans-serif'],
             mono: ['var(--font-mono)', 'monospace'],
           }
         }
       }
     }
     ```

---

### Step 3: Layout & Skeleton Assembly (Reverse Five Planes)

Reconstruct the UI from layout wireframe up to surface:

1. **Container Geometry**:
   - Set max width and gutters matching `UX_TEARDOWN_REPORT.md` (e.g. `max-w-6xl mx-auto px-6`).
2. **Grid & Flow Structure**:
   - For Bento Grids: Set up 12-column CSS Grid (`grid grid-cols-1 md:grid-cols-12 gap-4 lg:gap-6`).
   - For Split Views: Side-by-side flex/grid with equal column weights or code-preview ratios (e.g. 50/50 or 60/40).
   - For Sticky Navbars: `sticky top-0 z-50 backdrop-blur-md border-b border-white/10`.

---

### Step 4: Surface Styling, Micro-Interactions & Accessibility

1. **Visual Surface Depth**:
   - Layer surfaces cleanly (`canvas -> surface-1 -> surface-2`).
   - Apply hairline border masks (`border border-white/10` with gradient highlights).
2. **Motion & Interactivity**:
   - Apply the documented easing curves (`cubic-bezier(0.16, 1, 0.3, 1)`).
   - Add hover transformations (`hover:-translate-y-0.5 transition-all duration-200`).
   - Implement keyframes from `tokens.json` (shimmer, border glow, pulse).
3. **Accessibility (a11y)**:
   - Proper semantic tags (`<header>`, `<main>`, `<section>`, `<nav>`).
   - Accessible focus rings (`focus-visible:ring-2 focus-visible:ring-indigo-500`).
   - ARIA labels on icon-only buttons.

---

### Step 5: Fidelity & Alignment Audit

Before presenting the built component or application to the user, run the [Fidelity Checklist](./references/fidelity_checklist.md):
- [ ] Are background colors mapped directly from `tokens.json`?
- [ ] Is typography using the exact font family and weights from `meta.json`?
- [ ] Are borders using the exact opacity values from the local knowledge base?
- [ ] Is the component free of arbitrary, ungrounded hex codes?
- [ ] Is responsive layout behavior verified on both mobile and desktop viewports?
