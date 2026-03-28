import { defineConfig } from 'vitepress'
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

export default defineConfig({
  title: 'MetFont',
  description: '541 WMO and ICAO meteorological symbols as an open-source font. Browse, search, and download every glyph. Accurate symbols for accurate weather.',
  appearance: true,
  head: [
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    // Google Fonts CSS loaded dynamically in Layout.vue to avoid render-blocking
  ],
  vite: {
    css: {
      postcss: {
        plugins: [
          tailwindcss(),
          autoprefixer(),
        ],
      },
    },
  },
  themeConfig: {
    nav: [],
    sidebar: false,
  },
  cleanUrls: true
})
