# UX & UI Teardown: Wired (https://www.wired.com)

## 1. Executive Summary
- **Category**: Editorial, Media & Digital Storytelling (Rank #5)
- **Primary Design Style**: Tech-Forward Magazine Grid / Gear Review Cards
- **Recommended Stack**: React, Webpack, Custom Design System
- **Key Takeaway**: Modern technical magazine layout; high-contrast borders; gear review breakdown cards (Pros/Cons/Specs).

---

## 2. The Five Planes Analysis

### A. Strategy Plane
- **Target Persona**: Professionals, developers, or consumers seeking world-class UI ergonomics in the Editorial, Media & Digital Storytelling space.
- **Conversion Goal**: Drive user acquisition and engagement through Tech-Forward Magazine Grid / Gear Review Cards aesthetics and clear value proposition.
- **Trust Elements**: Customer validation, clean interaction feedback, and brand authority.

### B. Scope Plane
- **Core Interactive Features**: Product review 'The Good / The Bad' cards; pull-quote typography; author byline cards with social links.
- **Key Components**: Pros & Cons Card; Pull-Quote Callout; Byline Card; Review Summary Box

### C. Structure Plane (IA & IxD)
- **Navigation & Flow**: Fluid, responsive navigation hierarchy optimized for rapid scanning and minimal cognitive load.
- **Interaction Feedback**: Snappy state transitions, optimistic UI updates, and subtle micro-interactions.

### D. Skeleton Plane (Layout & Grids)
- **Container Geometry**: Centered responsive container with standard desktop max-width constraints.
- **Layout Rhythm**: Structured grid systems separating high-impact hero zones from modular feature components.

### E. Surface Plane (Sensory & Visuals)
- **Color Palette & Contrast**: 50 extracted colors adhering to Tech-Forward Magazine Grid / Gear Review Cards aesthetics.
- **Typography Hierarchy**: Fonts detected: Apercu, Breve Text, BreveText, LabGrotesque, Proxima Nova.
- **CSS Variables Count**: 639 active variables mapped in `extracted_variables.css`.

---

## 3. Implementation Blueprint for Builder Agents
When imitating this website using `web-design-builder`:
1. Import `extracted_variables.css` into the project root stylesheet.
2. Structure layout following the Pros & Cons Card; Pull-Quote Callout; Byline Card; Review Summary Box archetypes.
3. Apply the documented patterns: *Product review 'The Good / The Bad' cards; pull-quote typography; author byline cards with social links.*.
