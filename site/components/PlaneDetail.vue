<script setup>
import { computed, onMounted, ref } from 'vue'
import GlyphCard from './GlyphCard.vue'

const props = defineProps({
  plane: { type: Object, required: true },
  planeInfo: { type: Object, default: () => ({}) },
  allGlyphs: { type: Array, default: () => [] }
})

const emit = defineEmits(['navigateBack', 'selectGlyph', 'navigatePlane'])

const fontSize = ref(48)

const planeGlyphs = computed(() => {
  const start = props.plane.blockStart
  const end = props.plane.blockEnd
  return props.allGlyphs
    .filter(g => g.dec >= start && g.dec <= end)
    .sort((a, b) => a.dec - b.dec)
})

const subCategoryGlyphs = computed(() => {
  const groups = new Map()
  for (const sub of props.plane.subCategories) {
    groups.set(sub.id, [])
  }
  for (const glyph of planeGlyphs.value) {
    for (const sub of props.plane.subCategories) {
      if (glyph.category === sub.id || glyph.category.startsWith(sub.id)) {
        groups.get(sub.id).push(glyph)
        break
      }
    }
  }
  return groups
})

function getChar(unicode) {
  return String.fromCodePoint(parseInt(unicode.replace('U+', ''), 16))
}

function navigateToPlane(slug) {
  emit('navigatePlane', slug)
}

// Plane navigation
const planeSlugs = [
  'sky-cloud', 'present-weather', 'past-weather', 'state-of-ground',
  'pressure', 'wind-ocean', 'significant-weather'
]

const navItems = computed(() => {
  const idx = planeSlugs.indexOf(props.plane.slug)
  return {
    prev: idx > 0 ? planeSlugs[idx - 1] : null,
    next: idx < planeSlugs.length - 1 ? planeSlugs[idx + 1] : null,
    position: idx + 1,
    total: planeSlugs.length
  }
})

const codeTableList = computed(() => {
  if (!props.plane.codeTables) return []
  return Object.entries(props.plane.codeTables).map(([key, val]) => ({
    key,
    name: val.name,
    table: val.table,
    codes: val.codes,
    url: val.url
  }))
})

const hasMixedSources = computed(() => {
  const subs = props.plane.subCategories || []
  if (subs.length < 2) return false
  const sources = subs.map(s => (s.creator || '') + '|' + (s.publisher || '') + '|' + (s.source || ''))
  return new Set(sources).size > 1
})
</script>

<template>
  <main class="plane-page animate-slide-up">
    <!-- Nav bar -->
    <div class="plane-nav">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-12">
          <div class="flex items-center gap-2">
            <button @click="emit('navigateBack')" class="btn-icon" aria-label="Back to grid">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
            </button>
            <span class="text-xs" style="color: var(--text-tertiary)">Categories</span>
            <svg class="w-3 h-3" style="color: var(--text-tertiary)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
            <span class="text-xs font-medium" style="color: var(--text-secondary)">{{ plane.name }}</span>
          </div>
          <div class="flex items-center gap-1">
            <button
              v-if="navItems.prev"
              @click="navigateToPlane(navItems.prev)"
              class="btn-icon"
              aria-label="Previous category"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 18l-6-6 6-6"/>
              </svg>
            </button>
            <span class="text-[10px] tabular-nums px-1" style="color: var(--text-tertiary)">
              {{ navItems.position }}/{{ navItems.total }}
            </span>
            <button
              v-if="navItems.next"
              @click="navigateToPlane(navItems.next)"
              class="btn-icon"
              aria-label="Next category"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 18l6-6-6-6"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <!-- Header -->
      <div class="plane-header">
        <h1 class="plane-title">{{ plane.name }}</h1>
        <div class="plane-badges">
          <span class="badge">{{ plane.range[0] }}&ndash;{{ plane.range[1] }}</span>
          <span class="badge">{{ plane.count }} symbols</span>
          <span v-if="codeTableList.length" class="badge-amber">{{ codeTableList.length }} code tables</span>
        </div>
      </div>

      <!-- Description -->
      <div v-if="plane.description" class="plane-description">
        <p class="body-text">{{ plane.description }}</p>
      </div>

      <!-- Overview -->
      <div v-if="plane.overview" class="plane-overview">
        <h2 class="section-heading">Overview</h2>
        <p class="body-text">{{ plane.overview }}</p>
      </div>

      <div class="plane-layout">
        <!-- Left: metadata + sub-categories -->
        <div class="plane-left">
          <!-- WMO Documents -->
          <div v-if="plane.wmoDocuments && plane.wmoDocuments.length" class="plane-section">
            <h2 class="section-heading">WMO References</h2>
            <div class="doc-list">
              <a
                v-for="(doc, i) in plane.wmoDocuments"
                :key="i"
                :href="doc.url"
                target="_blank"
                rel="noopener"
                class="doc-item"
              >
                <div class="doc-info">
                  <span class="doc-name">{{ doc.name }}</span>
                  <span v-if="doc.sections" class="doc-sections">{{ doc.sections }}</span>
                </div>
                <svg class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Code Tables -->
          <div v-if="codeTableList.length" class="plane-section">
            <h2 class="section-heading">Code Tables</h2>
            <div class="ct-list">
              <a
                v-for="ct in codeTableList"
                :key="ct.key"
                :href="ct.url"
                target="_blank"
                rel="noopener"
                class="ct-item"
              >
                <div class="ct-info">
                  <span class="ct-name">{{ ct.name }}</span>
                  <span class="ct-meta">{{ ct.table }} &middot; {{ ct.codes }}</span>
                </div>
                <svg class="w-3.5 h-3.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Usage in Practice -->
          <div v-if="plane.usageInPractice && plane.usageInPractice.length" class="plane-section">
            <h2 class="section-heading">Usage in Practice</h2>
            <div class="usage-list">
              <div v-for="(usage, i) in plane.usageInPractice" :key="i" class="usage-item">
                <h3 class="usage-context">{{ usage.context }}</h3>
                <p class="usage-desc">{{ usage.description }}</p>
                <pre v-if="usage.example" class="usage-example"><code>{{ usage.example }}</code></pre>
              </div>
            </div>
          </div>

          <!-- Sub-categories with descriptions -->
          <div v-if="plane.subCategories && plane.subCategories.length" class="plane-section">
            <h2 class="section-heading">Sub-categories</h2>
            <div class="subcat-list">
              <div v-for="sub in plane.subCategories" :key="sub.id" class="subcat-item">
                <div class="subcat-info">
                  <span class="subcat-label">{{ sub.label }}</span>
                  <p v-if="sub.description" class="subcat-desc">{{ sub.description }}</p>
                </div>
                <span class="subcat-count">{{ sub.count }}</span>
              </div>
            </div>
          </div>

          <!-- Source Metadata -->
          <div class="plane-section">
            <h2 class="section-heading">Source</h2>

            <!-- Check if sub-categories have different sources -->
            <template v-if="hasMixedSources">
              <div v-for="sub in plane.subCategories" :key="'src-'+sub.id" class="source-block">
                <div class="source-block-header">
                  <span class="source-block-label">{{ sub.label }}</span>
                  <span v-if="sub.publisher" class="source-publisher-badge">{{ sub.publisher }}</span>
                </div>
                <div class="meta-fields">
                  <div v-if="sub.source" class="meta-field">
                    <span class="label-text">Document</span>
                    <span class="body-text text-xs">{{ sub.source }}</span>
                  </div>
                  <div v-if="sub.creator" class="meta-field">
                    <span class="label-text">Creator</span>
                    <span class="code-text">{{ sub.creator }}</span>
                  </div>
                  <div v-if="sub.date" class="meta-field">
                    <span class="label-text">Date</span>
                    <span class="code-text">{{ sub.date }}</span>
                  </div>
                </div>
              </div>
            </template>

            <!-- Single source for the whole plane -->
            <template v-else>
              <div class="meta-fields">
                <div v-if="plane.creator" class="meta-field">
                  <span class="label-text">Creator</span>
                  <span class="code-text">{{ plane.creator }}</span>
                </div>
                <div v-if="plane.publisher" class="meta-field">
                  <span class="label-text">Publisher</span>
                  <span class="code-text">{{ plane.publisher }}</span>
                </div>
                <div v-if="plane.date" class="meta-field">
                  <span class="label-text">Date</span>
                  <span class="code-text">{{ plane.date }}</span>
                </div>
                <div v-if="plane.contributor" class="meta-field">
                  <span class="label-text">Contributor</span>
                  <span class="code-text">{{ plane.contributor }}</span>
                </div>
                <div v-if="plane.wmoSource" class="meta-field">
                  <span class="label-text">Document</span>
                  <span class="body-text text-xs">{{ plane.wmoSource }}</span>
                </div>
                <div v-if="plane.wmoCodeTable" class="meta-field">
                  <span class="label-text">Code Table</span>
                  <a :href="plane.wmoCodeTable" target="_blank" rel="noopener" class="code-text" style="color: var(--accent)">{{ plane.wmoCodeTable }}</a>
                </div>
              </div>
            </template>

            <div v-if="plane.license" class="meta-field" style="margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--border-subtle)">
              <span class="label-text">License</span>
              <a :href="plane.license" target="_blank" rel="noopener" class="code-text" style="color: var(--accent)">{{ plane.license }}</a>
            </div>
          </div>
        </div>

        <!-- Right: glyph grid -->
        <div class="plane-right">
          <div v-for="sub in plane.subCategories" :key="sub.id" class="subcat-group">
            <div class="subcat-group-header">
              <h3 class="subcat-group-title">{{ sub.label }}</h3>
              <span class="subcat-group-count">{{ sub.count }} symbols</span>
            </div>
            <div class="plane-glyph-grid">
              <GlyphCard
                v-for="glyph in subCategoryGlyphs.get(sub.id)"
                :key="glyph.codepoint"
                :glyph="glyph"
                @open="emit('selectGlyph', $event)"
              />
            </div>
          </div>

          <!-- Plane nav links -->
          <div class="plane-nav-links">
            <button
              v-if="navItems.prev"
              @click="navigateToPlane(navItems.prev)"
              class="btn-ghost"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 18l-6-6 6-6"/>
              </svg>
              {{ props.planeInfo[navItems.prev]?.name || 'Previous' }}
            </button>
            <span v-else></span>
            <button
              v-if="navItems.next"
              @click="navigateToPlane(navItems.next)"
              class="btn-ghost"
            >
              {{ props.planeInfo[navItems.next]?.name || 'Next' }}
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 18l6-6-6-6"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.plane-page {
  flex: 1;
  background: var(--bg-base);
}

/* ── Nav ── */
.plane-nav {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 64px;
  z-index: 40;
  backdrop-filter: blur(12px);
}

/* ── Header ── */
.plane-header {
  margin-bottom: 24px;
}

.plane-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.1;
  margin-bottom: 12px;
}

@media (min-width: 640px) {
  .plane-title {
    font-size: 2.5rem;
  }
}

.plane-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* ── Description & Overview (full width above layout) ── */
.plane-description {
  max-width: 72rem;
  margin-bottom: 24px;
}

.plane-description p {
  font-size: 1.0625rem;
  line-height: 1.7;
  color: var(--text-secondary);
}

.plane-overview {
  max-width: 72rem;
  margin-bottom: 32px;
}

.plane-overview p {
  color: var(--text-secondary);
}

/* ── Section heading ── */
.section-heading {
  font-size: 0.8125rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-subtle);
}

/* ── Layout ── */
.plane-layout {
  display: grid;
  gap: 32px;
}

@media (min-width: 1024px) {
  .plane-layout {
    grid-template-columns: 4fr 8fr;
    gap: 48px;
  }
}

/* ── Left column ── */
.plane-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.plane-section {
  display: flex;
  flex-direction: column;
}

/* ── WMO Documents ── */
.doc-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.doc-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  padding: 10px 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--accent);
  transition: all 0.15s;
  text-decoration: none;
}

.doc-item:hover {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.doc-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.doc-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.doc-sections {
  font-size: 11px;
  color: var(--text-tertiary);
  word-break: break-word;
}

/* ── Code Tables ── */
.ct-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.ct-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--accent);
  transition: all 0.15s;
  text-decoration: none;
}

.ct-item:hover {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.ct-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.ct-name {
  font-size: 13px;
  color: var(--text-primary);
}

.ct-meta {
  font-size: 11px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  color: var(--text-tertiary);
}

/* ── Usage in Practice ── */
.usage-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.usage-item {
  padding: 14px 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.usage-context {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.usage-desc {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.usage-example {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 11px;
  line-height: 1.5;
  color: var(--text-secondary);
  overflow-x: auto;
  margin: 0;
}

.usage-example code {
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
}

/* ── Sub-categories ── */
.subcat-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.subcat-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.subcat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.subcat-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.subcat-desc {
  font-size: 12px;
  line-height: 1.5;
  color: var(--text-secondary);
}

.subcat-count {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  background: var(--bg-overlay);
  color: var(--text-tertiary);
  flex-shrink: 0;
  margin-top: 2px;
}

/* ── Source blocks (mixed provenance) ── */
.source-block {
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  margin-bottom: 8px;
}

.source-block:last-child {
  margin-bottom: 0;
}

.source-block-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.source-block-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.source-publisher-badge {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--accent-subtle);
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* ── Legacy metadata ── */
.meta-fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.meta-field {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* ── Right column ── */
.plane-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── Glyph grid per sub-category ── */
.subcat-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.subcat-group-header {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-subtle);
}

.subcat-group-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
}

.subcat-group-count {
  font-size: 11px;
  color: var(--text-tertiary);
}

.plane-glyph-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 8px;
}

@media (min-width: 640px) {
  .plane-glyph-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
  }
}

@media (min-width: 1024px) {
  .plane-glyph-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }
}

/* ── Plane nav links ── */
.plane-nav-links {
  display: flex;
  justify-content: space-between;
  padding-top: 24px;
  border-top: 1px solid var(--border-subtle);
}
</style>
