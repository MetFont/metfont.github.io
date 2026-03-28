<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  glyph: { type: Object, required: true },
  allGlyphs: { type: Array, default: () => [] },
  isInCompare: { type: Boolean, default: false }
})

const emit = defineEmits(['navigateBack', 'toggleCompare', 'selectGlyph', 'navigatePlane'])

const fontSize = ref(64)
const copied = ref(false)
const previewText = ref('')

watch(() => props.glyph, (g) => {
  previewText.value = `The weather symbol ${getChar(g.unicode)} appears here`
}, { immediate: true })

const related = computed(() => {
  return props.allGlyphs
    .filter(g => g.category === props.glyph.category && g.codepoint !== props.glyph.codepoint)
    .slice(0, 12)
})

const navItems = computed(() => {
  const sorted = props.allGlyphs
    .filter(g => g.category === props.glyph.category)
    .sort((a, b) => a.dec - b.dec)
  const idx = sorted.findIndex(g => g.codepoint === props.glyph.codepoint)
  return {
    prev: idx > 0 ? sorted[idx - 1] : null,
    next: idx < sorted.length - 1 ? sorted[idx + 1] : null,
    position: idx + 1,
    total: sorted.length
  }
})

function getChar(unicode) {
  return String.fromCodePoint(parseInt(unicode.replace('U+', ''), 16))
}

function getUtf8Bytes(dec) {
  const ch = String.fromCodePoint(dec)
  const bytes = new TextEncoder().encode(ch)
  return Array.from(bytes).map(b => '0x' + b.toString(16).toUpperCase().padStart(2, '0')).join(' ')
}

function getHtmlEntity(dec) {
  return `&#x${dec.toString(16)};`
}

function getCssContent(unicode) {
  return `"\\${unicode.replace('U+', '').toLowerCase()}"`
}

async function copyCodepoint() {
  try {
    await navigator.clipboard.writeText(props.glyph.unicode)
    copied.value = true
    setTimeout(() => { copied.value = false }, 1500)
  } catch (e) {
    console.error('Copy failed:', e)
  }
}

const sourceGithubUrl = computed(() => {
  if (!props.glyph.sourcePath) return ''
  return `https://github.com/OGCMetOceanDWG/WorldWeatherSymbols/blob/master/${props.glyph.sourcePath}`
})

// Data-driven metadata field definitions.
// type: 'text' | 'link' | 'tags' | 'document'
// Adding a new field here is all that's needed to display it.
const METADATA_FIELDS = [
  { key: 'identifier', label: 'WMO Code', type: 'link' },
  { key: 'source', label: 'Source Document', type: 'document' },
  { key: 'creator', label: 'Creator' },
  { key: 'publisher', label: 'Publisher' },
  { key: 'contributor', label: 'Contributor' },
  { key: 'date', label: 'Date' },
  { key: 'language', label: 'Language' },
  { key: 'coverage', label: 'Coverage' },
  { key: 'rights', label: 'Rights' },
  { key: 'license', label: 'License', type: 'link' },
  { key: 'about', label: 'Upstream', type: 'link' },
  { key: 'version', label: 'Version' },
  { key: 'status', label: 'Status' },
  { key: 'subject', label: 'Keywords', type: 'tags' },
]

const visibleMetadataFields = computed(() => {
  const m = props.glyph.metadata
  if (!m) return []
  return METADATA_FIELDS.filter(f => {
    const val = m[f.key]
    if (Array.isArray(val)) return val.length > 0
    return val
  })
})
</script>

<template>
  <main class="detail-page animate-slide-up">
    <!-- Detail nav bar -->
    <div class="detail-nav">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-12">
          <div class="flex items-center gap-2">
            <button @click="emit('navigateBack')" class="btn-icon" aria-label="Back to grid">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
            </button>
            <button
              v-if="glyph.plane"
              @click="emit('navigatePlane', glyph.plane)"
              class="text-xs hover:underline cursor-pointer"
              style="color: var(--text-tertiary)"
            >
              {{ glyph.categoryLabel || glyph.category }}
            </button>
            <span v-else class="text-xs" style="color: var(--text-tertiary)">
              {{ glyph.categoryLabel || glyph.category }}
            </span>
            <svg class="w-3 h-3" style="color: var(--text-tertiary)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
            <span class="text-xs font-medium" style="color: var(--text-secondary)">{{ glyph.name }}</span>
          </div>
          <div class="flex items-center gap-1">
            <button
              v-if="navItems.prev"
              @click="emit('selectGlyph', navItems.prev)"
              class="btn-icon"
              :aria-label="'Previous: ' + navItems.prev.name"
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
              @click="emit('selectGlyph', navItems.next)"
              class="btn-icon"
              :aria-label="'Next: ' + navItems.next.name"
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
      <div class="detail-layout">
        <!-- Left: glyph display -->
        <div class="detail-left">
          <!-- Em-box -->
          <div class="detail-em-box">
            <div class="glyph-box" style="aspect-ratio: 128/55">
              <div class="glyph-grid"></div>
              <div class="glyph-baseline"></div>
              <div class="glyph-em-border"></div>
              <span class="detail-glyph-char" :style="{ fontSize: fontSize + 'px' }">
                {{ getChar(glyph.unicode) }}
              </span>
            </div>
            <div class="detail-metrics">
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-1.5">
                  <div class="w-3 h-px rounded" style="background: var(--em-stroke)"></div>
                  <span class="text-[10px]" style="color: var(--text-tertiary)">Em box 128 x 55</span>
                </div>
                <div class="flex items-center gap-1.5">
                  <div class="w-3 h-px rounded" style="background: var(--baseline-stroke)"></div>
                  <span class="text-[10px]" style="color: var(--text-tertiary)">Baseline y=27.5</span>
                </div>
              </div>
              <span class="text-[10px]" style="color: var(--text-tertiary)">advance: 128</span>
            </div>
          </div>

          <!-- Size slider -->
          <div class="detail-slider">
            <div class="flex items-center justify-between mb-2">
              <span class="label-text">Preview Size</span>
              <span class="code-text">{{ fontSize }}px</span>
            </div>
            <input type="range" v-model.number="fontSize" min="16" max="128" step="4" class="size-slider" />
          </div>

          <!-- Text preview -->
          <div class="detail-text-preview">
            <span class="label-text mb-2 block">In-line text preview</span>
            <textarea
              v-model="previewText"
              class="preview-textarea"
              :style="{ fontSize: Math.max(16, fontSize * 0.5) + 'px' }"
              rows="3"
              spellcheck="false"
            ></textarea>
          </div>
        </div>

        <!-- Right: info -->
        <div class="detail-right">
          <!-- Header -->
          <div class="mb-6">
            <h1 class="detail-title">{{ glyph.name }}</h1>
            <div class="flex flex-wrap items-center gap-2 mt-2">
              <span class="badge">{{ glyph.categoryLabel || glyph.category }}</span>
              <span v-if="glyph.version" class="badge-amber">v{{ glyph.version }}</span>
              <span v-if="glyph.status" class="badge" :class="glyph.status === 'Provisional' ? 'badge-amber' : ''">
                {{ glyph.status }}
              </span>
            </div>
          </div>

          <!-- Codepoint tiles -->
          <div class="info-grid">
            <button class="info-tile" :class="{ 'is-copied': copied }" @click="copyCodepoint">
              <span class="label-text">Unicode</span>
              <span class="info-value-accent">{{ glyph.unicode }}</span>
              <span class="copy-hint">{{ copied ? 'Copied!' : 'Click to copy' }}</span>
            </button>
            <div class="info-tile">
              <span class="label-text">Decimal</span>
              <span class="info-value">{{ glyph.dec }}</span>
            </div>
            <div class="info-tile">
              <span class="label-text">UTF-8 Bytes</span>
              <span class="info-value">{{ getUtf8Bytes(glyph.dec) }}</span>
            </div>
            <div class="info-tile">
              <span class="label-text">HTML Entity</span>
              <span class="info-value">{{ getHtmlEntity(glyph.dec) }}</span>
            </div>
            <div class="info-tile">
              <span class="label-text">CSS Content</span>
              <span class="info-value">{{ getCssContent(glyph.unicode) }}</span>
            </div>
            <div class="info-tile">
              <span class="label-text">Em Position</span>
              <span class="info-value">(64, 27.5)</span>
            </div>
          </div>

          <!-- Description -->
          <div v-if="glyph.metadata?.description" class="detail-section">
            <p class="body-text">{{ glyph.metadata.description }}</p>
          </div>

          <!-- Metadata -->
          <div v-if="visibleMetadataFields.length" class="detail-section">
            <div class="meta-grid">
              <template v-for="field in visibleMetadataFields" :key="field.key">
                <!-- Link fields (identifier, license, about) -->
                <a
                  v-if="field.type === 'link'"
                  :href="glyph.metadata[field.key]"
                  target="_blank"
                  rel="noopener"
                  class="meta-link"
                >
                  <span class="label-text">{{ field.label }}</span>
                  <span class="meta-link-value">{{ glyph.metadata[field.key] }}</span>
                  <svg class="w-3 h-3 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                    <polyline points="15 3 21 3 21 9"/>
                    <line x1="10" y1="14" x2="21" y2="3"/>
                  </svg>
                </a>

                <!-- Document fields (source — long text) -->
                <div v-else-if="field.type === 'document'" class="meta-field-block">
                  <span class="label-text">{{ field.label }}</span>
                  <span class="body-text text-xs">{{ glyph.metadata[field.key] }}</span>
                </div>

                <!-- Tag fields (subject keywords) -->
                <div v-else-if="field.type === 'tags'" class="meta-field-block">
                  <span class="label-text">{{ field.label }}</span>
                  <div class="tag-list">
                    <span v-for="tag in glyph.metadata[field.key]" :key="tag" class="tag">{{ tag }}</span>
                  </div>
                </div>

                <!-- Plain text fields -->
                <div v-else class="meta-field-block">
                  <span class="label-text">{{ field.label }}</span>
                  <span class="code-text">{{ glyph.metadata[field.key] }}</span>
                </div>
              </template>
            </div>
          </div>

          <!-- Source file -->
          <div v-if="sourceGithubUrl" class="detail-section">
            <a :href="sourceGithubUrl" target="_blank" rel="noopener" class="source-file-link">
              <svg class="w-3.5 h-3.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                <polyline points="15 3 21 3 21 9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
              <span>{{ glyph.sourcePath }}</span>
            </a>
          </div>

          <!-- Related glyphs -->
          <div v-if="related.length > 0" class="detail-section">
            <h3 class="detail-section-title">
              Related in {{ glyph.categoryLabel || glyph.category }}
            </h3>
            <div class="related-scroll">
              <button
                v-for="rel in related"
                :key="rel.codepoint"
                @click="emit('selectGlyph', rel)"
                class="related-chip"
                :title="rel.name"
              >
                <span class="related-chip-char">{{ getChar(rel.unicode) }}</span>
                <span class="code-text text-[9px] truncate w-full text-center">{{ rel.unicode }}</span>
              </button>
            </div>
          </div>

          <!-- Actions -->
          <div class="detail-actions">
            <button @click="emit('toggleCompare', glyph)" class="btn-ghost w-full sm:w-auto"
              :class="{ 'is-active-btn': isInCompare }">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path v-if="isInCompare" d="M6 18L18 6M6 6l12 12"/>
                <path v-else d="M12 5v14M5 12h14"/>
              </svg>
              {{ isInCompare ? 'Remove from Compare' : 'Add to Compare' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.detail-page {
  flex: 1;
  background: var(--bg-base);
}

/* ── Nav ── */
.detail-nav {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 64px;
  z-index: 40;
  backdrop-filter: blur(12px);
}

/* ── Layout ── */
.detail-layout {
  display: grid;
  gap: 32px;
}

@media (min-width: 1024px) {
  .detail-layout {
    grid-template-columns: 5fr 7fr;
    gap: 48px;
  }
}

/* ── Left column ── */
.detail-left {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-em-box {
  display: flex;
  flex-direction: column;
}

.detail-glyph-char {
  line-height: 1;
  position: relative;
  z-index: 1;
  font-size: clamp(48px, 8vw, 80px);
}

.detail-metrics {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
  padding: 0 4px;
}

.detail-slider {
  padding: 0 4px;
}

.size-slider {
  width: 100%;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: var(--border-default);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.size-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--bg-surface);
  box-shadow: 0 0 0 1px var(--accent);
  cursor: pointer;
}

.size-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--bg-surface);
  box-shadow: 0 0 0 1px var(--accent);
  cursor: pointer;
}

/* ── Text preview ── */
.detail-text-preview {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px;
}

.preview-textarea {
  width: 100%;
  min-height: 60px;
  padding: 10px 12px;
  font-family: 'MetFont', 'Inter', -apple-system, sans-serif;
  line-height: 1.8;
  color: var(--text-secondary);
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  resize: vertical;
  outline: none;
  transition: border-color 0.15s;
}

.preview-textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-muted);
}

/* ── Right column ── */
.detail-right {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-title {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  line-height: 1.2;
}

@media (min-width: 640px) {
  .detail-title {
    font-size: 1.75rem;
  }
}

/* ── Info tiles ── */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

@media (min-width: 640px) {
  .info-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }
}

.info-tile {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: left;
  cursor: default;
  transition: all 0.15s;
}

button.info-tile {
  cursor: pointer;
}

button.info-tile:hover {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.info-value {
  font-size: 13px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  color: var(--text-primary);
  word-break: break-all;
}

.info-value-accent {
  font-size: 13px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  font-weight: 600;
  color: var(--accent);
}

.copy-hint {
  font-size: 10px;
  margin-top: 2px;
  color: var(--text-tertiary);
  transition: color 0.15s;
}

.is-copied {
  border-color: var(--green) !important;
  background: var(--green-muted) !important;
}

.is-copied .copy-hint {
  color: var(--green) !important;
}

/* ── Sections ── */
.detail-section {
  border-top: 1px solid var(--border-subtle);
  padding-top: 16px;
}

.detail-section-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

/* ── Metadata grid ── */
.meta-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-field-block {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 12px;
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.meta-link {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 12px;
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  transition: all 0.15s;
  text-decoration: none;
}

.meta-link:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-subtle);
}

.meta-link-value {
  font-size: 12px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  word-break: break-all;
}

/* ── Tags ── */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--accent-subtle);
  color: var(--accent);
  font-weight: 500;
  text-transform: capitalize;
}

/* ── Source file link ── */
.source-file-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 12px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  word-break: break-all;
  transition: all 0.15s;
  text-decoration: none;
}

.source-file-link:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-subtle);
}

/* ── Related glyphs ── */
.related-scroll {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
}

@media (min-width: 640px) {
  .related-scroll {
    grid-template-columns: repeat(6, 1fr);
  }
}

@media (max-width: 480px) {
  .related-scroll {
    grid-template-columns: repeat(4, 1fr);
  }
}

.related-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 4px;
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.15s;
}

.related-chip:hover {
  border-color: var(--accent);
  background: var(--accent-subtle);
}

.related-chip-char {
  font-family: 'MetFont', sans-serif;
  font-size: 1.25rem;
  line-height: 1;
}

/* ── Actions ── */
.detail-actions {
  border-top: 1px solid var(--border-subtle);
  padding-top: 16px;
}

.is-active-btn {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
}
</style>
