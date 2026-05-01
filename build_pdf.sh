#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
DIST=dist
mkdir -p "$DIST"

# Render Mermaid diagrams from WIRING_DIAGRAM.md to SVG, output a markdown
# variant with diagrams replaced by image refs. Uses system Chrome to avoid
# Apple Silicon Chromium architecture issues.
cat > "$DIST/puppeteer.json" <<'PUPPETEER_EOF'
{
  "executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "args": ["--no-sandbox"]
}
PUPPETEER_EOF

npx -y -p @mermaid-js/mermaid-cli@10.9.1 mmdc \
  -i WIRING_DIAGRAM.md \
  -o "$DIST/WIRING_DIAGRAM.md" \
  -e svg \
  --backgroundColor white \
  --puppeteerConfigFile "$DIST/puppeteer.json"
OUT="$DIST/the-builders-doctrine-v1.2-draft.pdf"

# Build title page
cat > "$DIST/00-title.md" <<'EOF'
# THE BUILDERS DOCTRINE

**v1.2-draft**
**2026-05-01**
**Hans Prahl**

---

The meta-doctrine that sits above every Hans Prahl AI product. Defines the principles, the person, the architecture of trust, the doctrine layering, and the measurement surface that make a product his — not anyone else's.

This bundle contains:

1. **The Builders Doctrine** — the canonical principles document (Section II is the founding eleven)
2. **Wiring Diagram and Walkthrough** — visual explanation of how biography compiles into product behavior, including a runtime trace of a real request end-to-end
3. **Explainer** — plain-language translation for non-technical readers
4. **Stress Test v1.0** — conformance audit across all three live products (TOP, Operator, Custer)
5. **Candidates v1.2** — what is in flight for the next doctrine version, including the synthetic portability test findings
6. **Anatomy Doctrine v2 — Implementation Plan** — the next six-session sprint to extend the body-system measurement framework

The v1.1 tag remains the canonical released version. v1.2-draft is in flight pending external test of the portability principle.

<div style="page-break-after: always;"></div>
EOF

# Combine all in order. WIRING_DIAGRAM uses dist/ version (images already rendered).
{
  cat "$DIST/00-title.md"
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat THE_BUILDERS_DOCTRINE.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat "$DIST/WIRING_DIAGRAM.md"
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat EXPLAINER.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat STRESS_TEST_v1.0.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat CANDIDATES_v1.2.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat ANATOMY_V2_PLAN.md
} > "$DIST/combined.md"

# CSS for the PDF — typographic restraint, no decoration
cat > "$DIST/print.css" <<'EOF'
@page {
  size: letter;
  margin: 0.85in 0.75in 0.85in 0.75in;
}
html { font-size: 11pt; }
body {
  font-family: -apple-system, "Helvetica Neue", "Arial", sans-serif;
  line-height: 1.45;
  color: #1a1a1a;
  max-width: none;
}
h1, h2, h3, h4, h5 {
  font-family: -apple-system, "Helvetica Neue", "Arial", sans-serif;
  font-weight: 600;
  line-height: 1.2;
  margin-top: 1.4em;
  margin-bottom: 0.5em;
  page-break-after: avoid;
}
h1 { font-size: 1.85em; border-bottom: 2px solid #1a1a1a; padding-bottom: 0.2em; }
h2 { font-size: 1.4em; border-bottom: 1px solid #999; padding-bottom: 0.15em; margin-top: 1.6em; }
h3 { font-size: 1.15em; }
h4 { font-size: 1.0em; }
p { margin: 0.55em 0; orphans: 3; widows: 3; }
ul, ol { margin: 0.5em 0; padding-left: 1.5em; }
li { margin: 0.15em 0; }
code {
  font-family: "SF Mono", "Menlo", "Consolas", monospace;
  font-size: 0.92em;
  background: #f4f4f4;
  padding: 0.08em 0.3em;
  border-radius: 2px;
}
pre {
  font-family: "SF Mono", "Menlo", "Consolas", monospace;
  font-size: 0.85em;
  background: #f4f4f4;
  border: 1px solid #ddd;
  padding: 0.7em 0.9em;
  border-radius: 3px;
  overflow-x: auto;
  page-break-inside: avoid;
}
pre code { background: transparent; padding: 0; }
blockquote {
  border-left: 3px solid #888;
  margin: 0.7em 0;
  padding: 0.1em 0 0.1em 1em;
  color: #444;
}
table {
  border-collapse: collapse;
  margin: 0.8em 0;
  font-size: 0.95em;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #bbb;
  padding: 0.35em 0.6em;
  text-align: left;
  vertical-align: top;
}
th { background: #f0f0f0; font-weight: 600; }
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0.7em auto;
  page-break-inside: avoid;
}
a { color: #0066cc; text-decoration: none; }
hr { border: none; border-top: 1px solid #999; margin: 1.4em 0; }
strong { font-weight: 600; }
EOF

# Pandoc → HTML
pandoc "$DIST/combined.md" \
  --standalone \
  --metadata title="The Builders Doctrine — v1.2-draft" \
  --css print.css \
  --resource-path="$DIST" \
  -o "$DIST/combined.html"

# Chrome headless → PDF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT" \
  --print-to-pdf-no-header \
  "file://$(pwd)/$DIST/combined.html" 2>&1 | tail -3

echo ""
echo "PDF: $OUT"
ls -lh "$OUT"
