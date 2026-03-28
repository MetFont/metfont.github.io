<script setup>
</script>

<template>
  <div class="usage-content">
    <h3 class="usage-subtitle">Windows</h3>

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
            <p class="body-text">Right-click <code class="code-inline">MetFont-glyf.ttf</code> and select <strong style="color: var(--text-primary)">"Install"</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">3</div>
          <div>
            <p class="body-text">The font is installed for all users. It appears as <strong style="color: var(--text-primary)">"MetFont"</strong> in every application's font picker.</p>
          </div>
        </div>
      </div>
      <div class="usage-note">
        <p class="body-text text-xs">
          <strong>Alternative:</strong> Drag the file to <code class="code-inline">C:\Windows\Fonts</code>
          (requires admin rights), or to <code class="code-inline">%LOCALAPPDATA%\Microsoft\Windows\Fonts</code>
          for per-user install.
        </p>
      </div>
    </section>

    <!-- Character Map -->
    <section class="usage-block">
      <h4 class="usage-heading">Character Map</h4>
      <p class="body-text mb-4">
        Use the built-in Character Map to browse and copy PUA glyphs:
      </p>
      <div class="usage-steps">
        <div class="usage-step">
          <div class="step-num">1</div>
          <div>
            <p class="body-text">Open Character Map: press <kbd class="kbd">Win</kbd>, type <code class="code-inline">charmap</code>, press Enter.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">2</div>
          <div>
            <p class="body-text">In the <strong style="color: var(--text-primary)">"Font"</strong> dropdown, select <strong style="color: var(--text-primary)">"MetFont"</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">3</div>
          <div>
            <p class="body-text">Check <strong style="color: var(--text-primary)">"Advanced view"</strong>. Set <strong style="color: var(--text-primary)">"Group by"</strong> to <strong style="color: var(--text-primary)">"Unicode Subrange"</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">4</div>
          <div>
            <p class="body-text">Select <strong style="color: var(--text-primary)">"Private Use Area"</strong> from the subgroup list. All 541 MetFont symbols will appear.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">5</div>
          <div>
            <p class="body-text">Click a symbol, click <strong style="color: var(--text-primary)">"Select"</strong>, then <strong style="color: var(--text-primary)">"Copy"</strong>. Paste into any application with MetFont set as the active font.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Word -->
    <section class="usage-block">
      <h4 class="usage-heading">Microsoft Word</h4>
      <p class="body-text mb-4">
        Insert symbols directly into Word documents:
      </p>
      <div class="usage-steps">
        <div class="usage-step">
          <div class="step-num">1</div>
          <div>
            <p class="body-text">Go to <strong style="color: var(--text-primary)">Insert &rarr; Symbol &rarr; More Symbols</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">2</div>
          <div>
            <p class="body-text">Set <strong style="color: var(--text-primary)">"Font"</strong> to <strong style="color: var(--text-primary)">"MetFont"</strong> and <strong style="color: var(--text-primary)">"Subset"</strong> to <strong style="color: var(--text-primary)">"Private Use Area"</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">3</div>
          <div>
            <p class="body-text">Browse the symbols, select one, and click <strong style="color: var(--text-primary)">"Insert"</strong>. Recently used symbols appear in the quick-access dropdown.</p>
          </div>
        </div>
      </div>
      <div class="usage-note">
        <p class="body-text text-xs">
          <strong>Shortcut:</strong> Assign a keyboard shortcut via <strong>Insert &rarr; Symbol &rarr; Shortcut Key</strong>
          for frequently used weather symbols. E.g., <kbd class="kbd">Alt</kbd>+<kbd class="kbd">R</kbd> for rain.
        </p>
      </div>
    </section>

    <!-- Other Apps -->
    <section class="usage-block">
      <h4 class="usage-heading">Other Applications</h4>
      <div class="app-grid">
        <div class="app-tile">
          <h5 class="app-tile-title">PowerPoint</h5>
          <p class="body-text text-xs">Insert &rarr; Symbol. Same process as Word. Symbols inserted as font glyphs scale with text size and respect color formatting.</p>
        </div>
        <div class="app-tile">
          <h5 class="app-tile-title">Excel</h5>
          <p class="body-text text-xs">Insert &rarr; Symbol. Select MetFont, Private Use Area. Symbols render in cells and can be used in formulas or conditional formatting rules.</p>
        </div>
        <div class="app-tile">
          <h5 class="app-tile-title">Paint / GIMP</h5>
          <p class="body-text text-xs">Select the Text tool, choose MetFont as the font. Type or paste PUA characters (U+E000&ndash;U+E7FF). Use Character Map to copy symbols first.</p>
        </div>
      </div>
    </section>

    <!-- Unicode Input -->
    <section class="usage-block">
      <h4 class="usage-heading">Direct Unicode Input</h4>
      <p class="body-text mb-4">
        Type PUA codepoints directly in most Windows applications:
      </p>
      <div class="usage-steps">
        <div class="usage-step">
          <div class="step-num">1</div>
          <div>
            <p class="body-text">Hold <kbd class="kbd">Alt</kbd> and type the codepoint on the <strong style="color: var(--text-primary)">numeric keypad</strong>.</p>
          </div>
        </div>
        <div class="usage-step">
          <div class="step-num">2</div>
          <div>
            <p class="body-text">For Unicode hex input, enable the registry key: <code class="code-inline">HKCU\Control Panel\Input Method\EnableHexInput</code> = <code class="code-inline">1</code>. Then <kbd class="kbd">Alt</kbd>+<kbd class="kbd">+</kbd> followed by the hex code (e.g., <kbd class="kbd">E713</kbd>).</p>
          </div>
        </div>
      </div>
      <div class="usage-note">
        <p class="body-text text-xs">
          <strong>Simplest method:</strong> Use Character Map to copy symbols, then paste with <kbd class="kbd">Ctrl</kbd>+<kbd class="kbd">V</kbd>.
          No registry changes needed. Works everywhere.
        </p>
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
