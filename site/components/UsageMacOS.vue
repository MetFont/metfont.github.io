<script setup>
</script>

<template>
  <div class="usage-content">
    <h3 class="usage-subtitle">macOS</h3>

    <!-- Install -->
    <section class="usage-block">
      <h4 class="usage-heading">Install the Font</h4>
      <div class="usage-steps">
        <div class="usage-step">
          <div class="step-num">1</div>
          <div>
            <p class="body-text">Download the <strong style="color: var(--text-primary)">TTF</strong> file from the <a href="#download" class="usage-link">Download page</a>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">2</div>
          <div>
            <p class="body-text">Double-click the <code class="code-inline">MetFont-glyf.ttf</code> file. Font Book will open.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">3</div>
          <div>
            <p class="body-text">Click <strong style="color: var(--text-primary)">"Install Font"</strong>. The font is now available system-wide.</p>
          </div>
        </div>
      </div>
      <div class="usage-note">
        <p class="body-text text-xs">
          <strong>Alternative:</strong> Drag the <code class="code-inline">.ttf</code> file directly into
          the Font Book window, or to <code class="code-inline">~/Library/Fonts/</code>.
        </p>
      </div>
    </section>

    <!-- Character Viewer -->
    <section class="usage-block">
      <h4 class="usage-heading">Character Viewer (Emoji &amp; Symbols)</h4>
      <p class="body-text mb-4">
        Use the built-in Character Viewer to browse and insert PUA glyphs:
      </p>
      <div class="usage-steps">
        <div class="usage-step">
          <div class="step-num">1</div>
          <div>
            <p class="body-text">Open Character Viewer: <strong style="color: var(--text-primary)">Edit &rarr; Emoji &amp; Symbols</strong> in most apps, or press <kbd class="kbd">Ctrl</kbd>+<kbd class="kbd">Cmd</kbd>+<kbd class="kbd">Space</kbd>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">2</div>
          <div>
            <p class="body-text">Click the <strong style="color: var(--text-primary)">gear icon</strong> in the top-left and select <strong style="color: var(--text-primary)">"Customize List..."</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">3</div>
          <div>
            <p class="body-text">Enable <strong style="color: var(--text-primary)">"Private Use Area"</strong> under Code Tables.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">4</div>
          <div>
            <p class="body-text">Scroll to the Private Use Area section. Select "MetFont" as the font. Browse U+E000&ndash;U+E7FF and double-click to insert.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Unicode Hex Input -->
    <section class="usage-block">
      <h4 class="usage-heading">Unicode Hex Input Keyboard</h4>
      <p class="body-text mb-4">
        Type PUA codepoints directly using the Unicode Hex Input keyboard:
      </p>
      <div class="usage-steps">
        <div class="usage-step">
          <div class="step-num">1</div>
          <div>
            <p class="body-text">Open <strong style="color: var(--text-primary)">System Settings &rarr; Keyboard &rarr; Text Input &rarr; Edit</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">2</div>
          <div>
            <p class="body-text">Click <strong style="color: var(--text-primary)">+</strong> and add <strong style="color: var(--text-primary)">"Unicode Hex Input"</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">3</div>
          <div>
            <p class="body-text">Switch to Unicode Hex Input (menu bar flag icon or input source selector).</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">4</div>
          <div>
            <p class="body-text">Hold <kbd class="kbd">Option</kbd> and type the hex code: e.g., <kbd class="kbd">Option</kbd>+<kbd class="kbd">E</kbd><kbd class="kbd">7</kbd><kbd class="kbd">1</kbd><kbd class="kbd">3</kbd> inserts the rain symbol (U+E713).</p>
          </div>
        </div>
      </div>
      <div class="usage-note">
        <p class="body-text text-xs">
          Make sure MetFont is selected as the active font in your application, or the PUA character
          will render as a box from the fallback font.
        </p>
      </div>
    </section>

    <!-- App Usage -->
    <section class="usage-block">
      <h4 class="usage-heading">Using in Applications</h4>
      <div class="app-grid">
        <div class="app-tile">
          <h5 class="app-tile-title">Pages / Keynote</h5>
          <p class="body-text text-xs">Select MetFont from the font picker. Use Character Viewer or paste a PUA character. The font appears in the formatting sidebar under "MetFont".</p>
        </div>
        <div class="app-tile">
          <h5 class="app-tile-title">TextEdit</h5>
          <p class="body-text text-xs">Format &rarr; Font &rarr; Show Fonts. Search for "MetFont". Type or paste PUA characters. Works in both rich and plain text modes.</p>
        </div>
        <div class="app-tile">
          <h5 class="app-tile-title">Microsoft Word</h5>
          <p class="body-text text-xs">Insert &rarr; Advanced Symbol. Set Font to "MetFont". Subset: "Private Use Area". Select and Insert. Recent symbols appear in the quick-access bar.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.usage-content {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.usage-subtitle {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 1.5rem;
}

.usage-block {
  margin-bottom: 2rem;
}

.usage-heading {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem;
}

.usage-link {
  color: var(--accent);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.code-inline {
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  font-size: 12px;
  padding: 1px 4px;
  border-radius: 3px;
  background: var(--bg-overlay);
}

.kbd {
  font-family: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--border-default);
  background: var(--bg-surface);
  color: var(--text-primary);
  box-shadow: 0 1px 0 var(--border-default);
}

.usage-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.usage-step {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.step-num {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--accent-muted);
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.usage-note {
  margin-top: 0.75rem;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  background: var(--accent-subtle);
  border: 1px solid var(--accent-muted);
}

.app-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

@media (min-width: 640px) {
  .app-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }
}

.app-tile {
  background: var(--bg-overlay);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px;
}

.app-tile-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px;
}
</style>
