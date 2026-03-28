<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  total: { type: Number, default: 0 },
  currentView: { type: String, default: 'grid' },
  selectedGlyph: { type: Object, default: null }
})

const emit = defineEmits(['navigateGrid', 'navigateAbout', 'navigateDownload', 'navigateCategories', 'navigateUsage'])

// ── Theme toggle ──
const isLight = ref(false)

function toggleTheme() {
  isLight.value = !isLight.value
  document.documentElement.classList.toggle('light', isLight.value)
  try {
    localStorage.setItem('wws-theme', isLight.value ? 'light' : 'dark')
  } catch (e) {}
}

onMounted(() => {
  // Sync with VitePress appearance or stored preference
  const stored = (function() {
    try { return localStorage.getItem('wws-theme') } catch (e) { return null }
  })()
  if (stored === 'light') {
    isLight.value = true
    document.documentElement.classList.add('light')
  } else if (stored === 'dark') {
    isLight.value = false
    document.documentElement.classList.remove('light')
  } else {
    // Default: dark
    isLight.value = false
    document.documentElement.classList.remove('light')
  }

  // Sync if VitePress changes theme externally
  window.addEventListener('vvp-color-scheme-change', (e) => {
    const isDark = e.detail === 'dark'
    isLight.value = !isDark
    document.documentElement.classList.toggle('light', !isDark)
  })
})
</script>

<template>
  <header class="site-header">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14 sm:h-16">
        <a href="#" @click.prevent="emit('navigateGrid')" class="flex items-center gap-3">
          <div class="header-logo">
            <svg viewBox="0 0 32 32" fill="none" class="header-logo-svg">
              <circle cx="12" cy="10" r="5" fill="#f0a030" opacity="0.9"/>
              <line x1="12" y1="2" x2="12" y2="4" stroke="#f0a030" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="5" y1="10" x2="7" y2="10" stroke="#f0a030" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="7" y1="5" x2="8.5" y2="6.5" stroke="#f0a030" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="17" y1="5" x2="15.5" y2="6.5" stroke="#f0a030" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="17" y1="10" x2="19" y2="10" stroke="#f0a030" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M10 16c-2.5 0-4.5 2-4.5 4.5s2 4.5 4.5 4.5h12c2 0 3.5-1.5 3.5-3.5s-1.5-3.5-3.5-3.5c-.3-1.8-1.8-3.2-3.7-3.2-1.6 0-3 .9-3.7 2.2-.5-.6-1.2-1-2.1-1z" fill="white" opacity="0.95"/>
              <line x1="11" y1="26" x2="10" y2="29" stroke="#4a9eff" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="16" y1="25" x2="15" y2="29" stroke="#4a9eff" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="21" y1="26" x2="20" y2="29" stroke="#4a9eff" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="hidden sm:block">
            <div class="text-sm font-semibold" style="color: var(--text-primary)">MetFont: Symbols for Accurate Weather</div>
            <div class="text-xs" style="color: var(--text-tertiary)">OGC/WMO/ICAO weather symbols in a font</div>
          </div>
        </a>
        <div class="flex items-center gap-3">
          <button
            @click="toggleTheme"
            class="theme-toggle"
            :aria-label="isLight ? 'Switch to dark mode' : 'Switch to light mode'"
            :title="isLight ? 'Dark mode' : 'Light mode'"
          >
            <!-- Sun (shown in dark mode to switch to light) -->
            <svg v-if="!isLight" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="4"/>
              <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
            </svg>
            <!-- Moon (shown in light mode to switch to dark) -->
            <svg v-else class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
            </svg>
          </button>
          <button
            @click="emit('navigateGrid')"
            class="header-nav-link"
            :class="{ active: currentView === 'grid' }"
          >
            Browse
          </button>
          <button
            @click="emit('navigateCategories')"
            class="header-nav-link hidden sm:inline-flex"
            :class="{ active: currentView === 'categories' }"
          >
            Categories
          </button>
          <button
            @click="emit('navigateUsage')"
            class="header-nav-link hidden sm:inline-flex"
            :class="{ active: currentView === 'usage' }"
          >
            Usage
          </button>
          <button
            @click="emit('navigateDownload')"
            class="header-nav-link"
            :class="{ active: currentView === 'download' }"
          >
            Download
          </button>
          <button
            @click="emit('navigateAbout')"
            class="header-nav-link"
            :class="{ active: currentView === 'about' }"
          >
            About
          </button>
          <span class="badge">{{ total }} symbols</span>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
}

.header-logo {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-raised);
  border: 1px solid var(--border-subtle);
}

.header-logo-svg {
  width: 28px;
  height: 28px;
}

.header-nav-link {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-tertiary);
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}

.header-nav-link:hover {
  color: var(--text-primary);
  background: var(--accent-subtle);
}

.header-nav-link.active {
  color: var(--accent);
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.15s;
  flex-shrink: 0;
}

.theme-toggle:hover {
  color: var(--text-primary);
  border-color: var(--border-default);
  background: var(--accent-subtle);
}
</style>
