# Common LLM Drift Anti-Patterns & Automated Remedies

This reference catalogs the most frequent hallucinations and drift anti-patterns that AI agents produce when building frontend interfaces, paired with their exact remedies from the local knowledge base.

---

## Anti-Pattern 1: The "Tailwind Slate/Gray" Default Syndrome

### The Drift
An agent is asked to build a dark mode UI and immediately outputs:
```tsx
// ❌ WRONG: Generic Tailwind defaults
<div className="min-h-screen bg-slate-950 text-slate-100">
  <div className="border border-slate-800 bg-slate-900/50 p-6">
    <p className="text-slate-400">Description...</p>
  </div>
</div>
```
### Why it fails
Linear, Resend, Vercel, and Stripe do NOT use Tailwind's default slate blue-grays. They use either pure obsidian blacks (`#000000`), deep warm graphites (`#08090a`), or custom OKLCH neutral curves.

### The Remedy
```tsx
// ✅ CORRECT: Grounded in local knowledge base variables
<div className="min-h-screen bg-[var(--background,#000)] text-[var(--text-primary,#fff)]">
  <div className="border border-[var(--border-subtle,rgba(255,255,255,0.1))] bg-[var(--surface-card,#0a0a0a)] p-6">
    <p className="text-[var(--text-muted,#888)]">Description...</p>
  </div>
</div>
```

---

## Anti-Pattern 2: The "Missing Brand Font" Amnesia

### The Drift
The agent ignores `meta.json` and writes:
```tsx
// ❌ WRONG: Default generic sans-serif
<h1 className="font-sans text-5xl font-bold">
  Email for developers
</h1>
```

### Why it fails
A website's premium identity comes largely from its typography (e.g., `ABC Favorit` on Resend, `Geist Sans` on Vercel, `Inter` on Linear, `GT America` on Pitchfork). Omitting the brand font makes the page look like a generic school project.

### The Remedy
```tsx
// ✅ CORRECT: Brand font explicitly declared with fallback stack
<h1 className="font-['ABC_Favorit',-apple-system,sans-serif] text-5xl font-bold tracking-tight">
  Email for developers
</h1>
```

---

## Anti-Pattern 3: Heavy Solid Borders Instead of Hairline Gradients

### The Drift
```tsx
// ❌ WRONG: Harsh solid outline
<div className="rounded-xl border-2 border-gray-700 bg-black">
```

### Why it fails
High-end modern tech websites almost never use solid thick borders. They use 1px hairline borders with alpha transparency (e.g. `rgba(255, 255, 255, 0.08)`) and an illuminated gradient mask along the top edge.

### The Remedy
```tsx
// ✅ CORRECT: Hairline border with top gradient illumination
<div className="relative overflow-hidden rounded-xl border border-white/10 bg-[#0a0a0a]">
  <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />
```

---

## Anti-Pattern 4: Sluggish & Linear Transitions

### The Drift
```tsx
// ❌ WRONG: Long, floaty animation
<button className="transition-all duration-500 ease-in-out hover:scale-105">
```

### Why it fails
Modern interactive web tools feel snappy and tactile. 500ms feels laggy to power users.

### The Remedy
```tsx
// ✅ CORRECT: Snappy 150ms transition with slight translate and scale
<button className="transition-all duration-150 ease-[cubic-bezier(0.16,1,0.3,1)] hover:-translate-y-0.5 active:scale-[0.98]">
```
