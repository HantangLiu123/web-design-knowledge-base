import React, { useState } from 'react';

/**
 * HeroSplitView component imitating Resend (https://resend.com)
 * Built strictly according to knowledge_base/sites/resend/ deliverables.
 *
 * Local Tokens Applied:
 * - Canvas: var(--background, #000000)
 * - Border Subtle: var(--border-subtle, rgba(255, 255, 255, 0.1))
 * - Typography: 'ABC Favorit' (Sans), 'Commit Mono' (Mono)
 * - Motion: 150ms snappy cubic-bezier transition
 */
export const ResendHero: React.FC = () => {
  const [copied, setCopied] = useState(false);

  const codeSnippet = `import { Resend } from 'resend';

const resend = new Resend('re_123456789');

await resend.emails.send({
  from: 'you@example.com',
  to: 'user@gmail.com',
  subject: 'Welcome to the platform',
  react: <WelcomeEmail firstName="Alex" />
});`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(codeSnippet);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative min-h-[600px] w-full bg-[#000000] text-white py-20 px-6 font-['ABC_Favorit',-apple-system,sans-serif]">
      {/* Top ambient glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[200px] bg-gradient-to-b from-white/10 to-transparent blur-[120px] pointer-events-none" />

      <div className="max-w-6xl mx-auto">
        {/* Header Hook */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs font-mono text-white/70 mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>Resend 2.0 is live</span>
          </div>

          <h1 className="text-5xl sm:text-6xl font-bold tracking-tight text-white mb-6">
            Email for developers
          </h1>
          <p className="text-lg text-white/60 leading-relaxed font-normal">
            The best way to reach humans instead of spam folders. Deliver transactional and marketing emails at scale.
          </p>

          <div className="mt-8 flex items-center justify-center gap-4">
            <button
              type="button"
              className="rounded-lg bg-white px-5 py-2.5 text-sm font-medium text-black transition-all hover:bg-white/90 active:scale-[0.98]"
            >
              Get Started
            </button>
            <button
              type="button"
              className="rounded-lg border border-white/10 bg-white/5 px-5 py-2.5 text-sm font-medium text-white/80 transition-all hover:bg-white/10 hover:text-white"
            >
              Documentation
            </button>
          </div>
        </div>

        {/* 2-Column Split: Code on Left, Live Render on Right */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
          {/* Left: Code Pane */}
          <div className="lg:col-span-6 rounded-2xl border border-[var(--border-subtle,rgba(255,255,255,0.1))] bg-[var(--surface-card,#000)] p-6 flex flex-col justify-between shadow-2xl">
            <div>
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-[var(--border-subtle,rgba(255,255,255,0.1))] text-xs font-mono text-[var(--text-muted,#888888)]">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-white/20" />
                  <span>api/send.ts</span>
                </div>
                <button
                  type="button"
                  onClick={copyToClipboard}
                  className="hover:text-white transition-colors"
                >
                  {copied ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <pre className="font-['Commit_Mono',monospace] text-xs leading-relaxed text-[var(--text-primary,#fff)] overflow-x-auto">
                <code>{codeSnippet}</code>
              </pre>
            </div>
            <div className="mt-6 pt-4 border-t border-[var(--border-subtle,rgba(255,255,255,0.1))] flex items-center justify-between text-xs font-mono text-[var(--text-muted,#888888)]">
              <span>TypeScript</span>
              <span>200 OK • 84ms</span>
            </div>
          </div>

          {/* Right: Rendered Email Preview Card */}
          <div className="lg:col-span-6 rounded-2xl border border-[var(--border-subtle,rgba(255,255,255,0.1))] bg-[var(--surface-card,#000)] p-8 flex flex-col justify-center items-center shadow-2xl relative overflow-hidden group">
            {/* Subtle top border illumination */}
            <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />

            <div className="w-full max-w-sm rounded-xl border border-[var(--border-subtle,rgba(255,255,255,0.1))] bg-black/60 p-6 shadow-xl backdrop-blur-md">
              <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center mb-4">
                <span className="text-white text-xs font-bold">R</span>
              </div>
              <h3 className="text-base font-semibold text-white mb-1">
                Welcome to Acme, Alex!
              </h3>
              <p className="text-xs text-[var(--text-muted,#888888)] mb-6 leading-relaxed">
                Thanks for joining us. You are ready to start building your next-gen web applications today.
              </p>
              <button
                type="button"
                className="w-full rounded-md bg-white py-2 text-xs font-semibold text-black transition-colors hover:bg-white/80"
              >
                Go to Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
