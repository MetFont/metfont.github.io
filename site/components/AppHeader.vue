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
            <img src="/logo-full.svg" alt="MetFont" class="header-logo-img" />
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
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-logo-img {
  height: 28px;
  width: auto;
  object-fit: contain;
  display: block;
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
