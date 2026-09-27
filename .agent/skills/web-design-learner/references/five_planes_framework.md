# The Five Planes of UX: Systematic Website Deconstruction Guide

Jesse James Garrett's **Five Planes of UX** provides a conceptual hierarchy for reverse-engineering any website. When analyzing an inspirational website, moving from bottom to top (Strategy to Surface) ensures you don't merely copy superficial aesthetics, but understand the architectural intent that makes the UI successful.

```
       ┌────────────────────────┐
Top    │      5. SURFACE        │  Visual Design, Sensory, Typography, Micro-interactions
       ├────────────────────────┤
       │      4. SKELETON       │  Interface, Navigation, Information Design, Grids
       ├────────────────────────┤
       │      3. STRUCTURE      │  Information Architecture (IA), Interaction Design (IxD)
       ├────────────────────────┤
       │      2. SCOPE          │  Functional Specifications, Content Requirements
       ├────────────────────────┤
Bottom │      1. STRATEGY       │  User Needs, Business Objectives, Brand Personality
       └────────────────────────┘
```

---

## 1. The Strategy Plane (The "Why")

### What to Analyze
- **User Personas & Mental Models**:
  - Who is this site designed for? (e.g., Senior Software Engineers, Creative Directors, Gen-Z Shoppers, Enterprise CFOs)
  - What mental models does it align with? (e.g., Linear appeals to keyboard-centric Vim/Git power users; Stripe appeals to developers seeking trust and precision).
- **Core Value Proposition**:
  - What is the primary hook communicated above the fold?
  - How quickly can a first-time visitor understand what the product does?
- **Brand Personality Attributes**:
  - Tone of voice: Authoritative, playful, minimalist, technical, luxurious, or disruptive?
  - Visual stance: Does it follow mainstream conventions (familiarity) or introduce novel paradigms (differentiation)?

### Questions the Agent Must Answer
1. What single action does this page desperately want the visitor to take? (e.g., `git clone`, `Sign up with Google`, `Buy Now`, `Book Demo`)
2. What psychological trust markers are used? (e.g., customer logos, SOC2 badges, GitHub star counts, press reviews, investor tiers).

---

## 2. The Scope Plane (The "What")

### What to Analyze
- **Feature Set & Functional Scope**:
  - Interactive components: live playgrounds, ROI calculators, theme toggles, search modals, video scrubbers, audio previews.
  - State management: Does the page allow filtering, live state manipulation, or configuration before signing in?
- **Content Requirements**:
  - Media types: 3D WebGL models, MP4/WebM video hero reels, vector SVG illustrations, high-density telemetry charts, editorial photography.
  - Social Proof Scope: Tweets/quotes carousel, metrics callouts ("$10B+ processed"), customer case study cards.

### Questions the Agent Must Answer
1. Which features are functional vs. purely decorative?
2. How is technical or complex product information tiered (progressive disclosure)?

---

## 3. The Structure Plane (The "How It Works")

### What to Analyze
- **Interaction Design (IxD)**:
  - How do interactive components respond to human input?
  - State transitions: Instant optimistic updates vs. skeleton placeholders vs. shimmer spinners.
  - Error and edge handling: Form validation feedback, empty search states, fallback avatars.
- **Information Architecture (IA)**:
  - Navigation hierarchy:
    - Primary nav (sticky, mega-menu, simple links).
    - Secondary nav (anchor links, in-page tabs, subcategory filters).
    - Utility nav (search shortcut, login, theme switch, GitHub link).
  - Page Rhythm & Section Flow:
    - Example sequence: `Hero -> Social Proof -> Core Value Prop -> Deep Feature Dive (Bento Grid) -> Interactive Demo -> Pricing/Testimonials -> Final CTA -> Multi-column Footer`.

### Questions the Agent Must Answer
1. How does the user navigate between high-level overviews and fine-grained details?
2. What interaction conventions are innovated on, and what standard conventions are kept intact?

---

## 4. The Skeleton Plane (The "Where Things Go")

### What to Analyze
- **Layout Architecture & Grids**:
  - Screen zoning: Header, Hero, Main Content Rails, Sticky Aside / Table of Contents, Footer.
  - Grid rhythm: 12-column grid, modular Bento grid, 3-column sticky documentation, or full-width fluid canvas.
- **Visual Scanning Paths**:
  - F-pattern layouts (reading dense documentation).
  - Z-pattern layouts (marketing landing pages with alternating text and imagery).
  - Center-weighted focal layouts (single-input AI tools like Perplexity or ChatGPT).
- **Component Placement & Proximity**:
  - Proximity rules: How closely are badges, headlines, sub-copy, and CTA buttons clustered?
  - Whitespace / Breathing Room: Tight and dense (GitHub, Linear) vs. expansive and luxurious (Apple, Aesop, Kinfolk).

### Questions the Agent Must Answer
1. What is the container width constraint? (e.g., `max-w-7xl` ~1280px, `max-w-5xl` ~1024px, or full fluid `100vw`).
2. Where are the primary visual anchor points that guide the eye downward?

---

## 5. The Surface Plane (The "How It Looks & Feels")

### What to Analyze
- **Visual Hierarchy & Weight**:
  - Scale contrast: Ratio between `H1` (e.g., 64px–80px) and `body` (15px–17px).
  - Font weight layering: ExtraBold headlines -> Medium subheadings -> Regular body -> Monospace labels.
- **Color Temperature & Palette**:
  - Base canvas: Pure black (`#000000`), deep graphite (`#090a0f`), warm ivory (`#fcfbf9`), clean sterile white (`#ffffff`).
  - Accent roles: Primary CTA color, secondary hover color, success/warning semantic colors.
  - Depth indicators: Multiple dark surface tiers (`surface-1`, `surface-2`, `surface-3`) creating elevation without harsh drop shadows.
- **Texture, Materials & Borders**:
  - Hairline borders: `1px solid rgba(255, 255, 255, 0.08)`.
  - Frosted glass: `backdrop-filter: blur(12px)` + translucent backgrounds.
  - Noise / Grain overlays: Subtle SVG noise texture for physical warmth.
- **Motion Physics & Micro-Sensory Experience**:
  - Hover feedback: Button scale `1.02`, magnetic button pull, subtle border glow shift.
  - Page scroll physics: Smooth inertia scroll, sticky element unpinning, scrubbed animations.

---

## 📋 Five Planes Summary Matrix for Site Teardowns

When reporting your analysis, summarize findings into this matrix:

| Plane | Core Focus | Key Questions Answered | Deliverable Output |
| :--- | :--- | :--- | :--- |
| **Strategy** | Purpose & User | Who is this for? What is the conversion goal? | Strategy Profile & Persona Map |
| **Scope** | Features & Content | What interactive modules and content are required? | Feature & Content Inventory |
| **Structure** | IA & IxD | How does the user traverse the experience? | Section Flow & State Diagram |
| **Skeleton** | Layout & Wireframe | Where are elements arranged on screen? | Wireframe & Grid Geometry Specs |
| **Surface** | Visuals & Motion | What colors, fonts, borders, and animations are used? | Design Tokens & Component Code |
