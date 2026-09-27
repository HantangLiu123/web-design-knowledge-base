# UX & UI Teardown: Figma (https://www.figma.com)

## 1. Executive Summary
- **Category**: SaaS & Productivity (Rank #4)
- **Primary Design Style**: High-Contrast Canvas / Multiplayer Workspace
- **Recommended Stack**: WebAssembly, WebGL, React, C++
- **Key Takeaway**: Desktop-grade web application standard; seamless multiplayer cursor presence; modular floating tool panels.

---

## 2. The Five Planes Analysis

### A. Strategy Plane
- **Target Persona**: Professionals, developers, or consumers seeking world-class UI ergonomics in the SaaS & Productivity space.
- **Conversion Goal**: Drive user acquisition and engagement through High-Contrast Canvas / Multiplayer Workspace aesthetics and clear value proposition.
- **Trust Elements**: Customer validation, clean interaction feedback, and brand authority.

### B. Scope Plane
- **Core Interactive Features**: Floating canvas toolbar; collaborative cursor presence with name tags; layered side inspectors; zoom pan canvas.
- **Key Components**: Floating Action Bar; Multiplayer Cursors; Layer Tree; Property Inspector

### C. Structure Plane (IA & IxD)
- **Navigation & Flow**: Fluid, responsive navigation hierarchy optimized for rapid scanning and minimal cognitive load.
- **Interaction Feedback**: Snappy state transitions, optimistic UI updates, and subtle micro-interactions.

### D. Skeleton Plane (Layout & Grids)
- **Container Geometry**: Centered responsive container with standard desktop max-width constraints.
- **Layout Rhythm**: Structured grid systems separating high-impact hero zones from modular feature components.

### E. Surface Plane (Sensory & Visuals)
- **Color Palette & Contrast**: 10 extracted colors adhering to High-Contrast Canvas / Multiplayer Workspace aesthetics.
- **Typography Hierarchy**: Fonts detected: SF Mono, SF Pro Display, figmaMono, figmaMono Fallback, figmaSans.
- **CSS Variables Count**: 114 active variables mapped in `extracted_variables.css`.

---

## 3. Implementation Blueprint for Builder Agents
When imitating this website using `web-design-builder`:
1. Import `extracted_variables.css` into the project root stylesheet.
2. Structure layout following the Floating Action Bar; Multiplayer Cursors; Layer Tree; Property Inspector archetypes.
3. Apply the documented patterns: *Floating canvas toolbar; collaborative cursor presence with name tags; layered side inspectors; zoom pan canvas.*.
