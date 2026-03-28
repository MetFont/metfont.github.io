<script setup>
function getChar(unicode) {
  return String.fromCodePoint(parseInt(unicode.replace('U+', ''), 16))
}

const HERO_GLYPHS = [
  { code: 'U+E713', label: 'Rain' },
  { code: 'U+E71A', label: 'Thunderstorm' },
  { code: 'U+E719', label: 'Snow' },
  { code: 'U+E71F', label: 'Fog' },
  { code: 'U+E703', label: 'Drizzle' },
  { code: 'U+E71B', label: 'Tropical Cyclone' },
]

defineEmits(['browse', 'viewGrid', 'viewAbout', 'viewDownload'])
</script>

<template>
  <section class="hero-section">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
      <div class="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">

        <!-- ── Left: Editorial content ── -->
        <div class="animate-slide-up">
          <div class="label-text mb-3">Open Source &middot; Unicode PUA &middot; CC BY 3.0</div>
          <h1 class="heading-display mb-2">
            <img src="/logo-full.svg" alt="MetFont" class="hero-logo-img" />
          </h1>
          <p class="hero-tagline mb-4">Trusted Symbols for Accurate Weather</p>
          <p class="hero-subtitle mb-4">From WMO, ICAO, OGC</p>

          <!-- Partner / standards logos — institutional backing -->
          <div class="hero-partners">
            <span class="hero-partners-label">SOURCES: </span>
            <div class="hero-partners-logos">
              <img src="/logo-wmo.svg" alt="WMO — World Meteorological Organization" class="hero-partner-logo" />
              <img src="/logo-icao.svg" alt="ICAO — International Civil Aviation Organization" class="hero-partner-logo" />
              <img src="/logo-ogc.svg" alt="OGC — Open Geospatial Consortium" class="hero-partner-logo" />
            </div>
          </div>

          <div class="flex flex-wrap gap-2 mb-8">
            <span class="badge">SYNOP</span>
            <span class="badge">METAR</span>
            <span class="badge">TAF</span>
            <span class="badge">SIGWX</span>
            <span class="badge">Marine</span>
            <span class="badge-amber">Font &middot; Reference</span>
          </div>
          <div class="flex flex-col sm:flex-row gap-3">
            <button @click="$emit('browse')" class="btn-primary">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              Browse Symbols
            </button>
            <button @click="$emit('viewDownload')" class="btn-primary">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
              Download Font
            </button>
            <button @click="$emit('viewAbout')" class="btn-ghost">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
              About
            </button>
          </div>
        </div>

        <!-- ── Right: Hero illustration — glyphs + standards ── -->
        <div class="hidden lg:flex flex-col items-center justify-center gap-8 animate-fade-in stagger-2">

          <!-- Live glyph preview — the hero illustration -->
          <div class="hero-preview-grid">
            <div v-for="(glyph, i) in HERO_GLYPHS" :key="glyph.code"
              class="hero-glyph-cell" :style="{ animationDelay: (i * 0.08) + 's' }">
              <span class="hero-glyph-char">{{ getChar(glyph.code) }}</span>
            </div>
          </div>

          <!-- Metrics strip -->
          <div class="hero-metrics">
            <div class="flex items-center gap-2">
              <div class="w-3 h-px rounded" style="background: var(--em-stroke)"></div>
              <span class="text-xs" style="color: var(--text-tertiary)">Em box</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-3 h-px rounded" style="background: var(--baseline-stroke)"></div>
              <span class="text-xs" style="color: var(--text-tertiary)">Baseline</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-3 h-px rounded" style="background: var(--advance-stroke)"></div>
              <span class="text-xs" style="color: var(--text-tertiary)">Advance</span>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* ── Hero layout ── */
.hero-section {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: relative;
  overflow: hidden;
}

.hero-section > div {
  position: relative;
  z-index: 1;
}

/* ── Left: h1 logo ── */
.hero-logo-img {
  height: 48px;
  width: auto;
  display: block;
}

h1.heading-display {
  line-height: normal;
}

/* ── Left: typography ── */
.hero-tagline {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--accent);
}

.hero-subtitle {
  font-size: 0.9rem;
  color: var(--text-tertiary);
}

/* ── Left: partner logos ── */
.hero-partners {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.hero-partners-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.hero-partners-logos {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hero-partner-logo {
  height: 70px;
  width: auto;
  object-fit: contain;
  //opacity: 0.65;
  //filter: brightness(1.0);
  transition: opacity 0.2s ease, filter 0.2s ease;
}

.hero-partner-logo:hover {
  opacity: 1;
  filter: grayscale(0%);
}

/* ── Right: glyph preview grid ── */
.hero-preview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  width: 100%;
}

.hero-glyph-cell {
  aspect-ratio: 128 / 55;
  background: var(--glyph-bg);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.4s ease-out both;
  position: relative;
  overflow: hidden;
}

.hero-glyph-cell::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(var(--glyph-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--glyph-grid) 1px, transparent 1px);
  background-size: 8px 8px;
  pointer-events: none;
}

.hero-glyph-cell::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 50%;
  height: 1px;
  background: var(--baseline-stroke);
  opacity: 0.5;
}

.hero-glyph-char {
  font-family: 'MetFont', sans-serif;
  font-size: 28px;
  line-height: 1;
  position: relative;
  z-index: 1;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));
}

/* ── Right: metrics strip ── */
.hero-metrics {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}
</style>
