<script setup>
const props = defineProps({
  glyph: { type: Object, required: true },
  isCompared: { type: Boolean, default: false }
})

const emit = defineEmits(['open', 'toggleCompare'])

function getChar(unicode) {
  return String.fromCodePoint(parseInt(unicode.replace('U+', ''), 16))
}

function getCategoryLabel(cat) {
  // Only transform raw category IDs (directory names like "ICAO_SigWx", "CL_CloudLow")
  // Do NOT transform already-formatted categoryLabels like "Cloud High (CH)"
  // Detection: formatted labels don't contain underscores
  if (!cat || !cat.includes('_')) return cat
  return cat
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/_/g, ' ')
    .replace(/  +/g, ' ')
    .trim()
}

// Plane color for category indicator dot
const PLANE_COLORS = {
  'sky-cloud': '#4a9eff',
  'present-weather': '#f0a030',
  'past-weather': '#a060e0',
  'state-of-ground': '#8b6914',
  'pressure': '#6c7fd9',
  'wind-ocean': '#2ab0a0',
  'significant-weather': '#e05050',
}

function getPlaneColor(cat) {
  if (!cat) return null
  const planeMap = {
    'CH_CloudHigh': 'sky-cloud', 'CL_CloudLow': 'sky-cloud',
    'CM_CloudMedium': 'sky-cloud', 'C_CloudGenus': 'sky-cloud',
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
  const plane = planeMap[cat]
  return plane ? PLANE_COLORS[plane] : null
}
</script>

<template>
  <article
    class="glyph-card"
    :class="{ 'is-compared': isCompared }"
    @click="emit('open', glyph)"
  >
    <div class="glyph-card-preview">
      <div class="glyph-box">
        <div class="glyph-grid"></div>
        <div class="glyph-baseline"></div>
        <span class="glyph-card-char">{{ getChar(glyph.unicode) }}</span>
      </div>
      <span
        v-if="getPlaneColor(glyph.category)"
        class="glyph-cat-dot"
        :style="{ background: getPlaneColor(glyph.category) }"
        :title="glyph.category"
      ></span>
    </div>
    <div class="glyph-card-info">
      <span class="glyph-card-code">{{ glyph.unicode }}</span>
      <span class="glyph-card-cat">{{ getCategoryLabel(glyph.category) }}</span>
      <span class="glyph-card-name" :title="glyph.name">{{ glyph.name }}</span>
    </div>
    <button
      @click.stop="emit('toggleCompare', glyph)"
      class="glyph-card-action"
      :class="{ active: isCompared }"
      :aria-label="isCompared ? 'Remove from compare' : 'Add to compare'"
    >
      <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path v-if="isCompared" d="M6 18L18 6M6 6l12 12"/>
        <path v-else d="M12 5v14M5 12h14"/>
      </svg>
    </button>
  </article>
</template>

<style scoped>
.glyph-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.glyph-card:hover {
  border-color: var(--border-default);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.glyph-card.is-compared {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent);
}

.glyph-card-preview {
  padding: 10px 10px 0;
  position: relative;
}

.glyph-cat-dot {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  opacity: 0.85;
  z-index: 3;
}

.glyph-card-char {
  font-size: 32px;
  line-height: 1;
  position: relative;
  z-index: 1;
}

@media (min-width: 640px) {
  .glyph-card-char {
    font-size: 38px;
  }
}

.glyph-card-info {
  padding: 8px 10px 10px;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.glyph-card-code {
  font-size: 11px;
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  color: var(--text-tertiary);
  letter-spacing: 0.02em;
}

.glyph-card-cat {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.glyph-card-name {
  font-size: 12px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  /* min-height ensures uniform card height even with short names */
  min-height: 1.2em;
}

.glyph-card-action {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  color: var(--text-tertiary);
  opacity: 0.7;
  transition: all 0.15s;
  z-index: 2;
}

.glyph-card:hover .glyph-card-action,
.glyph-card-action.active {
  opacity: 1;
}

.glyph-card-action:hover {
  color: var(--accent);
  border-color: var(--accent);
  opacity: 1;
}

.glyph-card-action.active {
  background: var(--accent-muted);
  color: var(--accent);
  border-color: var(--accent);
}
</style>
