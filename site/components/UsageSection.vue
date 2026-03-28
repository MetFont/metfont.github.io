<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import UsageWeb from './UsageWeb.vue'
import UsageMacOS from './UsageMacOS.vue'
import UsageWindows from './UsageWindows.vue'

const emit = defineEmits(['navigateBack'])

const TABS = [
  { id: 'web', label: 'Web', icon: 'globe' },
  { id: 'macos', label: 'macOS', icon: 'apple' },
  { id: 'windows', label: 'Windows', icon: 'monitor' },
]

const activeTab = ref('web')

// Read hash to determine initial tab
function syncTabFromHash() {
  const h = window.location.hash.slice(1)
  if (h === 'usage' || h === 'usage/') {
    activeTab.value = 'web'
  } else if (h.startsWith('usage/')) {
    const slug = h.replace('usage/', '')
    if (TABS.some(t => t.id === slug)) {
      activeTab.value = slug
    }
  }
}

function switchTab(tabId) {
  activeTab.value = tabId
  window.location.hash = `usage/${tabId}`
}

// Sync on mount and hash change
onMounted(() => {
  syncTabFromHash()
  window.addEventListener('hashchange', syncTabFromHash)
})

onUnmounted(() => {
  window.removeEventListener('hashchange', syncTabFromHash)
})

const currentComponent = computed(() => {
  switch (activeTab.value) {
    case 'web': return UsageWeb
    case 'macos': return UsageMacOS
    case 'windows': return UsageWindows
    default: return UsageWeb
  }
})
</script>

<template>
  <main class="usage-page animate-slide-up">
    <!-- Back nav -->
    <div class="usage-nav">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center h-12">
          <button @click="emit('navigateBack')" class="btn-icon" aria-label="Back to grid">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
          </button>
          <span class="text-xs font-medium" style="color: var(--text-secondary)">Usage</span>
        </div>
      </div>
    </div>

    <!-- Tab bar -->
    <div class="usage-tabs-bar">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex gap-1">
          <button
            v-for="tab in TABS"
            :key="tab.id"
            @click="switchTab(tab.id)"
            class="usage-tab"
            :class="{ active: activeTab === tab.id }"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <template v-if="tab.icon === 'globe'">
                <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 4l-4 4"/><path d="M12 2v10"/>
              </template>
              <template v-else-if="tab.icon === 'apple'">
                <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2z"/><path d="M12 7v5l3 3"/>
              </template>
              <template v-else-if="tab.icon === 'monitor'">
                <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
              </template>
            </svg>
            <span>{{ tab.label }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div class="usage-hero">
        <h1 class="usage-title">Using MetFont</h1>
        <p class="usage-subtitle-text">
          How to install, use, and embed MetFont symbols on each platform.
          Whether you're building for the web or typing weather reports on desktop,
          we've got you covered.
        </p>
      </div>

      <component :is="currentComponent" />

      <!-- Footer -->
      <div class="usage-footer">
        <p class="usage-humor">
          Every cloud has a silver lining. Every symbol has a Unicode codepoint.
        </p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.usage-page {
  flex: 1;
  background: var(--bg-base);
}

.usage-nav {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 64px;
  z-index: 40;
  backdrop-filter: blur(12px);
}

.usage-tabs-bar {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
}

.usage-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-tertiary);
  border-bottom: 2px solid transparent;
  transition: all 0.15s;
  margin-bottom: -1px;
}

.usage-tab:hover {
  color: var(--text-primary);
}

.usage-tab.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.usage-hero {
  margin-bottom: 2rem;
}

.usage-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.1;
  margin-bottom: 1rem;
}

@media (min-width: 640px) {
  .usage-title {
    font-size: 2.5rem;
  }
}

.usage-subtitle-text {
  font-size: 1.125rem;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 40rem;
}

.usage-footer {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px dashed var(--border-subtle);
}

.usage-humor {
  font-style: italic;
  color: var(--text-tertiary);
  font-size: 0.875rem;
  text-align: center;
}
</style>
