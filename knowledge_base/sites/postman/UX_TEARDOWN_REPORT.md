# UX & UI Teardown: Postman (https://www.postman.com)

## 1. Executive Summary
- **Category**: Developer Tools & Infrastructure (Rank #10)
- **Primary Design Style**: Heavy Multi-Tab Workspace / JSON Inspector
- **Recommended Stack**: React, Redux, Custom Webpack/DOM Components
- **Key Takeaway**: Complex desktop-grade API client on the web; multi-tab request builder; collapsible JSON response viewer.

---

## 2. The Five Planes Analysis

### A. Strategy Plane
- **Target Persona**: Professionals, developers, or consumers seeking world-class UI ergonomics in the Developer Tools & Infrastructure space.
- **Conversion Goal**: Drive user acquisition and engagement through Heavy Multi-Tab Workspace / JSON Inspector aesthetics and clear value proposition.
- **Trust Elements**: Customer validation, clean interaction feedback, and brand authority.

### B. Scope Plane
- **Core Interactive Features**: Tabbed request workspace; collapsible JSON tree inspector; environment variable dropdowns; mock server builder.
- **Key Components**: Tabbed Request Bar; JSON Syntax Fold Viewer; Environment Dropdown

### C. Structure Plane (IA & IxD)
- **Navigation & Flow**: Fluid, responsive navigation hierarchy optimized for rapid scanning and minimal cognitive load.
- **Interaction Feedback**: Snappy state transitions, optimistic UI updates, and subtle micro-interactions.

### D. Skeleton Plane (Layout & Grids)
- **Container Geometry**: Centered responsive container with standard desktop max-width constraints.
- **Layout Rhythm**: Structured grid systems separating high-impact hero zones from modular feature components.

### E. Surface Plane (Sensory & Visuals)
- **Color Palette & Contrast**: 50 extracted colors adhering to Heavy Multi-Tab Workspace / JSON Inspector aesthetics.
- **Typography Hierarchy**: Fonts detected: -apple-system, Apple Color Emoji, Arial, BlinkMacSystemFont, Consolas.
- **CSS Variables Count**: 376 active variables mapped in `extracted_variables.css`.

---

## 3. Implementation Blueprint for Builder Agents
When imitating this website using `web-design-builder`:
1. Import `extracted_variables.css` into the project root stylesheet.
2. Structure layout following the Tabbed Request Bar; JSON Syntax Fold Viewer; Environment Dropdown archetypes.
3. Apply the documented patterns: *Tabbed request workspace; collapsible JSON tree inspector; environment variable dropdowns; mock server builder.*.
