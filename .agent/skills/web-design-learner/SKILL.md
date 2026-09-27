---
name: web-design-learner
description: >-
  Systematically fetch, inspect, and reverse-engineer the code and UX architecture of any website.
  Deconstructs design systems across the Five Planes of UX and extracts code-level design tokens,
  layouts, micro-interactions, and component blueprints for imitation in other projects.
---

# Web Design Learner: Reverse-Engineering & UI Imitation Skill

This skill guides an agent through systematically deconstructing any website's user interface, user experience, and underlying frontend code. The goal is to turn any inspirational website into actionable, production-ready design tokens, layout patterns, and component implementations that can be imitated in new projects.

---

## 🔄 The 5-Stage Reverse-Engineering Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. INGEST &     │ ──> │ 2. FIVE PLANES  │ ──> │ 3. CODE-LEVEL   │
│    FETCH        │     │    UX ANALYSIS  │     │    EXTRACTION   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 5. IMITATION &  │ <── │ 4. SYNTHESIS &  │ <── │ COMPONENT       │
│    CODEGEN      │     │    DESIGN TOKENS│     │ DECONSTRUCTION  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Stage 1: Ingestion & Asset Fetching

1. **Target URL Assessment**:
   - Determine whether the target is a static landing page, a content publication, a SaaS application dashboard, or a WebGL experience.
2. **Fetch DOM & Stylesheets**:
   - Retrieve raw HTML/DOM using HTTP tools (`read_url_content`) or browser tools (`read_browser_page`).
   - Identify stylesheet links (`<link rel="stylesheet">`), inline `<style>` tags, and `@import` declarations.
   - Extract bundled script references or modern module chunks to identify frontend frameworks (Next.js, Vite, React, Vue, Svelte, Tailwind, Radix UI, Framer Motion, GSAP, Three.js).
3. **Automated Python Crawler (Recommended for Fast Extraction)**:
   - Run the bundled zero-dependency Python extractor script to crawl stylesheets, extract `:root` CSS variables, color palettes, typography, and layout breakpoints automatically:
     ```powershell
     python .agent/skills/web-design-learner/scripts/extract_design_tokens.py <TARGET_URL> --output-dir ./scratch/extracted_tokens
     ```
   - This automatically parses external CSS files, aggregates CSS custom properties into `extracted_variables.css`, and structures all design tokens into `tokens.json`.
4. **Capture Metadata & Assets**:
   - Favicons, open graph images, web fonts (`<link rel="preload" as="font">` or `@font-face`), inline SVGs, and icon libraries (Lucide, Heroicons, Phosphor, FontAwesome).

---

## Stage 2: The Five Planes UX Deconstruction

Before looking at raw CSS lines, understand **why** the design was built this way using Jesse James Garrett's Five Planes model.

Refer to the detailed guide: [Five Planes Framework Reference](./references/five_planes_framework.md).

1. **Strategy Plane (Why it exists & who it's for)**:
   - What is the business goal (conversion, engagement, developer trust, luxury prestige)?
   - What user mental model does it serve (consumer, enterprise, developer, creator)?
2. **Scope Plane (What features and content are present)**:
   - Feature inventory: Interactive demo, pricing slider, code runner, search palette, video reel.
   - Content types: High-res photography, technical diagrams, animated cards, testimonials.
3. **Structure Plane (Interaction Design & Information Architecture)**:
   - Navigation model: Top sticky nav, vertical sidebar rail, collapsible drawer, breadcrumbs.
   - User flow: How does a user go from hero to value proposition to CTA or sign-up?
   - State feedback: Loading states, optimistic responses, hover reveals, error prompts.
4. **Skeleton Plane (Wireframe & Layout Zoning)**:
   - Layout architecture: Single-column narrative, asymmetric bento grid, 2-column split (e.g., code left, preview right), 3-column docs.
   - Visual hierarchy & scanning paths: F-pattern, Z-pattern, or guided visual anchor points.
5. **Surface Plane (Visual & Sensory Design)**:
   - Color mood, typography pairings, surface textures, elevation layers, motion curves, and micro-copy voice.

---

## Stage 3: Code-Level Technical Extraction

Extract exact, measurable design parameters from the fetched code.

Refer to the complete technical runbook: [Code Extraction Guide](./references/code_extraction_guide.md).

### 1. Design Tokens Extraction
Inspect `:root`, `html`, or CSS class definitions for:
- **Color System**:
  - Background surface tiers (e.g. `bg-primary: #08090a`, `bg-subtle: #121316`, `bg-card: #18191b`).
  - Text hierarchy (`text-primary`, `text-secondary`, `text-muted`).
  - Accent / Brand colors, glowing gradients, border highlight colors.
  - Alpha-channel translucency (`rgba(...)` or `oklch(...)` for glassmorphic layers).
- **Typography Scale**:
  - Primary font family (e.g., Inter, Geist Sans, SF Pro Display, Plus Jakarta Sans, Outfit).
  - Code/Monospace font (e.g., JetBrains Mono, Fira Code, Geist Mono).
  - Scale steps: `font-size`, `line-height`, `letter-spacing` (tracking), `font-weight`.
- **Spacing & Layout Scale**:
  - Grid gutters, container `max-width`, section vertical paddings (`padding-block`), element gaps.
- **Elevation & Depth**:
  - `box-shadow` layers (ambient vs. directional drop shadows).
  - `backdrop-filter: blur(...)` and border alpha blends.
- **Borders & Radii**:
  - Border widths (typically `1px`), subtle contrast borders (`rgba(255, 255, 255, 0.08)`).
  - Corner radii scale (`--radius-sm: 4px`, `--radius-md: 8px`, `--radius-lg: 12px`, `--radius-full: 9999px`).

### 2. Layout & Grid Engineering
- Check if using **CSS Grid** (`grid-template-columns`, `auto-fit`, `auto-fill`, `minmax()`), **Flexbox**, or **Bento Grids**.
- Responsive Breakpoints: Mobile (`<640px`), Tablet (`768px`), Desktop (`1024px`), Wide (`1280px+`).
- Viewport scaling techniques: `clamp(min, preferred, max)` for fluid type and spacing.

### 3. Motion & Animation Physics
- **Timing & Curves**:
  - Durations: micro (100–150ms), standard (200–300ms), expressive (400–600ms).
  - Easing: `cubic-bezier(0.16, 1, 0.3, 1)` (snappy ease-out) or spring approximations.
- **Micro-Interactions**:
  - Hover states: `transform: translateY(-2px)`, scale, border brightness shift, cursor follow.
  - Focus rings: Double rings (`box-shadow: 0 0 0 2px bg, 0 0 0 4px accent`).

---

## Stage 4: Component Deconstruction

Deconstruct the target site into standard reusable component archetypes:

1. **Header / Navbar**:
   - Fixed vs. sticky; glassmorphic background blur; responsive hamburger transition.
2. **Hero Section**:
   - Headline typography; call-to-action button group; visual centerpiece (3D, video, interactive card).
3. **Feature Cards / Bento Grid**:
   - Asymmetric column spans; card hover lighting/shimmer; badge tags.
4. **Interactive Controls**:
   - Buttons (primary, secondary, ghost, magnetic hover).
   - Form inputs (floating labels, dark background inputs, focus glow).
   - Command palettes (`Cmd+K` popover, keyboard shortcut chips).
5. **Footer & Trust Badges**:
   - Multi-column site map, investor/customer logo tickers, copyright & social links.

---

## Stage 5: Synthesis & Standardized Knowledge Base Deliverables

All outputs created by this skill must be stored in the standardized knowledge base interface directory so that downstream builder agents (`web-design-builder`) can locate, read, and implement them without ambiguity:

**Standardized Deliverable Directory**:
`knowledge_base/sites/<site_slug>/` (e.g., `knowledge_base/sites/linear/`, `knowledge_base/sites/resend/`)

Each site folder must contain:
1. **`meta.json`**: Summary descriptor (site name, URL, category, capture date, font families, framework stack).
2. **`tokens.json`**: Full structured tokens file (colors, typography, radii, shadows, media queries).
3. **`extracted_variables.css`**: Consolidated `:root` CSS variables ready for immediate import.
4. **`UX_TEARDOWN_REPORT.md`**: Comprehensive Five Planes analysis, layout rules, and interaction physics.
5. **`components/`**: Cleaned, reusable component blueprints (e.g., `BentoCard.tsx`, `HeroSection.tsx`).

Use the standardized templates in [Output Templates Reference](./references/output_templates.md).

---

## 🎯 Validation Checklist for Agents

Before completing a website design study, verify:
- [ ] Are all color tokens extracted with exact hex/rgba/oklch values?
- [ ] Is the font stack identified with appropriate fallback fonts?
- [ ] Are key animation durations and easing curves documented?
- [ ] Are responsive breakpoint behaviors verified (mobile vs. desktop)?
- [ ] Is the generated code free of hardcoded vendor-specific junk or proprietary tracking scripts?
- [ ] Can another engineer or AI copy the generated component directly into a clean Next.js/Vite project and have it render accurately?
