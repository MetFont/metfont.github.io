<script setup>
import { ref, onMounted, computed, onUnmounted, watch } from 'vue'
import AppHeader from '../../components/AppHeader.vue'
import HeroSection from '../../components/HeroSection.vue'
import FilterBar from '../../components/FilterBar.vue'
import GlyphGrid from '../../components/GlyphGrid.vue'
import CompareTray from '../../components/CompareTray.vue'
import GlyphDetail from '../../components/GlyphDetail.vue'
import PlaneDetail from '../../components/PlaneDetail.vue'
import AboutSection from '../../components/AboutSection.vue'
import DownloadSection from '../../components/DownloadSection.vue'
import CategoriesSection from '../../components/CategoriesSection.vue'
import UsageSection from '../../components/UsageSection.vue'

const glyphs = ref([])
const glyphMetadata = ref(null) // Lazy-loaded on first glyph detail view
const planeInfo = ref({})
const fontVersion = ref('')
const loading = ref(true)

// Metadata is now eagerly loaded from metadata.json in onMounted
async function ensureMetadata() {
  return glyphMetadata.value || {}
}

// Apply metadata to a glyph object (mutates in place for reactivity)
function enrichGlyph(glyph) {
  if (!glyphMetadata.value || !glyph || glyph.metadata) return
  const meta = glyphMetadata.value[glyph.unicode]
  if (meta) glyph.metadata = meta
}

onMounted(async () => {
  try {
    const metaRes = await fetch('/metadata.json')
    const data = await metaRes.json()
    glyphs.value = data.glyphs || []
    planeInfo.value = data.planes || {}
    fontVersion.value = data.version || ''
    glyphMetadata.value = data.metadata || {}
  } catch (e) {
    console.error('Failed to load data:', e)
  } finally {
    loading.value = false
  }

  // Defer Google Fonts loading — not blocking initial render
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap'
  document.head.appendChild(link)
})

const searchQuery = ref('')
const selectedCategory = ref('all')
const compareList = ref([])
const filterBarRef = ref(null)

// ── Hash-based routing ──
const currentHash = ref(typeof window !== 'undefined' ? window.location.hash.slice(1) : '')

function onHashChange() {
  currentHash.value = window.location.hash.slice(1)
  // Always scroll to top on navigation
  window.scrollTo(0, 0)
}

onMounted(() => {
  window.addEventListener('hashchange', onHashChange)
  currentHash.value = window.location.hash.slice(1)
})

onUnmounted(() => {
  window.removeEventListener('hashchange', onHashChange)
})

const currentView = computed(() => {
  const h = currentHash.value
  if (h.startsWith('glyph/')) return 'detail'
  if (h.startsWith('plane/')) return 'plane'
  if (h === 'about') return 'about'
  if (h === 'download') return 'download'
  if (h === 'categories') return 'categories'
  if (h.startsWith('usage')) return 'usage'
  return 'grid'
})

const selectedCodepoint = computed(() => {
  if (currentView.value !== 'detail') return null
  return currentHash.value.replace('glyph/', '')
})

const selectedPlaneSlug = computed(() => {
  if (currentView.value !== 'plane') return null
  return currentHash.value.replace('plane/', '')
})

const selectedPlane = computed(() => {
  if (!selectedPlaneSlug.value) return null
  return planeInfo.value[selectedPlaneSlug.value] || null
})

const selectedGlyph = computed(() => {
  if (!selectedCodepoint.value) return null
  return glyphs.value.find(g => g.unicode === selectedCodepoint.value) || null
})

// Lazy-load metadata when a glyph detail view is opened
watch(selectedGlyph, async (glyph) => {
  if (!glyph) return
  if (glyph.metadata) return
  const meta = await ensureMetadata()
  if (meta) enrichGlyph(glyph)
}, { immediate: true })

function navigateToGlyph(glyph) {
  window.location.hash = `glyph/${glyph.unicode}`
}

function navigateToAbout() {
  window.location.hash = 'about'
}

function navigateToDownload() {
  window.location.hash = 'download'
}

function navigateToGrid() {
  window.location.hash = ''
}

function navigateToPlane(slug) {
  window.location.hash = `plane/${slug}`
}

function navigateToCategories() {
  window.location.hash = 'categories'
}

function navigateToUsage() {
  window.location.hash = 'usage/web'
}

// ── Categories ──
const categories = computed(() => {
  const cats = new Map()
  glyphs.value.forEach(g => {
    const label = g.categoryLabel || g.category
    if (!cats.has(g.category)) {
      cats.set(g.category, { label, count: 0 })
    }
    cats.get(g.category).count++
  })
  return [
    { name: 'all', label: 'All', count: glyphs.value.length },
    ...Array.from(cats.entries())
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([name, { label, count }]) => ({ name, label, count }))
  ]
})

// ── Filtering ──
const filteredGlyphs = computed(() => {
  let result = glyphs.value
  if (selectedCategory.value !== 'all') {
    result = result.filter(g => g.category === selectedCategory.value)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(g =>
      g.name.toLowerCase().includes(q) ||
      g.unicode.toLowerCase().includes(q) ||
      g.category.toLowerCase().includes(q) ||
      (g.categoryLabel && g.categoryLabel.toLowerCase().includes(q)) ||
      (g.description && g.description.toLowerCase().includes(q))
    )
  }
  return result
})

// ── Compare ──
function toggleCompare(glyph) {
  const idx = compareList.value.findIndex(g => g.codepoint === glyph.codepoint)
  if (idx >= 0) {
    compareList.value.splice(idx, 1)
  } else if (compareList.value.length < 6) {
    compareList.value.push(glyph)
  }
}

function isInCompare(glyph) {
  return compareList.value.some(g => g.codepoint === glyph.codepoint)
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'all'
}

// ── Keyboard shortcuts ──
function handleKeydown(e) {
  if (e.key === 'Escape') {
    if (currentView.value === 'detail' || currentView.value === 'about' || currentView.value === 'download' || currentView.value === 'plane' || currentView.value === 'categories' || currentView.value === 'usage') {
      navigateToGrid()
    }
  }
  if (e.key === '/' && currentView.value === 'grid' && document.activeElement !== filterBarRef.value?.searchInput) {
    e.preventDefault()
    filterBarRef.value?.focusSearch()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="app-root">
    <AppHeader
      :total="glyphs.length"
      :current-view="currentView"
      :selected-glyph="selectedGlyph"
      :version="fontVersion"
      @navigate-grid="navigateToGrid"
      @navigate-about="navigateToAbout"
      @navigate-download="navigateToDownload"
      @navigate-categories="navigateToCategories"
      @navigate-usage="navigateToUsage"
    />

    <GlyphDetail
      v-if="currentView === 'detail' && selectedGlyph"
      :glyph="selectedGlyph"
      :all-glyphs="glyphs"
      :is-in-compare="isInCompare(selectedGlyph)"
      @navigate-back="navigateToGrid"
      @toggle-compare="toggleCompare"
      @select-glyph="navigateToGlyph"
      @navigate-plane="navigateToPlane"
    />

    <PlaneDetail
      v-else-if="currentView === 'plane' && selectedPlane"
      :plane="selectedPlane"
      :plane-info="planeInfo"
      :all-glyphs="glyphs"
      @navigate-back="navigateToGrid"
      @select-glyph="navigateToGlyph"
      @navigate-plane="navigateToPlane"
    />

    <AboutSection
      v-else-if="currentView === 'about'"
      :total-glyphs="glyphs.length"
      :categories="categories"
      :plane-info="planeInfo"
      @navigate-back="navigateToGrid"
      @navigate-plane="navigateToPlane"
    />

    <DownloadSection
      v-else-if="currentView === 'download'"
      :version="fontVersion"
      @navigate-back="navigateToGrid"
    />

    <CategoriesSection
      v-else-if="currentView === 'categories'"
      :plane-info="planeInfo"
      :total-glyphs="glyphs.length"
      @navigate-back="navigateToGrid"
      @navigate-plane="navigateToPlane"
    />

    <UsageSection
      v-else-if="currentView === 'usage'"
      @navigate-back="navigateToGrid"
    />

    <template v-else>
      <HeroSection
        @browse="filterBarRef?.focusSearch()"
        @view-grid="document.querySelector('.grid-section')?.scrollIntoView({ behavior: 'smooth' })"
        @view-about="navigateToAbout"
        @view-download="navigateToDownload"
      />

      <FilterBar
        ref="filterBarRef"
        v-model:searchQuery="searchQuery"
        v-model:selectedCategory="selectedCategory"
        :categories="categories"
        :total-count="glyphs.length"
        :filtered-count="filteredGlyphs.length"
        @navigate-plane="navigateToPlane"
      />

      <CompareTray
        v-if="compareList.length > 0"
        :compare-list="compareList"
        @open-detail="navigateToGlyph"
        @toggle-compare="toggleCompare"
        @clear-all="compareList = []"
      />

      <GlyphGrid
        :glyphs="filteredGlyphs"
        :loading="loading"
        :compare-list="compareList"
        :search-query="searchQuery"
        :selected-category="selectedCategory"
        @open-detail="navigateToGlyph"
        @toggle-compare="toggleCompare"
        @reset-filters="resetFilters"
      />
    </template>

    <!-- Site-wide footer -->
    <footer class="site-footer">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div class="flex flex-col sm:flex-row items-center gap-2 sm:gap-4">
            <p class="text-sm" style="color: var(--text-tertiary)">
              &copy; {{ new Date().getFullYear() }} Ribose. CC BY 3.0.
            </p>
            <span class="hidden sm:inline" style="color: var(--border-default)">|</span>
            <a
              href="https://www.ribose.com"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-ribose-link"
            >
              A Ribose project
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>
          <div class="flex items-center gap-4">
            <a href="https://github.com/MetFont/metfont" target="_blank" rel="noopener noreferrer" class="footer-ribose-link">
              GitHub
            </a>
            <a href="https://github.com/MetFont/metfont/releases" target="_blank" rel="noopener noreferrer" class="footer-ribose-link">
              Releases
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.site-footer {
  margin-top: auto;
  border-top: 1px solid var(--border-subtle);
  background: var(--bg-surface);
}

.footer-ribose-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--text-tertiary);
  text-decoration: none;
  transition: color 0.15s;
}

.footer-ribose-link:hover {
  color: var(--accent);
}
</style>
