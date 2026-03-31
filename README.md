# MetFont Website

Public website for [MetFont](https://github.com/MetFont/metfont) — 541 WMO/ICAO meteorological symbols as a Unicode font.

Live site: https://metfont.github.io

## Structure

```
site/               VitePress application
  components/       Vue components (UI sections and detail views)
  .vitepress/       VitePress configuration and theme overrides
    theme/          Custom theme (Layout.vue, CSS overrides)
    styles.css      Global CSS with design tokens (dark/light themes)
  public/           Static assets served as-is (logos, favicons, fonts)
  index.md          VitePress entry page
  package.json      VitePress dependencies

.github/workflows/
  site.yml          GitHub Actions: download font release → build → deploy to GitHub Pages
```

## Build

The site downloads the pre-built font package (fonts + `metadata.json`) from the [MetFont releases](https://github.com/MetFont/metfont/releases/latest) at CI time. No font build tooling is needed locally.

```bash
cd site
npm install
npm run build   # builds into site/.vitepress/dist/
npm run dev     # dev server with hot reload
```

## Font Assets

Fonts and `metadata.json` are downloaded from `releases/latest` during CI and placed in `site/public/`. They are not committed to the repo.

## Theme

The site uses a custom VitePress theme with CSS design tokens for dark/light mode. The font (MetFont) is loaded via `@font-face` pointing to `/MetFont-glyf.woff2`.
