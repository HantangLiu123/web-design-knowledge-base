# Design Compliance Inspection Report: [Component/Page Name]

| Audit Metric | Value |
| :--- | :--- |
| **Target Code Path** | `[path/to/component.tsx]` |
| **Reference Knowledge Base** | `knowledge_base/sites/[site_slug]/` |
| **Audit Date** | [YYYY-MM-DD] |
| **Compliance Score** | **[Score] / 100** |
| **Final Decision** | **[✅ PASSED / ⚠️ CONDITIONAL FAIL / ❌ CRITICAL FAIL]** |

---

## 1. Executive Quality Summary
[Brief 2-sentence assessment of whether the code captures the benchmark's visual quality or suffered from generic LLM drift.]

---

## 2. Dimension Score Breakdown

| Dimension | Weight | Score | Evaluation Notes |
| :---: | :---: | :---: | :--- |
| **1. Color Token Fidelity** | 30 pts | [X] / 30 | [Notes on canvas, surface tiers, borders] |
| **2. Typography & Brand Font** | 20 pts | [X] / 20 | [Notes on font-family declaration, tracking] |
| **3. Layout & Skeleton Geometry** | 20 pts | [X] / 20 | [Notes on max-w constraints, grid spans] |
| **4. Surface Depth & Materials** | 15 pts | [X] / 15 | [Notes on top border masks, glassmorphism] |
| **5. Motion Physics & A11y** | 15 pts | [X] / 15 | [Notes on easing curves, focus rings] |
| **TOTAL** | **100 pts** | **[X] / 100** | **[Status]** |

---

## 3. Passed Verification Checks
- [x] Background canvas matches local `--background` variable.
- [x] Container max-width matches teardown geometry (`max-w-6xl`).
- [x] Button elements include interactive hover feedback and active downscale.

---

## 4. Flagged Discrepancies & Required Fixes

| Severity | Category | Line(s) | Discrepancy Found | Actionable Remedy |
| :---: | :--- | :---: | :--- | :--- |
| **HIGH** | Color Drift | L34 | Uses ungrounded hex `#1e1e24` | Replace with `var(--surface-card, #0a0a0a)` |
| **MEDIUM** | Typography | L12 | Missing brand font fallback | Declare `font-['ABC_Favorit',sans-serif]` |
| **LOW** | Motion | L58 | Sluggish `duration-500` | Change to snappy `duration-150` |

---

## 5. Automated Patch Code for Builder Agent
Provide copy-pasteable code patches that the builder agent can immediately apply to resolve all flagged discrepancies:

```tsx
// Apply this patch to resolve flagged discrepancies:
- <div className="bg-[#1e1e24] font-sans">
+ <div className="bg-[var(--surface-card,#0a0a0a)] font-['ABC_Favorit',sans-serif]">
```
