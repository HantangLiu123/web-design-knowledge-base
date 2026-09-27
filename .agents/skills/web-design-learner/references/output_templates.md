# Synthesis & Output Templates for UI Deconstruction

When the `web-design-learner` skill analyzes a target website, use these standardized templates to generate conclusions and reusable design assets.

---

## Template 1: UX Teardown Report (`UX_TEARDOWN_REPORT.md`)

```markdown
# UX & UI Teardown: [Website Name] ([URL])

## 1. Executive Summary
- **Primary Design Style**: [e.g., Cyber-Minimalist, Swiss Editorial, Bento Grid, Neumorphic Glow]
- **Target Audience / Persona**: [e.g., Enterprise Developers, Creative Directors, Everyday Shoppers]
- **Key Takeaway**: [1-2 sentences summarizing why this design succeeds]

---

## 2. The Five Planes Analysis

### A. Strategy Plane
- **Business Goal**: [Primary conversion or brand outcome]
- **User Mental Model**: [Expectations and mental models addressed]
- **Trust Elements**: [Certifications, logos, social proof, metrics]

### B. Scope Plane
- **Core Interactive Features**: [List key features, e.g., live demo, calculator, switcher]
- **Content Strategy**: [Typography hierarchy, media formats, micro-copy voice]

### C. Structure Plane (IA & IxD)
- **Navigation Model**: [Sticky header, vertical rail, mega-menu, command palette]
- **User Flow**: [Step-by-step path from first impression to primary CTA]
- **State Feedback**: [Loading, optimistic UI, hover feedback, active states]

### D. Skeleton Plane (Layout & Grids)
- **Layout Architecture**: [Bento grid, 2-column split, multi-rail layout]
- **Container Geometry**: [Max-width, column gutters, padding scales]
- **Scanning Rhythm**: [F-pattern, Z-pattern, or focal hero hierarchy]

### E. Surface Plane (Sensory & Visuals)
- **Palette**: [Primary background, surface layers, brand accents, borders]
- **Typography**: [Display font, body font, monospace font, scale ratio]
- **Motion & Depth**: [Shadow layers, border gradients, cubic-bezier easing curves]

---

## 3. Extracted Design Tokens
[Insert extracted CSS variables or Tailwind extension block]

---

## 4. Reusable Component Blueprint
[Insert cleaned React + Tailwind or HTML+CSS implementation of the signature component]

---

## 5. Adaptation & Imitation Guide
- **What to Adopt**: [Which patterns provide the most value for your own project]
- **What to Adapt/Avoid**: [Anti-patterns, vendor-specific lock-in, or brand trademarks to steer clear of]
```

---

## Template 2: Standalone Design Tokens (`design-tokens.css`)

```css
:root {
  /* Surface Layers */
  --bg-canvas: #090a0f;
  --bg-surface-1: #111318;
  --bg-surface-2: #181b22;
  --bg-surface-3: #222630;
  
  /* Text & Foreground */
  --text-primary: #ffffff;
  --text-secondary: #9496a1;
  --text-muted: #5e606e;

  /* Accent & Action */
  --accent-primary: #5e6ad2;
  --accent-primary-hover: #4f5bbd;
  --accent-glow: rgba(94, 106, 210, 0.25);

  /* Borders & Dividers */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);
  --border-focus: #5e6ad2;

  /* Typography Scale */
  --font-family-display: 'Inter', -apple-system, sans-serif;
  --font-family-body: 'Inter', -apple-system, sans-serif;
  --font-family-mono: 'Geist Mono', monospace;

  --text-display: clamp(2.5rem, 5vw, 4.5rem);
  --text-h1: clamp(2rem, 3.5vw, 3rem);
  --text-h2: clamp(1.5rem, 2.5vw, 2.25rem);
  --text-h3: 1.25rem;
  --text-body: 1rem;
  --text-caption: 0.8125rem;

  /* Radius Scale */
  --radius-xs: 4px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-card: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
  --shadow-popover: 0 10px 30px -4px rgba(0, 0, 0, 0.6);

  /* Motion & Easing */
  --ease-snappy: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 450ms;
}
```

---

## Template 3: Clean Reusable Component Implementation (React + Tailwind)

```tsx
import React from 'react';

interface BentoCardProps {
  badge?: string;
  title: string;
  description: string;
  children?: React.ReactNode;
  className?: string;
}

export const BentoCard: React.FC<BentoCardProps> = ({
  badge,
  title,
  description,
  children,
  className = '',
}) => {
  return (
    <div
      className={`group relative overflow-hidden rounded-2xl border border-white/10 bg-[#111318] p-6 transition-all duration-300 hover:border-white/20 hover:shadow-2xl hover:shadow-indigo-500/10 ${className}`}
    >
      {/* Subtle top border highlight */}
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />

      {badge && (
        <span className="inline-flex items-center rounded-full border border-indigo-500/30 bg-indigo-500/10 px-2.5 py-0.5 text-xs font-medium text-indigo-400">
          {badge}
        </span>
      )}

      <h3 className="mt-3 text-lg font-semibold tracking-tight text-white group-hover:text-indigo-200 transition-colors">
        {title}
      </h3>
      <p className="mt-1.5 text-sm leading-relaxed text-zinc-400">
        {description}
      </p>

      {children && <div className="mt-6">{children}</div>}
    </div>
  );
};
```
