<script setup>
import { ref } from 'vue'

const props = defineProps({
  categories: { type: Array, default: () => [] },
  selectedCategory: { type: String, default: 'all' },
  searchQuery: { type: String, default: '' },
  totalCount: { type: Number, default: 0 },
  filteredCount: { type: Number, default: 0 }
})

const emit = defineEmits(['update:searchQuery', 'update:selectedCategory', 'navigate-plane'])

const searchInput = ref(null)
const showCategories = ref(true)

function focusSearch() {
  searchInput.value?.focus()
}

defineExpose({ focusSearch, searchInput })

// Map category keys to representative unicode codepoints for icon display
const CATEGORY_ICONS = {
  'CH_CloudHigh': 'U+E000',
  'CL_CloudLow': 'U+E009',
  'CM_CloudMedium': 'U+E013',
  'C_CloudGenus': 'U+E01C',
  'N_TotalCloudCover': 'U+E026',
  'ww_PresentWeather': 'U+E100',
  'wawa_PresentWeatherAutomaticStation': 'U+E16F',
  'w1w1_PresentWeatherAdditional': 'U+E1C0',
  'W1W2_PastWeather': 'U+E300',
  'Wa1Wa2_PastWeatherAutomaticStation': 'U+E309',
  'E_StateOfGround': 'U+E400',
  'Eprime_StateOfGround': 'U+E40A',
  'a_PressureTendencyCharacteristic': 'U+E500',
  'PressureCentres': 'U+E509',
  'ddff_WindArrows': 'U+E600',
  'dw1dw1_SwellDirection': 'U+E666',
  'Ds_ShipDirection': 'U+E66A',
  'ICAO_SigWx': 'U+E700',
  'Ft_Fronts': 'U+E727',
}

const CATEGORY_TO_PLANE = {
  'CH_CloudHigh': 'sky-cloud',
  'CL_CloudLow': 'sky-cloud',
  'CM_CloudMedium': 'sky-cloud',
  'C_CloudGenus': 'sky-cloud',
  'N_TotalCloudCover': 'sky-cloud',
  'ww_PresentWeather': 'present-weather',
  'wawa_PresentWeatherAutomaticStation': 'present-weather',
  'w1w1_PresentWeatherAdditional': 'present-weather',
  'W1W2_PastWeather': 'past-weather',
  'Wa1Wa2_PastWeatherAutomaticStation': 'past-weather',
  'E_StateOfGround': 'state-of-ground',
  'Eprime_StateOfGround': 'state-of-ground',
  'a_PressureTendencyCharacteristic': 'pressure',
  'PressureCentres': 'pressure',
  'ddff_WindArrows': 'wind-ocean',
  'dw1dw1_SwellDirection': 'wind-ocean',
  'Ds_ShipDirection': 'wind-ocean',
  'ICAO_SigWx': 'significant-weather',
  'Ft_Fronts': 'significant-weather',
}

function getChar(unicode) {
  return String.fromCodePoint(parseInt(unicode.replace('U+', ''), 16))
}

function getCategoryIcon(catName) {
  // Try exact match first, then prefix match
  if (CATEGORY_ICONS[catName]) return CATEGORY_ICONS[catName]
  for (const [key, val] of Object.entries(CATEGORY_ICONS)) {
    if (catName.startsWith(key)) return val
  }
  return null
}

function getShortLabel(catName) {
  if (catName === 'all') return 'All'
  // Extract the part after the last space or dash for a shorter label
  const label = catName.replace(/-/g, ' ')
  const parts = label.split(' ').filter(p => p.length > 0)
  // Take last 2 meaningful words
  return parts.slice(-2).join(' ')
}
</script>

<template>
  <section class="filter-section">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <!-- Search row -->
      <div class="filter-search-row">
        <div class="search-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
          <input
            ref="searchInput"
            :value="searchQuery"
            @input="emit('update:searchQuery', $event.target.value)"
            type="search"
            class="search-input"
            placeholder="Search symbols... (press / to focus)"
            aria-label="Search symbols"
          />
          <kbd v-if="!searchQuery" class="search-kbd">/</kbd>
          <button
            v-if="searchQuery"
            @click="emit('update:searchQuery', '')"
            class="search-clear"
            aria-label="Clear search"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6 6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="filter-meta">
          <span class="filter-count">{{ filteredCount }}<span v-if="searchQuery || selectedCategory !== 'all'" class="filter-count-total"> / {{ totalCount }}</span></span>
          <button
            @click="showCategories = !showCategories"
            class="filter-toggle"
            :aria-expanded="showCategories"
            aria-label="Toggle category filter"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>
            </svg>
            <span class="hidden sm:inline">Categories</span>
          </button>
        </div>
      </div>

      <!-- Category chips -->
      <div v-if="showCategories" class="category-grid">
        <button
          v-for="cat in categories"
          :key="cat.name"
          @click="cat.name === 'all' ? emit('update:selectedCategory', 'all') : emit('navigate-plane', CATEGORY_TO_PLANE[cat.name])"
          class="cat-chip"
          :class="{ 'is-active': selectedCategory === cat.name }"
          :title="(cat.label || cat.name) + ' (' + cat.count + ')'"
        >
          <span
            v-if="cat.name !== 'all'"
            class="cat-chip-icon"
          >{{ getChar(getCategoryIcon(cat.name) || '') }}</span>
          <svg v-else class="cat-chip-icon cat-chip-icon-all" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" rx="1"/>
            <rect x="14" y="3" width="7" height="7" rx="1"/>
            <rect x="3" y="14" width="7" height="7" rx="1"/>
            <rect x="14" y="14" width="7" height="7" rx="1"/>
          </svg>
          <span class="cat-chip-label">{{ cat.label || getShortLabel(cat.name) }}</span>
          <span class="cat-chip-count">{{ cat.count }}</span>
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.filter-section {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 64px;
  z-index: 40;
  backdrop-filter: blur(12px);
}

/* ── Search row ── */
.filter-search-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-wrapper {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 40px;
  font-size: 14px;
  border-radius: var(--radius-md);
  background: var(--bg-input);
  border: 1px solid var(--border-default);
  color: var(--text-primary);
  outline: none;
  transition: all 0.15s;
  font-family: inherit;
}

.search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-muted);
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.search-kbd {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  display: none;
  align-items: center;
  padding: 2px 6px;
  font-size: 11px;
  border-radius: 4px;
  border: 1px solid var(--border-default);
  background: var(--bg-overlay);
  color: var(--text-tertiary);
  font-family: inherit;
}

@media (min-width: 640px) {
  .search-kbd {
    display: inline-flex;
  }
}

.search-clear {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.15s;
}

.search-clear:hover {
  color: var(--text-primary);
  background: var(--accent-muted);
}

/* ── Meta ── */
.filter-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.filter-count {
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  color: var(--text-secondary);
  white-space: nowrap;
}

.filter-count-total {
  color: var(--text-tertiary);
}

.filter-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-md);
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  font-family: inherit;
}

.filter-toggle:hover {
  color: var(--text-primary);
  border-color: var(--border-default);
  background: var(--accent-subtle);
}

/* ── Category grid ── */
.category-grid {
  display: flex;
  gap: 6px;
  margin-top: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.category-grid::-webkit-scrollbar {
  display: none;
}

.cat-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: var(--radius-md);
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  flex-shrink: 0;
  font-family: inherit;
  font-size: 12px;
  font-weight: 500;
}

.cat-chip:hover {
  color: var(--text-primary);
  border-color: var(--border-default);
  background: var(--accent-subtle);
}

.cat-chip.is-active {
  background: var(--accent-muted);
  color: var(--accent);
  border-color: var(--accent);
}

.cat-chip-icon {
  font-family: 'MetFont', sans-serif;
  font-size: 16px;
  line-height: 1;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.cat-chip-icon-all {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
}

.cat-chip.is-active .cat-chip-icon-all {
  color: var(--accent);
}

.cat-chip-label {
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cat-chip-count {
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 10px;
  background: var(--bg-base);
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.cat-chip.is-active .cat-chip-count {
  background: rgba(74, 158, 255, 0.2);
  color: var(--accent);
}

@media (min-width: 768px) {
  .category-grid {
    flex-wrap: wrap;
    overflow-x: visible;
  }

  .cat-chip {
    flex-shrink: 1;
  }
}
</style>
