/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './components/**/*.vue',
    './.vitepress/theme/**/*.vue',
    './.vitepress/styles.css',
    './index.md',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['IBM Plex Mono', 'SF Mono', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
}
