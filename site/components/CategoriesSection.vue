<script setup>
import { computed } from 'vue'

const props = defineProps({
  planeInfo: { type: Object, default: () => ({}) },
  totalGlyphs: { type: Number, default: 0 }
})

const emit = defineEmits(['navigateBack', 'navigatePlane'])

const sortedPlanes = computed(() => {
  return Object.values(props.planeInfo)
    .sort((a, b) => (a.blockStart || 0) - (b.blockStart || 0))
})

const ALLOCATED_RANGES = [
  { start: 0xE000, end: 0xE0FF },
  { start: 0xE100, end: 0xE2FF },
  { start: 0xE300, end: 0xE3FF },
  { start: 0xE400, end: 0xE4FF },
  { start: 0xE500, end: 0xE5FF },
  { start: 0xE600, end: 0xE6FF },
  { start: 0xE700, end: 0xE7FF },
]
</script>

<template>
  <main class="categories-page animate-slide-up">
    <!-- Back nav -->
    <div class="categories-nav">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center h-12">
          <button @click="emit('navigateBack')" class="btn-icon" aria-label="Back to grid">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
          </button>
          <span class="text-xs font-medium" style="color: var(--text-secondary)">Categories</span>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <!-- Hero -->
      <div class="categories-hero">
        <h1 class="categories-title">Symbol Categories</h1>
        <p class="categories-subtitle">
          {{ totalGlyphs }} symbols organized into {{ sortedPlanes.length }} semantic blocks
          within the Unicode Private Use Area (U+E000&ndash;U+E7FF). Each block maps to
          a WMO observation category.
        </p>
      </div>

      <!-- PUA Range Map -->
      <section class="categories-section">
        <h2 class="categories-section-title">PUA Block Allocation</h2>
        <div class="pua-map">
          <div
            v-for="plane in sortedPlanes"
            :key="plane.slug"
            class="pua-block"
            @click="emit('navigatePlane', plane.slug)"
          >
            <div class="pua-block-range">
              <span class="code-text">{{ plane.range[0] }}</span>
              <span class="text-xs" style="color: var(--text-tertiary)">&ndash;</span>
              <span class="code-text">{{ plane.range[1] }}</span>
            </div>
            <div class="pua-block-fill" :style="{ flex: plane.count }"></div>
            <div class="pua-block-label">
              <span class="text-xs font-medium" style="color: var(--text-primary)">{{ plane.name }}</span>
              <span class="code-text text-xs">{{ plane.count }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Category Cards -->
      <section class="categories-section">
        <h2 class="categories-section-title">Categories</h2>
        <div class="category-cards">
          <div
            v-for="plane in sortedPlanes"
            :key="plane.slug"
            class="category-card"
            @click="emit('navigatePlane', plane.slug)"
          >
            <div class="card-header">
              <div>
                <h3 class="card-name">{{ plane.name }}</h3>
                <div class="card-range">
                  <span class="code-text">{{ plane.range[0] }}</span>
                  <span class="mx-1" style="color: var(--text-tertiary)">&ndash;</span>
                  <span class="code-text">{{ plane.range[1] }}</span>
                </div>
              </div>
              <div class="card-count">
                <span class="card-count-num">{{ plane.count }}</span>
                <span class="card-count-label">glyphs</span>
              </div>
            </div>
            <p v-if="plane.description" class="card-desc">{{ plane.description }}</p>
            <div v-if="plane.subCategories?.length" class="card-pills">
              <span
                v-for="sub in plane.subCategories"
                :key="sub.id"
                class="card-pill"
              >{{ sub.label }}</span>
            </div>
            <div class="card-footer">
              <span class="card-link">View symbols &rarr;</span>
            </div>
          </div>
        </div>
      </section>
    </div>
    <footer class="section-footer">
      <p class="footer-humor">Every cloud has a silver lining — look at our symbols.</p>
    </footer>
  </main>
</template>

<style scoped>
.categories-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-base);
}

.categories-nav {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 64px;
  z-index: 40;
  backdrop-filter: blur(12px);
}

.categories-hero {
  margin-bottom: 3rem;
}

.categories-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.1;
  margin-bottom: 1rem;
}

@media (min-width: 640px) {
  .categories-title {
    font-size: 2.5rem;
  }
}

.categories-subtitle {
  font-size: 1.125rem;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 40rem;
}

.categories-section {
  margin-bottom: 3rem;
}

.categories-section-title {
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-subtle);
}

/* ── PUA Map ── */
.pua-map {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pua-block {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: all 0.15s;
}

.pua-block:hover {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.pua-block-range {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 120px;
  flex-shrink: 0;
}

.pua-block-fill {
  height: 8px;
  border-radius: 4px;
  background: var(--accent-muted);
  min-width: 8px;
}

.pua-block-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  flex-shrink: 0;
}

/* ── Category Cards ── */
.category-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-card {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-card:hover {
  border-color: var(--accent);
  box-shadow: var(--shadow-md);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.card-range {
  display: flex;
  align-items: center;
  margin-top: 2px;
}

.card-count {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  background: var(--accent-muted);
  flex-shrink: 0;
}

.card-count-num {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}

.card-count-label {
  font-size: 10px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-desc {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0 0 12px;
}

.card-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.card-pill {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  white-space: nowrap;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.card-link {
  font-size: 13px;
  font-weight: 500;
  color: var(--accent);
  transition: color 0.15s;
}

.category-card:hover .card-link {
  color: var(--accent-hover);
}

.section-footer {
  border-top: 1px solid var(--border-subtle);
  padding: 24px 0;
  margin-top: auto;
}

.footer-humor {
  font-style: italic;
  color: var(--text-tertiary);
  font-size: 0.875rem;
  text-align: center;
}
</style>
