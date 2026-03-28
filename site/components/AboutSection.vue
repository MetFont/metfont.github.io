<script setup>
import { computed } from 'vue'

const props = defineProps({
  totalGlyphs: { type: Number, default: 0 },
  categories: { type: Array, default: () => [] },
  planeInfo: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['navigateBack', 'navigatePlane'])

const categoryList = computed(() => {
  return props.categories.filter(c => c.name !== 'all')
})

// Map category name to plane slug
const CATEGORY_PLANE_MAP = {
  'CH_CloudHigh': 'sky-cloud', 'CL_CloudLow': 'sky-cloud', 'CM_CloudMedium': 'sky-cloud',
  'C_CloudGenus': 'sky-cloud', 'N_TotalCloudCover': 'sky-cloud',
  'ww_PresentWeather': 'present-weather', 'wawa_PresentWeatherAutomaticStation': 'present-weather',
  'w1w1_PresentWeatherAdditional': 'present-weather',
  'W1W2_PastWeather': 'past-weather', 'Wa1Wa2_PastWeatherAutomaticStation': 'past-weather',
  'E_StateOfGround': 'state-of-ground', 'Eprime_StateOfGround': 'state-of-ground',
  'a_PressureTendencyCharacteristic': 'pressure', 'PressureCentres': 'pressure',
  'ddff_WindArrows': 'wind-ocean', 'dw1dw1_SwellDirection': 'wind-ocean', 'Ds_ShipDirection': 'wind-ocean',
  'ICAO_SigWx': 'significant-weather', 'Ft_Fronts': 'significant-weather',
}

function getPlaneSlug(catName) {
  return CATEGORY_PLANE_MAP[catName] || null
}

// Build unique plane list from categories
const planeList = computed(() => {
  const seen = new Map()
  for (const cat of categoryList.value) {
    const slug = getPlaneSlug(cat.name)
    if (slug && !seen.has(slug)) {
      seen.set(slug, props.planeInfo[slug] || null)
    }
  }
  return Array.from(seen.entries()).map(([slug, info]) => ({
    slug,
    name: info?.name || slug,
    count: info?.count || 0,
    range: info?.range || [],
    description: info?.description || '',
    blockStart: info?.blockStart || 0,
  })).sort((a, b) => a.blockStart - b.blockStart)
})
</script>

<template>
  <main class="about-page animate-slide-up">
    <!-- Back nav -->
    <div class="about-nav">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center h-12">
          <button @click="emit('navigateBack')" class="btn-icon" aria-label="Back to grid">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
          </button>
          <span class="text-xs font-medium" style="color: var(--text-secondary)">About</span>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <!-- Hero -->
      <div class="about-hero">
        <h1 class="about-title">About MetFont</h1>
        <p class="about-subtitle">
          An open-source, freely licensed symbol font containing {{ totalGlyphs }} meteorological
          symbols from WMO and ICAO standards. Accurate symbols for accurate weather.
        </p>
      </div>

      <!-- What is this site -->
      <section class="about-section">
        <h2 class="about-section-title">What is MetFont?</h2>
        <p class="body-text mb-4">
          MetFont is a <strong style="color: var(--text-primary)">free and open-source</strong>
          symbol font that maps {{ totalGlyphs }} meteorological symbols to the
          <strong style="color: var(--text-primary)">Unicode Private Use Area</strong>
          (U+E000&ndash;U+E7FF). The symbols were curated by the
          <a href="https://www.ogc.org/about/working-groups/metocean-domain-working-group" target="_blank" rel="noopener" class="about-link">OGC MetOcean Domain Working Group</a>
          from <a href="https://public.wmo.int" target="_blank" rel="noopener" class="about-link">WMO</a>
          and ICAO standards, and are documented with code table references, usage in weather reports
          (SYNOP, METAR, TAF, SIGWX), and the publications where they are defined.
        </p>
        <p class="body-text">
          Organized into 7 semantic blocks by WMO category, MetFont works in any application
          that supports OpenType, TrueType, or WOFF2 web fonts. Download it, install it, embed it &mdash;
          no rain checks required. Licensed under
          <a href="https://creativecommons.org/licenses/by/3.0/" target="_blank" rel="noopener" class="about-link">CC BY 3.0</a>.
        </p>
      </section>

      <!-- Font specs -->
      <section class="about-section">
        <h2 class="about-section-title">Font Specifications</h2>
        <div class="specs-grid">
          <div class="spec-tile">
            <span class="label-text">Unicode Range</span>
            <span class="spec-value">U+E000 &ndash; U+E7FF</span>
          </div>
          <div class="spec-tile">
            <span class="label-text">Glyph Count</span>
            <span class="spec-value">{{ totalGlyphs }}</span>
          </div>
          <div class="spec-tile">
            <span class="label-text">Em Size</span>
            <span class="spec-value">1024 units</span>
          </div>
          <div class="spec-tile">
            <span class="label-text">Ascent / Descent</span>
            <span class="spec-value">1320 / 0</span>
          </div>
          <div class="spec-tile">
            <span class="label-text">USE_TYPO_METRICS</span>
            <span class="spec-value">Yes</span>
          </div>
          <div class="spec-tile">
            <span class="label-text">Formats</span>
            <span class="spec-value">glyf &middot; COLRv1 &middot; SVG &middot; WOFF2</span>
          </div>
          <div class="spec-tile">
            <span class="label-text">License</span>
            <span class="spec-value">CC BY 3.0</span>
          </div>
          <div class="spec-tile">
            <span class="label-text">Source</span>
            <span class="spec-value">WMO-No. 485</span>
          </div>
        </div>
      </section>

      <!-- Symbol Categories (planes) -->
      <section class="about-section">
        <h2 class="about-section-title">Symbol Categories</h2>
        <p class="body-text mb-4">
          The {{ totalGlyphs }} symbols are organized into {{ planeList.length }} categories based on
          WMO observation codes and reporting standards. Each category page documents what the symbols mean,
          WMO code tables, and how they are used in practice.
        </p>
        <div class="category-table">
          <div
            v-for="plane in planeList"
            :key="plane.slug"
            class="category-row-item category-row-clickable"
            @click="emit('navigatePlane', plane.slug)"
          >
            <div class="category-row-info">
              <span class="body-text text-sm font-medium">{{ plane.name }}</span>
              <span v-if="plane.description" class="category-desc">{{ plane.description.slice(0, 100) }}{{ plane.description.length > 100 ? '...' : '' }}</span>
            </div>
            <div class="category-row-meta">
              <span v-if="plane.range.length === 2" class="code-text text-xs">{{ plane.range[0] }}</span>
              <span class="code-text">{{ plane.count }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Pipeline -->
      <section class="about-section">
        <h2 class="about-section-title">Build Pipeline</h2>
        <p class="body-text mb-4">
          MetFont is built from authoritative WMO and ICAO SVG symbols through a multi-stage pipeline:
        </p>
        <div class="pipeline-steps">
          <div class="pipeline-step">
            <div class="pipeline-number">1</div>
            <div>
              <h4 class="text-sm font-semibold" style="color: var(--text-primary)">Source Symbols</h4>
              <p class="body-text text-xs">
                Authoritative SVGs from WMO with full Dublin Core metadata, RDF licensing, and descriptive
                <code>&lt;title&gt;</code> and <code>&lt;desc&gt;</code> elements in <code>symbols/</code>.
              </p>
            </div>
          </div>
          <div class="pipeline-step">
            <div class="pipeline-number">2</div>
            <div>
              <h4 class="text-sm font-semibold" style="color: var(--text-primary)">Font-Ready Icons</h4>
              <p class="body-text text-xs">
                Simplified SVGs in <code>icons/</code> with centered viewBox and clean paths suitable for
                font outline import.
              </p>
            </div>
          </div>
          <div class="pipeline-step">
            <div class="pipeline-number">3</div>
            <div>
              <h4 class="text-sm font-semibold" style="color: var(--text-primary)">Stripped SVGs</h4>
              <p class="body-text text-xs">
                Inkscape processes <code>icons/</code> to ungroup elements, convert strokes to paths, union
                overlapping shapes, and export to <code>icons-stripped/</code>. FontForge silently drops
                stroked elements, making this step mandatory.
              </p>
            </div>
          </div>
          <div class="pipeline-step">
            <div class="pipeline-number">4</div>
            <div>
              <h4 class="text-sm font-semibold" style="color: var(--text-primary)">Font Compilation</h4>
              <p class="body-text text-xs">
                <code>nanoemoji</code> (Google's font compiler) processes SVG sources with
                <code>picosvg</code> for stroke-to-fill conversion, producing
                <code>MetFont-glyf.ttf</code>, <code>MetFont-glyf_colr_1.ttf</code>,
                and <code>MetFont-picosvgz.ttf</code> with WOFF2 compression.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Usage -->
      <section class="about-section">
        <h2 class="about-section-title">Usage</h2>
        <p class="body-text mb-4">
          Embed MetFont in your application using a standard CSS <code>@font-face</code> declaration:
        </p>
        <pre class="about-code"><code>@font-face {
  font-family: 'MetFont';
  src: url('MetFont-glyf.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}

.weather-symbol {
  font-family: 'MetFont', sans-serif;
}

/* Reference a specific symbol by Unicode codepoint */
.cloud-symbol::before {
  content: '\E000';
}</code></pre>
      </section>

      <!-- Credits -->
      <section class="about-section">
        <h2 class="about-section-title">Credits &amp; License</h2>
        <div class="body-text space-y-3">
          <p>
            <strong style="color: var(--text-primary)">Symbol sources:</strong>
            WMO and ICAO meteorological symbols, curated by the
            <a href="https://www.ogc.org/about/working-groups/metocean-domain-working-group" target="_blank" rel="noopener" class="about-link">OGC MetOcean Domain Working Group</a>
            from WMO Commission for Basic Systems (CBS) standards documented in
            <em>WMO-No. 485 &mdash; Manual on Codes</em> and ICAO Annex 3 / WMO-No. 49.
          </p>
          <p>
            <strong style="color: var(--text-primary)">Font &amp; site:</strong>
            Built and maintained by
            <a href="https://www.ribose.com" target="_blank" rel="noopener" class="about-link">Ribose</a>.
            Open-source and freely available under
            <a href="https://creativecommons.org/licenses/by/3.0/" target="_blank" rel="noopener" class="about-link">
              Creative Commons Attribution 3.0 (CC BY 3.0)
            </a>.
          </p>
          <p class="about-humor">
            The weather cooled and it all happened.
          </p>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.about-page {
  flex: 1;
  background: var(--bg-base);
}

.about-nav {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 64px;
  z-index: 40;
  backdrop-filter: blur(12px);
}

.about-hero {
  margin-bottom: 3rem;
}

.about-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.1;
  margin-bottom: 1rem;
}

@media (min-width: 640px) {
  .about-title {
    font-size: 2.5rem;
  }
}

.about-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 40rem;
}

.about-section {
  margin-bottom: 3rem;
}

.about-section-title {
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-subtle);
}

.about-link {
  color: var(--accent);
  text-decoration: underline;
  text-underline-offset: 2px;
  transition: color 0.15s;
}

.about-link:hover {
  color: var(--accent-hover);
}

/* ── Specs grid ── */
.specs-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

@media (min-width: 640px) {
  .specs-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.spec-tile {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.spec-value {
  font-size: 13px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  color: var(--text-primary);
}

/* ── Category table ── */
.category-table {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.category-row-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-bottom: 1px solid var(--border-subtle);
  transition: background 0.15s;
}

.category-row-item:last-child {
  border-bottom: none;
}

.category-row-item:hover {
  background: var(--accent-subtle);
}

.category-row-clickable {
  cursor: pointer;
}

.category-row-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.category-row-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.category-desc {
  font-size: 12px;
  color: var(--text-tertiary);
  line-height: 1.4;
}

/* ── Pipeline ── */
.pipeline-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pipeline-step {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.pipeline-number {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--accent-muted);
  color: var(--accent);
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── Code block ── */
.about-code {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-x: auto;
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.about-code code {
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
}

.about-humor {
  font-style: italic;
  color: var(--text-tertiary);
  font-size: 0.875rem;
  padding-top: 1rem;
  border-top: 1px dashed var(--border-subtle);
}
</style>
