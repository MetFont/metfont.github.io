<script setup>
const CDN_URL = 'https://cdn.jsdelivr.net/gh/MetFont/metfont@latest/site/public/MetFont-glyf.woff2'
const CDN_PINNED = 'https://cdn.jsdelivr.net/gh/MetFont/metfont@v1.0.0/site/public/MetFont-glyf.woff2'
</script>

<template>
  <div class="usage-content">
    <h3 class="usage-subtitle">Web Embedding</h3>

    <!-- CDN Quick Start -->
    <section class="usage-block">
      <h4 class="usage-heading">CDN Quick Start</h4>
      <p class="body-text mb-4">
        MetFont is available via <a href="https://www.jsdelivr.com/" target="_blank" rel="noopener" class="usage-link">jsDelivr</a>,
        a free CDN for open-source projects. No download required &mdash; just reference the font URL directly.
      </p>
      <pre class="usage-code"><code>&lt;!-- CDN via jsDelivr (always latest) --&gt;
&lt;style&gt;
@font-face {
  font-family: 'MetFont';
  src: url('{{ CDN_URL }}') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}
&lt;/style&gt;</code></pre>
      <div class="usage-note">
        <p class="body-text text-xs">
          <strong>Production:</strong> Pin to a specific version for stability:
          <code class="code-inline">{{ CDN_PINNED }}</code>
        </p>
      </div>
    </section>

    <!-- CSS Usage -->
    <section class="usage-block">
      <h4 class="usage-heading">CSS Content Property</h4>
      <p class="body-text mb-4">
        Reference symbols by their Unicode codepoint using CSS <code class="code-inline">content</code>:
      </p>
      <pre class="usage-code"><code>/* Apply the font */
.weather-symbol {
  font-family: 'MetFont', sans-serif;
}

/* Reference specific symbols */
.rain::before              { content: '\E713'; }
.thunderstorm::before      { content: '\E71A'; }
.snow::before              { content: '\E719'; }
.fog::before               { content: '\E71F'; }
.drizzle::before           { content: '\E703'; }
.tropical-cyclone::before  { content: '\E71B'; }
.cloud-high::before        { content: '\E000'; }
.wind-calm::before         { content: '\E600'; }</code></pre>
    </section>

    <!-- HTML Entities -->
    <section class="usage-block">
      <h4 class="usage-heading">HTML Hex Entities</h4>
      <p class="body-text mb-4">
        Use hex entities directly in HTML markup:
      </p>
      <pre class="usage-code"><code>&lt;span style="font-family: MetFont"&gt;&amp;#xE713;&lt;/span&gt;  &lt;!-- Rain --&gt;
&lt;span style="font-family: MetFont"&gt;&amp;#xE71A;&lt;/span&gt;  &lt;!-- Thunderstorm --&gt;
&lt;span style="font-family: MetFont"&gt;&amp;#xE719;&lt;/span&gt;  &lt;!-- Snow --&gt;
&lt;span style="font-family: MetFont"&gt;&amp;#xE71B;&lt;/span&gt;  &lt;!-- Tropical cyclone --&gt;</code></pre>
    </section>

    <!-- JavaScript -->
    <section class="usage-block">
      <h4 class="usage-heading">JavaScript / TypeScript</h4>
      <pre class="usage-code"><code>// Create symbol from codepoint
const rain = String.fromCodePoint(0xE713);
const thunderstorm = String.fromCodePoint(0xE71A);

// Set text content
document.querySelector('.weather').textContent = rain;

// React
&lt;span style="font-family: MetFont"&gt;{String.fromCodePoint(0xE713)}&lt;/span&gt;

// Vue template
&lt;span style="font-family: MetFont"&gt;{{ String.fromCodePoint(0xE713) }}&lt;/span&gt;  &lt;!-- use computed --&gt;</code></pre>
    </section>

    <!-- Self-Hosting -->
    <section class="usage-block">
      <h4 class="usage-heading">Self-Hosting</h4>
      <p class="body-text mb-4">
        For maximum control, download the WOFF2 file and host it yourself:
      </p>
      <pre class="usage-code"><code>@font-face {
  font-family: 'MetFont';
  src: url('/fonts/MetFont-glyf.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}</code></pre>
      <div class="usage-note">
        <p class="body-text text-xs">
          Download the WOFF2 from the <a href="#download" class="usage-link">Download page</a>.
          Place it in your project's <code class="code-inline">public/fonts/</code> directory.
        </p>
      </div>
    </section>

    <!-- Glyph Data -->
    <section class="usage-block">
      <h4 class="usage-heading">Programmatic Lookup</h4>
      <p class="body-text mb-4">
        The full glyph catalog is available as JSON for building UIs:
      </p>
      <pre class="usage-code"><code>// Fetch glyph metadata
const glyphs = await fetch('/glyphs.json').then(r => r.json());

// Each glyph has: unicode, name, category, codepoint
// Example: { unicode: "U+E713", name: "Rain", category: "..." }

// Find symbol by name
const rain = glyphs.find(g => g.name.includes('Rain'));
console.log(rain.unicode); // "U+E713"</code></pre>
    </section>
  </div>
</template>

<style scoped>
.usage-content {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.usage-subtitle {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 1.5rem;
}

.usage-block {
  margin-bottom: 2rem;
}

.usage-heading {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem;
}

.usage-link {
  color: var(--accent);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.usage-code {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-x: auto;
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.usage-code code {
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
}

.code-inline {
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  font-size: 12px;
  padding: 1px 4px;
  border-radius: 3px;
  background: var(--bg-overlay);
}

.usage-note {
  margin-top: 0.75rem;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  background: var(--accent-subtle);
  border: 1px solid var(--accent-muted);
}
</style>
