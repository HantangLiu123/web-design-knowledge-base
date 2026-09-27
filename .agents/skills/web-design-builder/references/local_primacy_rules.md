# Local Knowledge Base Primacy Rules

This document specifies the strict behavioral rules that govern how the **`web-design-builder`** agent must prioritize local knowledge base data over the generic training weights of the LLM.

---

## 🚫 The Problem: Generic LLM Drift
When an LLM is asked to build a modern UI without grounding, it defaults to:
- Generic Tailwind grays (`bg-gray-900`, `bg-slate-950`).
- Generic system fonts or plain Inter without matching weights or tracking.
- Standard blue/purple gradients (`from-blue-600 to-indigo-600`).
- Oversized generic rounded corners (`rounded-2xl` everywhere).
- Generic box-shadows that look "floaty" rather than crisp.

This results in generic, uninspired websites that do not reflect the benchmark's actual design craftsmanship.

---

## 🛡️ The Primacy Principles

When building UI, the agent must enforce these 5 non-negotiable rules:

### Rule 1: Local CSS Variables Are Absolute
- **Directive**: Every surface, canvas background, text color, and border MUST resolve to an extracted variable from `extracted_variables.css` or `tokens.json`.
- **Wrong**: `className="bg-[#121212] text-white border border-gray-700"`
- **Right**: `className="bg-[var(--background,#000)] text-[var(--text-primary,#fff)] border border-[var(--border-subtle,rgba(255,255,255,0.1))]"`

### Rule 2: Exact Font Identity & Fallbacks
- **Directive**: Check `meta.json` and `tokens.json` for the site's authentic typography.
- If the site uses `ABC Favorit` or `Commit Mono` (e.g. Resend), or `Geist Sans` (Vercel), declare that exact font in the CSS font stack with suitable fallbacks:
  ```css
  font-family: 'ABC Favorit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  ```
- Match the exact letter-spacing (tracking) documented in the teardown (e.g., negative tracking `tracking-tight` on large display headings).

### Rule 3: Precise Hairline Borders, Not Heavy Outlines
- Modern benchmark sites (Linear, Resend, Vercel, Supabase) use **subtle translucent borders**, usually `rgba(255, 255, 255, 0.08)` to `rgba(255, 255, 255, 0.12)`, often accented with a 1px gradient mask.
- **Never** use heavy solid borders like `border-gray-600` or `border-zinc-700`.

### Rule 4: Match Documented Layout Grids
- Check `UX_TEARDOWN_REPORT.md` for container geometry:
  - If the site uses `max-w-6xl` (~1152px), do not arbitrarily use `max-w-7xl` (~1280px) or `max-w-screen-2xl`.
  - If the site uses a 12-column asymmetric Bento Grid, replicate the exact column spans (`col-span-8` + `col-span-4`), rather than a symmetrical 3-column grid.

### Rule 5: Replicate Documented Easing & Physics
- Do not use generic `transition-all duration-300 ease-in-out`.
- Use the target's documented physics:
  - Linear/Resend Snappy Easing: `cubic-bezier(0.16, 1, 0.3, 1)` with `150ms` - `200ms` duration.
  - Hover transforms: Subtle translation (`translateY(-1px)` or `translateY(-2px)`) with border brightness increase.

---

## 🔍 Pre-Generation Grounding Query

Before generating code, the builder agent must mentally or programmatically perform this verification:

```markdown
1. Which directory am I reading? -> knowledge_base/sites/<slug>/
2. What is the primary canvas background? -> Extracted from tokens.json
3. What is the display font and code font? -> Extracted from meta.json
4. What is the signature layout archetype? -> Extracted from UX_TEARDOWN_REPORT.md
5. Am I using any arbitrary hex codes not present in the local tokens? -> If yes, REJECT and replace with local token.
```
