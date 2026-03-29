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
          An open-source, freely licensed metrology symbol font containing {{ totalGlyphs }} meteorological
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
          <a href="meteorology-oceanography" target="_blank" rel="noopener" class="about-link">OGC MetOcean Domain Working Group</a>
          from <a href="https://wmo.int" target="_blank" rel="noopener" class="about-link">WMO</a>
          and <a href="https://www.icao.int" target="_blank" rel="noopener" class="about-link">ICAO</a> standards, and are documented with code table references, usage in weather reports
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
              <h4 class="text-sm font-semibold" style="color: var(--text-primary)">Path Union &amp; Normalization</h4>
              <p class="body-text text-xs">
                <code>normalize-svg.py</code> uses <code>picosvg</code> to convert strokes to fills,
                bakes transforms into path data, and normalises the viewBox to 0&ndash;72. A second pass
                runs Inkscape's <code>path-combine</code> on every multi-path SVG to merge overlapping
                outlines into a single compound path — preventing holes from rendering as solid fill in the
                final font. Output goes to <code>color/svg/</code>.
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

      <!-- The Logo -->
      <section class="about-section">
        <h2 class="about-section-title">The Logo</h2>

        <div class="logo-showcase">
          <img src="/logo-full.svg" alt="MetFont Logo" class="logo-full-display" />
        </div>

        <p class="body-text mb-4">
          The MetFont logo is not merely a brand mark — it is a compact philosophical statement encoded in
          two meteorological symbols. Its design draws from the transition between
          <strong style="color: var(--text-primary)">Past Weather</strong> and
          <strong style="color: var(--text-primary)">Present Weather</strong>, two of the seven symbol
          categories encoded in the font itself.
        </p>

        <div class="logo-symbols-explainer">
          <div class="logo-symbol-item">
            <div class="logo-symbol-visual">
              <img src="/logo-icon.svg" alt="Past Weather" class="logo-symbol-icon" />
            </div>
            <div class="logo-symbol-info">
              <h4 class="text-sm font-semibold" style="color: var(--text-primary)">Past Weather &mdash; U+E302</h4>
              <p class="body-text text-xs">
                <strong>W1W2 &mdash; Fog or ice deposit</strong> (WMO Code Table 4561). Three horizontal
                bars symbolise the sky being partially or wholly obscured by fog, mist, or ice crystals.
                In the logo this symbol occupies the <em>left</em> position — what was.
              </p>
            </div>
          </div>

          <div class="logo-symbol-arrow">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </div>

          <div class="logo-symbol-item">
            <div class="logo-symbol-visual">
              <div class="logo-clear-sky">
                <svg viewBox="0 0 32 32" class="logo-symbol-icon">
                  <circle cx="11" cy="16" r="7.5" fill="url(#fog-clear-grad)"/>
                  <defs>
                    <linearGradient id="fog-clear-grad" x1="11" y1="8.5" x2="11" y2="23.5" gradientUnits="userSpaceOnUse">
                      <stop offset="0%" stop-color="#4a9eff"/>
                      <stop offset="100%" stop-color="#ef4136"/>
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>
            <div class="logo-symbol-info">
              <h4 class="text-sm font-semibold" style="color: var(--text-primary)">Total Cloud Cover &mdash; U+E027</h4>
              <p class="body-text text-xs">
                <strong>N &mdash; 0 oktas, clear sky</strong> (WMO Code Table 2700). Three horizontal
                bars again — but here they represent the open sky: zero cloud cover, unobstructed
                visibility. In the logo this symbol occupies the <em>right</em> position — what is.
              </p>
            </div>
          </div>
        </div>

        <h3 class="text-base font-semibold mb-2 mt-6" style="color: var(--text-primary)">The Sunrise Metaphor</h3>
        <p class="body-text mb-4">
          The logo arranges its two symbols in the posture of a sunrise over open water. The warm gradient
          of the <em>ring</em> — amber at its base, deepening to crimson at its crown — evokes the first
          light breaking through morning fog. The cool blue of the <em>bars</em> evokes both the sea
          and the clarity that follows after the mist lifts. Light rising above the sea: a universal
          symbol of hope and new beginnings.
        </p>

        <h3 class="text-base font-semibold mb-2" style="color: var(--text-primary)">The Meteorological Message</h3>
        <p class="body-text mb-4">
          Meteorology is, at its core, the study of <em>transformation</em> — of how the atmosphere
          moves from one state to another. Fog does not stay forever; clear skies do not guarantee
          tomorrow's sun. The past (what was observed, recorded, summarised in the W1W2 code) informs
          the present (what is now visible, measurable, reportable in the N okta code). And it is
          from this continuous chain of observation — past flowing into present — that forecasts
          are made, that futures are glimpsed.
        </p>
        <p class="body-text">
          The MetFont logo embodies this truth: <em>the past restrains vision, but scientific
          observation clears the sky.</em> That is the hopeful promise at the heart of weather
          forecasting — and at the heart of this project.
        </p>
      </section>

      <!-- Credits -->
      <section class="about-section">
        <h2 class="about-section-title">Credits &amp; License</h2>
        <div class="body-text space-y-3">
          <p>
            <strong style="color: var(--text-primary)">Symbol sources:</strong>
            WMO and ICAO meteorological symbols, curated by the
            <a href="https://www.ogc.org/groups/meteorology-oceanography-domain-working-group/" target="_blank" rel="noopener" class="about-link">OGC MetOcean Domain Working Group</a>
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

/* ── Credits ── */
.about-humor {
  font-style: italic;
  color: var(--text-tertiary);
  font-size: 0.875rem;
  padding-top: 1rem;
  border-top: 1px dashed var(--border-subtle);
}

/* ── Logo section ── */
.logo-showcase {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.logo-full-display {
  height: 48px;
  width: auto;
  display: block;
}

.logo-symbols-explainer {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.logo-symbol-item {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 200px;
}

.logo-symbol-visual {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.logo-symbol-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  display: block;
}

.logo-symbol-arrow {
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.logo-clear-sky {
  width: 28px;
  height: 28px;
}

.logo-clear-sky svg {
  width: 100%;
  height: 100%;
}

.logo-symbol-info h4 {
  margin-bottom: 4px;
}
</style>
