# UX & UI Teardown: Raycast (https://www.raycast.com)

## 1. Executive Summary
- **Category**: SaaS & Productivity (Rank #2)
- **Primary Design Style**: Dark Neumorphic / Developer Glow
- **Recommended Stack**: Next.js, Tailwind CSS, Framer Motion
- **Key Takeaway**: Interactive homepage with live keyboard simulations; crisp custom icon system; spotlight search focus.

---

## 2. The Five Planes Analysis

### A. Strategy Plane
- **Target Persona**: Professionals, developers, or consumers seeking world-class UI ergonomics in the SaaS & Productivity space.
- **Conversion Goal**: Drive user acquisition and engagement through Dark Neumorphic / Developer Glow aesthetics and clear value proposition.
- **Trust Elements**: Customer validation, clean interaction feedback, and brand authority.

### B. Scope Plane
- **Core Interactive Features**: Spotlight launcher UI; interactive manual simulation; extension store grid; hotkey visual badges.
- **Key Components**: Interactive Search Modal; Key Cap Badges; Extension Cards

### C. Structure Plane (IA & IxD)
- **Navigation & Flow**: Fluid, responsive navigation hierarchy optimized for rapid scanning and minimal cognitive load.
- **Interaction Feedback**: Snappy state transitions, optimistic UI updates, and subtle micro-interactions.

### D. Skeleton Plane (Layout & Grids)
- **Container Geometry**: Centered responsive container with standard desktop max-width constraints.
- **Layout Rhythm**: Structured grid systems separating high-impact hero zones from modular feature components.

### E. Surface Plane (Sensory & Visuals)
- **Color Palette & Contrast**: 50 extracted colors adhering to Dark Neumorphic / Developer Glow aesthetics.
- **Typography Hierarchy**: Fonts detected: Apple Color Emoji, Arial, Consolas, Geist Mono, GeistMono.
- **CSS Variables Count**: 113 active variables mapped in `extracted_variables.css`.

---

## 3. Implementation Blueprint for Builder Agents
When imitating this website using `web-design-builder`:
1. Import `extracted_variables.css` into the project root stylesheet.
2. Structure layout following the Interactive Search Modal; Key Cap Badges; Extension Cards archetypes.
3. Apply the documented patterns: *Spotlight launcher UI; interactive manual simulation; extension store grid; hotkey visual badges.*.
