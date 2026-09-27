# UX & UI Teardown: Discord (https://discord.com)

## 1. Executive Summary
- **Category**: Community, Educational & Lifestyle (Rank #4)
- **Primary Design Style**: 3-Tier Hierarchy / Voice HUD / Markdown Embeds
- **Recommended Stack**: React, Electron, WebRTC, Flux
- **Key Takeaway**: Definitive community chat layout; 3-column navigation; voice channel status bar; contextual action popovers.

---

## 2. The Five Planes Analysis

### A. Strategy Plane
- **Target Persona**: Professionals, developers, or consumers seeking world-class UI ergonomics in the Community, Educational & Lifestyle space.
- **Conversion Goal**: Drive user acquisition and engagement through 3-Tier Hierarchy / Voice HUD / Markdown Embeds aesthetics and clear value proposition.
- **Trust Elements**: Customer validation, clean interaction feedback, and brand authority.

### B. Scope Plane
- **Core Interactive Features**: 3-tier sidebar hierarchy (Servers -> Channels -> Chat); voice room HUD; contextual message action popovers.
- **Key Components**: Server Rail; Channel Tree; Message Action Popover; Voice Control HUD

### C. Structure Plane (IA & IxD)
- **Navigation & Flow**: Fluid, responsive navigation hierarchy optimized for rapid scanning and minimal cognitive load.
- **Interaction Feedback**: Snappy state transitions, optimistic UI updates, and subtle micro-interactions.

### D. Skeleton Plane (Layout & Grids)
- **Container Geometry**: Centered responsive container with standard desktop max-width constraints.
- **Layout Rhythm**: Structured grid systems separating high-impact hero zones from modular feature components.

### E. Surface Plane (Sensory & Visuals)
- **Color Palette & Contrast**: 50 extracted colors adhering to 3-Tier Hierarchy / Voice HUD / Markdown Embeds aesthetics.
- **Typography Hierarchy**: Fonts detected: ABC Ginto Normal, ABCGintoNormal-Bold, Abcgintodiscord, Abcgintodiscordnord, Abcgintodiscordnord-italic.
- **CSS Variables Count**: 26 active variables mapped in `extracted_variables.css`.

---

## 3. Implementation Blueprint for Builder Agents
When imitating this website using `web-design-builder`:
1. Import `extracted_variables.css` into the project root stylesheet.
2. Structure layout following the Server Rail; Channel Tree; Message Action Popover; Voice Control HUD archetypes.
3. Apply the documented patterns: *3-tier sidebar hierarchy (Servers -> Channels -> Chat); voice room HUD; contextual message action popovers.*.
