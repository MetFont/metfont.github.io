<script setup>
const props = defineProps({
  compareList: { type: Array, default: () => [] }
})

const emit = defineEmits(['openDetail', 'toggleCompare', 'clearAll'])

function getChar(unicode) {
  return String.fromCodePoint(parseInt(unicode.replace('U+', ''), 16))
}
</script>

<template>
  <div class="compare-tray">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
      <div class="flex items-center gap-3">
        <span class="text-xs font-medium" style="color: var(--text-secondary)">Compare</span>
        <div class="compare-chips">
          <div v-for="glyph in compareList" :key="glyph.codepoint"
            class="compare-chip" @click="emit('openDetail', glyph)">
            <span class="text-lg leading-none">{{ getChar(glyph.unicode) }}</span>
            <span class="code-text text-[10px]">{{ glyph.unicode }}</span>
            <button @click.stop="emit('toggleCompare', glyph)" class="compare-remove" aria-label="Remove">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6 6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        <button @click="emit('clearAll')" class="compare-clear">Clear all</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.compare-tray {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  animation: slideUp 0.2s ease-out;
}

.compare-chips {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.compare-chips::-webkit-scrollbar {
  display: none;
}

.compare-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--bg-overlay);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.compare-chip:hover {
  border-color: var(--accent);
}

.compare-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  transition: color 0.15s;
}

.compare-remove:hover {
  color: var(--red);
}

.compare-clear {
  font-size: 12px;
  margin-left: auto;
  white-space: nowrap;
  color: var(--text-tertiary);
  transition: color 0.15s;
}

.compare-clear:hover {
  color: var(--text-secondary);
}
</style>
