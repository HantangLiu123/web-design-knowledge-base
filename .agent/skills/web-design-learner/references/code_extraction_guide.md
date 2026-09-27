# Code-Level Reverse Engineering & Extraction Guide

This guide details how an agent fetches, inspects, and extracts frontend source code to replicate a website's UI patterns accurately.

## 0. Automated Token Extraction with the Python Crawler

A dedicated zero-dependency script is included in `scripts/extract_design_tokens.py`. It uses only the Python Standard Library (`urllib`, `re`, `html.parser`, `json`), meaning it requires no extra packages.

```powershell
python .agent/skills/web-design-learner/scripts/extract_design_tokens.py https://example.com --output-dir ./scratch/extracted_tokens
```

### What the script automatically produces:
1. **`tokens.json`**:
   - Every CSS custom property (`--*`) mapped to its value.
   - Frequency-ranked color palette (hex, rgba, hsl, oklch).
   - Unique font families extracted from `font-family` declarations and Google Fonts links.
   - Identified border-radii, box-shadows, and `@media` queries.
   - Detected frontend frameworks (Next.js, Tailwind, Radix UI, Framer Motion, etc.).
2. **`extracted_variables.css`**:
   - Clean, consolidated `:root { ... }` block containing all active CSS custom properties.

---

## 1. Inspecting the DOM & Technical Stack

When inspecting a web page's source, check the following signatures:

```markdown
Stack Indicator               | Identified Technologies
------------------------------|---------------------------------------------
`<div id="__next">`           | Next.js (Pages Router)
`<script id="__NEXT_DATA__">` | Next.js server-rendered data
`class="flex flex-col p-4"`   | Tailwind CSS
`class="css-1a2b3c"`          | Emotion / Styled-Components (CSS-in-JS)
`class="Header_root__x9f"`    | CSS Modules
`data-radix-popper-content`   | Radix UI / Shadcn UI primitives
`<canvas data-engine="three">`| Three.js / WebGL
`style="--framer-..."`        | Framer Motion / Framer Sites
```

---

## 2. Extracting Design Tokens

### A. Root CSS Variables
Look inside `<style>` tags or linked `.css` files for `:root` or `html.dark`:

```css
:root {
  /* Surface colors */
  --background: #08090a;
  --surface-subtle: #121316;
  --surface-card: #18191b;
  --surface-overlay: rgba(24, 25, 27, 0.8);

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'Geist Mono', monospace;

  /* Borders & Radius */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-active: rgba(255, 255, 255, 0.2);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
  --shadow-glow: 0 0 20px -5px rgba(120, 119, 198, 0.3);
}
```

### B. Converting Extracted Tokens to Tailwind Configuration
Convert extracted tokens directly into a `tailwind.config.js` extension block:

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#08090a',
        surface: {
          subtle: '#121316',
          card: '#18191b',
        },
        border: {
          subtle: 'rgba(255, 255, 255, 0.08)',
          active: 'rgba(255, 255, 255, 0.2)',
        },
        brand: {
          DEFAULT: '#5e6ad2',
          glow: 'rgba(120, 119, 198, 0.3)',
        }
      },
      borderRadius: {
        sm: '6px',
        md: '10px',
        lg: '16px',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Geist Mono', 'monospace'],
      }
    }
  }
}
```

---

## 3. Extracting Layout Systems

### A. Bento Grid Deconstruction
Modern websites (Vercel, Linear, Apple) make extensive use of asymmetric Bento Grids:

1. Look for the parent grid declaration:
   ```css
   display: grid;
   grid-template-columns: repeat(12, minmax(0, 1fr));
   gap: 1.5rem;
   ```
2. Identify card spans across viewports:
   - Card 1 (Large showcase): `col-span-12 lg:col-span-8 row-span-2`
   - Card 2 (Vertical stat/metric): `col-span-12 lg:col-span-4 row-span-2`
   - Card 3 (Horizontal feature): `col-span-12 lg:col-span-4`
   - Card 4 (Horizontal feature): `col-span-12 lg:col-span-4`
   - Card 5 (Horizontal feature): `col-span-12 lg:col-span-4`

### B. Sticky Multi-Column Layout (Docs & Dashboards)
Look for sticky behavior in navigation or secondary rails:
```css
position: sticky;
top: 4rem;
height: calc(100vh - 4rem);
overflow-y: auto;
```

---

## 4. Extracting Motion, Timing & Easing

Look for transition rules in CSS or motion objects in JavaScript:

1. **Easing Curves**:
   - Linear tech curve: `cubic-bezier(0.16, 1, 0.3, 1)` (instant start, smooth deceleration).
   - Bouncy spring: `cubic-bezier(0.34, 1.56, 0.64, 1)`.
   - Subtle standard: `cubic-bezier(0.4, 0, 0.2, 1)`.
2. **Durations**:
   - Fast state toggles: `150ms`.
   - Card reveals & dropdowns: `250ms` - `300ms`.
   - Modal backdrops & complex layout morphs: `400ms` - `500ms`.
3. **Card Border Shimmer Effect**:
   Extract CSS pseudo-element tricks for card borders:
   ```css
   .card-glow {
     position: relative;
     border-radius: 12px;
     background: #121316;
   }
   .card-glow::before {
     content: '';
     position: absolute;
     inset: -1px;
     border-radius: 13px;
     background: linear-gradient(180deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 100%);
     z-index: -1;
   }
   ```

---

## 5. Cleaning & Porting Component Blueprints

When copying extracted DOM elements into clean component code:
1. **Remove Vendor Bloat**:
   - Strip automated telemetry attributes (`data-analytics`, `data-track-id`, `data-sentry-*`).
   - Remove obfuscated class names (`c10x_1a`) and replace with standard Tailwind or clean CSS classes.
2. **Restore Semantic Structure**:
   - Replace nested `<div>` ladders with semantic tags (`<nav>`, `<header>`, `<main>`, `<article>`, `<aside>`, `<button>`).
3. **Ensure Accessibility**:
   - Ensure buttons have `type="button"`, `aria-label`, and interactive focus rings.
   - Modals must include `role="dialog"`, `aria-modal="true"`, and focus trapping logic.
