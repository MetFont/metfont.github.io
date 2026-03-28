<script setup>
import GlyphCard from './GlyphCard.vue'

const props = defineProps({
  glyphs: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  compareList: { type: Array, default: () => [] },
  searchQuery: { type: String, default: '' },
  selectedCategory: { type: String, default: 'all' }
})

const emit = defineEmits(['openDetail', 'toggleCompare', 'resetFilters'])

function isInCompare(glyph) {
  return props.compareList.some(g => g.codepoint === glyph.codepoint)
}
</script>

<template>
  <main class="grid-section">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <!-- Loading -->
      <div v-if="loading" class="grid-message">
        <div class="loading-spinner"></div>
        <span class="body-text">Loading glyphs...</span>
      </div>

      <!-- Empty state -->
      <div v-else-if="!glyphs.length" class="grid-message">
        <svg class="w-12 h-12" style="color: var(--text-tertiary)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <h3 class="heading-section">No symbols found</h3>
        <p class="body-text">Try adjusting your search or filter</p>
        <button @click="emit('resetFilters')" class="btn-ghost mt-2">Reset filters</button>
      </div>

      <!-- Grid -->
      <div v-else class="glyph-grid-layout">
        <GlyphCard
          v-for="glyph in glyphs"
          :key="glyph.codepoint"
          :glyph="glyph"
          :is-compared="isInCompare(glyph)"
          @open="emit('openDetail', $event)"
          @toggle-compare="emit('toggleCompare', $event)"
        />
      </div>
    </div>
  </main>
</template>

<style scoped>
.grid-section {
  flex: 1;
  background: var(--bg-base);
}

.grid-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  gap: 16px;
}

.glyph-grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
}

@media (min-width: 640px) {
  .glyph-grid-layout {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
  }
}

@media (min-width: 1024px) {
  .glyph-grid-layout {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 2px solid var(--border-default);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
