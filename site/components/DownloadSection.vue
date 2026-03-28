<script setup>
const emit = defineEmits(['navigateBack'])

const FONT_FORMATS = [
  {
    id: 'woff2',
    name: 'WOFF2',
    file: 'MetFont-glyf.woff2',
    size: '18 KB',
    description: 'Best for modern web. Compressed with Brotli for the smallest file size. Supported by all modern browsers.',
    bestFor: 'Production websites and web apps',
    icon: 'globe',
  },
  {
    id: 'ttf',
    name: 'TTF',
    file: 'MetFont-glyf.ttf',
    size: '43 KB',
    description: 'TrueType outlines. Universal format supported everywhere. Install on any OS for desktop use.',
    bestFor: 'Desktop apps, documents, local installation',
    icon: 'monitor',
  },
  {
    id: 'colr_ttf',
    name: 'COLRv1 TTF',
    file: 'MetFont-glyf_colr_1.ttf',
    size: '54 KB',
    description: 'Color font with COLRv1 + CPAL tables. Supports layered color glyphs in Chrome, Edge, and other Chromium browsers.',
    bestFor: 'Modern browsers with color emoji support',
    icon: 'palette',
  },
  {
    id: 'svg_ttf',
    name: 'SVG TTF',
    file: 'MetFont-picosvgz.ttf',
    size: '73 KB',
    description: 'Font with embedded SVG table. Provides the highest fidelity rendering in Safari and Firefox.',
    bestFor: 'Maximum rendering fidelity',
    icon: 'pen-tool',
  },
]
</script>

<template>
  <main class="download-page animate-slide-up">
    <div class="download-nav">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center h-12">
          <button @click="emit('navigateBack')" class="btn-icon" aria-label="Back">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
          </button>
          <span class="text-xs font-medium" style="color: var(--text-secondary)">Download</span>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <!-- Hero -->
      <div class="about-hero">
        <h1 class="about-title">Download the Font</h1>
        <p class="about-subtitle">
          Perfect symbols for imperfect weather. Grab MetFont in whatever format
          floats your boat.
        </p>
      </div>

      <!-- Format cards -->
      <section class="download-section">
        <h2 class="about-section-title">Font Formats</h2>
        <div class="format-grid">
          <div v-for="fmt in FONT_FORMATS" :key="fmt.id" class="format-card">
            <div class="format-header">
              <div class="format-icon-wrap">
                <svg class="w-5 h-5" style="color: var(--accent)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <template v-if="fmt.icon === 'globe'">
                    <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 4l-4 4"/><path d="M12 2v10"/>
                  </template>
                  <template v-else-if="fmt.icon === 'shield'">
                    <path d="M12 22s8-4 8-10V5l-8-3v9c0 6 8 10 8 10z"/><path d="M9 9v1M12 9v1M15 9v1"/>
                  </template>
                  <template v-else-if="fmt.icon === 'monitor'">
                    <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
                  </template>
                  <template v-else-if="fmt.icon === 'pen-tool'">
                    <path d="M12 19l7-7 3 3-7 7-3-3 7-7z"/><path d="M18 13l-1.5-7.5L2 2l3 3L13 16.5"/>
                  </template>
                </svg>
              </div>
              <div>
                <div class="format-name">{{ fmt.name }}</div>
                <span class="badge">{{ fmt.size }}</span>
              </div>
            </div>
            <p class="format-desc">{{ fmt.description }}</p>
            <div class="format-use">
              <span class="label-text">Best for</span>
              <span class="format-use-text">{{ fmt.bestFor }}</span>
            </div>
            <a :href="'/' + fmt.file" :download="fmt.file" class="format-download">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
              </svg>
              Download {{ fmt.name }}
            </a>
          </div>
        </div>
      </section>

      <!-- Web Embedding -->
      <section class="download-section">
        <h2 class="about-section-title">Usage: Web Embedding</h2>
        <p class="body-text mb-4">
          Embed MetFont in your website using a CSS
          <code>@font-face</code> declaration. All 541 glyphs live in the
          Unicode Private Use Area (U+E000&ndash;U+E7FF).
        </p>
        <pre class="code-block"><code>/* 1. Declare the font */
@font-face {
  font-family: 'MetFont';
  src: url('MetFont-glyf.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

/* 2. Apply to any element */
.weather-icon {
  font-family: 'MetFont', sans-serif;
}

/* 3. Reference specific symbols by codepoint */
.rain::before      { content: '\E713'; }
.thunderstorm::before { content: '\E71A'; }
.snow::before        { content: '\E719'; }
.fog::before         { content: '\E71F'; }

/* Or use inline styles */
&lt;span style="font-family: MetFont"&gt;&amp;#xE713;&lt;/span&gt;</code></pre>
      </section>

      <!-- HTML & JavaScript -->
      <section class="download-section">
        <h2 class="about-section-title">Usage: HTML &amp; JavaScript</h2>
        <pre class="code-block"><code>&lt;!-- HTML hex entities --&gt;
&lt;span style="font-family: MetFont"&gt;&amp;#xE713;&lt;/span&gt;  &lt;!-- Rain --&gt;
&lt;span style="font-family: MetFont"&gt;&amp;#xE71A;&lt;/span&gt;  &lt;!-- Thunderstorm --&gt;
&lt;span style="font-family: MetFont"&gt;&amp;#xE719;&lt;/span&gt;  &lt;!-- Snow --&gt;

&lt;!-- JavaScript --&gt;
&lt;script&gt;
const rain = String.fromCodePoint(0xE713);
const thunderstorm = String.fromCodePoint(0xE71A);
document.querySelector('.weather').textContent = rain;
&lt;/script&gt;</code></pre>
        <p class="body-text mt-4" style="color: var(--text-tertiary); font-size: 0.875rem;">
          <em>Tip:</em> The full glyph list with codepoints, descriptions, and WMO codes is available in
          <a href="/glyphs.json" style="color: var(--accent)">glyphs.json</a>.
        </p>
      </section>

      <!-- Programming Languages -->
      <section class="download-section">
        <h2 class="about-section-title">Usage: Programming Languages</h2>
        <pre class="code-block"><code>// JavaScript / TypeScript
const symbol = String.fromCodePoint(0xE71A);

// Python
symbol = '\uE71A'

// CSS content property
.weather::before { content: '\E71A'; }

// HTML entity
&amp;#xE71A;

// C / C++
wchar_t ch = 0xE71A;</code></pre>
      </section>

      <!-- Local Installation -->
      <section class="download-section">
        <h2 class="about-section-title">Usage: Local Installation</h2>
        <div class="body-text space-y-3">
          <p>
            <strong style="color: var(--text-primary)">macOS:</strong>
            Double-click the <code>.ttf</code> or <code>.otf</code> file to open in Font Book,
            then click "Install Font".
          </p>
          <p>
            <strong style="color: var(--text-primary)">Windows:</strong>
            Right-click the <code>.ttf</code> file and select "Install", or drag it to
            <code>C:\Windows\Fonts</code>.
          </p>
          <p>
            <strong style="color: var(--text-primary)">Linux:</strong>
            Copy to <code>~/.local/share/fonts/</code> and run <code>fc-cache -f</code>.
          </p>
        </div>
        <div class="install-note">
          <p class="body-text">
            Once installed, the font appears as <strong style="color: var(--text-primary)">"MetFont"</strong>
            in any application's font picker. Use a character map utility (like macOS Character Viewer)
            to browse the PUA range U+E000&ndash;U+E7FF.
          </p>
        </div>
      </section>

      <!-- Understanding PUA -->
      <section class="download-section">
        <h2 class="about-section-title">Understanding Private Use Area (PUA)</h2>
        <div class="body-text space-y-3">
          <p>
            The Unicode standard reserves the range U+E000&ndash;U+F8FF as a
            <strong style="color: var(--text-primary)">Private Use Area</strong> &mdash; a sandbox
            where organizations can assign codepoints for internal use without conflicting
            with official Unicode characters.
          </p>
          <p>
            MetFont uses the subrange <strong style="color: var(--accent)">U+E000&ndash;U+E7FF</strong>
            (541 codepoints) to encode WMO and ICAO meteorological symbols. These characters will
            display correctly only when MetFont is loaded &mdash; other fonts will show
            boxes or question marks.
          </p>
          <p>
            In CSS, always pair <code>font-family: 'MetFont'</code> with the codepoint reference.
            In HTML, use the <code>style</code> attribute or a CSS class that sets the font family.
          </p>
        </div>
      </section>

      <!-- Footer humor -->
      <div class="download-footer">
        <p class="download-humor">
          Because predicting the weather is hard enough. Getting the symbols right shouldn't be.
          Fair-weather fonts for foul-weather professionals.
        </p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.download-page {
  flex: 1;
  background: var(--bg-base);
}

.download-nav {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 64px;
  z-index: 40;
  backdrop-filter: blur(12px);
}

.download-section {
  margin-bottom: 3rem;
}

/* ── Format grid ── */
.format-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

@media (min-width: 768px) {
  .format-grid {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}

.format-card {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.2s;
}

.format-card:hover {
  border-color: var(--border-default);
  box-shadow: var(--shadow-md);
}

.format-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.format-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--accent-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.format-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
}

.format-desc {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-secondary);
  flex: 1;
}

.format-use {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.format-use-text {
  font-size: 12px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  color: var(--text-primary);
}

.format-download {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-md);
  background: var(--accent);
  color: var(--text-inverse);
  text-decoration: none;
  transition: all 0.2s;
  width: 100%;
}

.format-download:hover {
  background: var(--accent-hover);
  box-shadow: var(--shadow-glow);
}

/* ── Code block ── */
.code-block {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-x: auto;
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.code-block code {
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
}

/* ── Install note ── */
.install-note {
  margin-top: 1rem;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  background: var(--accent-subtle);
  border: 1px solid var(--accent-muted);
}

/* ── Footer humor ── */
.download-footer {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px dashed var(--border-subtle);
}

.download-humor {
  font-style: italic;
  color: var(--text-tertiary);
  font-size: 0.875rem;
  text-align: center;
}
</style>
